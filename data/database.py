"""
Чтобы начать использовать Базу Данных, нужно написать в основном исполняемом файле:

db = DataBase()

db - интерфейс, через который происходит взаимодействие с БД. Функционал ограниченный только необходимыми функциями

пул примеров:

class_9 = [
        'Феринов Максим Валентинович',
        'Полюев Виктор Павлович',
        'Аликперов Александр Александрович',
        'Филимонова Арина Александровна',
        'Сучков Михаил Сергеевич',
        'Глазунов Глеб Викторович',
    ]
db.upload_students(class_9, 9) - подгрузит все данные из списка и для кадой записи выставит 9 класс

if not db.has_token('Завадский Глеб Дмитриевич'):                   - Добавляем токен для студента с None в поле token
    db.update_student_token('Завадский Глеб Дмитриевич', 1234567)

db.head() - вывод первых 5 строк таблицы

"""
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from typing import List, Optional
from prettytable import PrettyTable
from sqlalchemy.orm import joinedload

Base = declarative_base()


class TaskGroup(Base):
    __tablename__ = 'task_group'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(nullable=False)
    info: Mapped[str] = mapped_column(nullable=True)

    tasks: Mapped[Optional[List['Task']]] = relationship(back_populates='task_group')
    grades: Mapped[Optional[List['Grade']]] = relationship(back_populates='task_group')

    def __repr__(self):
        return f'TaskGroup\n' \
               f'\tid: {self.id!r}\n' \
               f'\tgroup_name: {self.group_name}\n' \
               f'\tinfo {self.info}\n' \
               f'\ttasks: {self.tasks!r}'


class Grade(Base):
    __tablename__ = 'grade'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column()

    students: Mapped[List['Student']] = relationship(back_populates='grade')

    task_group_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task_group.id'), nullable=True)
    task_group: Mapped['TaskGroup'] = relationship(back_populates='grades')

    def __repr__(self):
        return f'\nGrade\n' \
               f'\tid: {self.id}\n' \
               f'\tnumber: {self.number}\n' \
               f'\tStudents: {self.students}'


class Student(Base):
    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    tg_token: Mapped[int] = mapped_column(BigInteger, nullable=True)
    done_homework: Mapped[str] = mapped_column(insert_default='000000')

    grade_id: Mapped[int] = mapped_column(ForeignKey('grade.id'), nullable=True)
    grade: Mapped['Grade'] = relationship(back_populates='students')

    def __repr__(self):
        return f'\n\tStudent\n' \
               f'\t\tid: {self.id}\n' \
               f'\t\tname: {self.name}\n' \
               f'\t\ttg_token: {self.tg_token}\n' \
               f'\t\tdone_homework: {self.done_homework}\n'


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    info: Mapped[str] = mapped_column(nullable=True)

    task_group_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task_group.id'), nullable=True)
    task_group: Mapped['TaskGroup'] = relationship(back_populates='tasks')

    def __repr__(self):
        return f'Task\n' \
               f'\tid: {self.id}\n' \
               f'\tinfo: {self.info}'


class DataBase:

    def __init__(self):
        self.__engine = create_engine('sqlite:///mydb.db', echo=True)
        Base.metadata.create_all(bind=self.__engine)

    def upload_students(self, student_data: list[str], class_number: int):
        """
        Загружает данные о студентах в базу данных.
        Полагаем, что данные вводятся для конкретного класса
        Встроен перевод в нижний регистр
        :param student_data: list[str]
        :param class_number: int
        :return: Nothing
        """

        with Session(self.__engine) as session:
            group = session.query(Grade).where(Grade.number == class_number).first()
            print(group)
            if not group:
                session.add(
                    Grade(number=class_number)
                )
            session.commit()
            group = session.query(Grade).where(Grade.number == class_number).first()
            print(group)
            for student in student_data:
                name = student.lower().strip()
                if self.is_student_exists(name):
                    print(f"Пропущен при добавлении: {name} (уж. сущ.)")
                    continue

                group.students.append(
                    Student(name=name,
                            grade_id=group.id)
                )
            session.commit()

    def update_student_token(self, name: str, token: int):
        """
        Изменяет значение токена для конкретного студента
        :param name: str
        :param token: int
        :return: Ничего
        """
        with Session(self.__engine) as session:
            student = session.query(Student).filter(Student.name == name.lower()).first()
            student.tg_token = token
            session.commit()

    def get_name_by_token(self, token: int):
        """
        Ищет студента по токену и возвращает его фио
        :param token: int
        :return: str ФИО студента
        """
        with Session(self.__engine) as session:
            student = session.query(Student).filter(Student.tg_token == token).first()
            return student.name

    def get_token_by_name(self, name: str):
        """
        Возвращает значение токена конкретного студента
        :param name: str
        :return: tg_token: int
        """
        with Session(self.__engine) as session:
            student = session.query(Student).where(Student.name == name).first()
            return student.tg_token

    def get_all_student_names_in_class(self, class_number: int):
        """
        Возвращает список всех фио;
        Только сейчас понял, что тупая идея. Потом перепишу под проверку существования студента
        :return: list[str]
        """
        names = []
        with Session(self.__engine) as session:
            stmt = session.query(Grade).where(Grade.number == class_number).first()
            for student in stmt.students:
                names.append(student.student.name)

    def get_class_number(self, token: int):
        """
        Возвращает значение номера класса для студента по его токену
        :param token: int
        :return: int
        """
        with Session(self.__engine) as session:
            stmt = session.query(Student).where(Student.tg_token == token).first()
            return stmt.grade.number

    def is_student_exists(self, name: str):

        """
        Проверка на существование студента
        Встроен перевод в нижний регистр
        :param name: str
        :return: bool
        """
        with Session(self.__engine) as session:
            a = session.query(Student).filter(Student.name == name.lower()).count() > 0
            return a

    def is_token_exist(self, token: int):
        """
        Проверка на наличие токена
        Проверяет наличие токена в БД
        :param token: str
        :return: bool
        """
        with Session(self.__engine) as session:
            student = session.query(Student).filter(Student.tg_token == token).first()
            return student.tg_token != 0 if student else False

    def is_task_done(self, token: int, task_number: int):
        """
        Проверка решена ли домашняя работа
        :param token: int
        :param task_number: int
        :return: bool
        """
        with Session(self.__engine) as session:
            stmt = session.query(Student).where(Student.tg_token == token).first()
            sequence = bin(int(stmt.done_homework, 16))[2:]
            print(sequence)
            if not len(sequence) >= task_number:
                return 0

            return sequence[-task_number]

    def has_token(self, name: str):
        """
        Проверка на наличие токена
        Встроен перевод в нижний регистр
        :param name: str
        :return: bool
        """
        with Session(self.__engine) as session:
            student = session.query(Student).filter(Student.name == name.lower()).first()
            return student.tg_token != 0 if student else False

    def accept_hw(self, token: int, task_number: int):
        with Session(self.__engine) as session:
            student = session.query(Student).where(Student.tg_token == token).first()
            old_value = student.done_homework
            sequence = int(old_value, 16)
            sequence |= (1 << (task_number - 1))
            student.done_homework = hex(sequence)

            session.commit()

    @staticmethod
    def get_number_student_done_hw(value: str):
        return bin(int(value, 16))[2:].count("1")

    def __get_head(self, value):
        """
        Системный метод
        :param value: int
        :return: list[Session]
        """
        with Session(self.__engine) as session:
            students = session.query(Student).options(joinedload(Student.grade)).limit(value).all()
            return [student for student in students]

    def head(self, value: int = 5):
        """
        Строт таблицу с указанной длинной по данным из Базы Данных
        :param value: int (default = 5)
        :return: Ничего
        """
        students = self.__get_head(value)

        table = PrettyTable()
        table.field_names = ["ID", "Имя", "Класс", "Токен", "Домашки", 'value']
        for student in students:
            table.add_row([student.id,
                           student.name,
                           student.grade.number,
                           student.tg_token,
                           self.get_number_student_done_hw(student.done_homework),
                           student.done_homework
                           ])

        print(table)
