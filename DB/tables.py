from sqlalchemy import create_engine, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from typing import List

Base = declarative_base()

engine = create_engine('sqlite:///new_db.sqlite3', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class Student(Base):
    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    done_homework: Mapped[str] = mapped_column(insert_default='000000')
    tg_chat_token: Mapped[int] = mapped_column(BigInteger, nullable=True)

    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'), nullable=True)
    group: Mapped['Group'] = relationship(back_populates='students')

    def __repr__(self):
        return f'Student {self.first_name} {self.patronymic} | {self.done_homework} | {self.tg_chat_token} '


class Group(Base):
    __tablename__ = 'group'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)
    class_letter: Mapped[str] = mapped_column(nullable=False)

    tutor_first_name: Mapped[str] = mapped_column(nullable=True)
    tutor_second_name: Mapped[str] = mapped_column(nullable=True)
    tutor_patronymic: Mapped[str] = mapped_column(nullable=True)
    tutor_link: Mapped[str] = mapped_column(nullable=True)

    info: Mapped[str] = mapped_column(nullable=True)

    students: Mapped[List['Student']] = relationship(back_populates='group')

    teacher_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'), nullable=True)
    teacher: Mapped['Teacher'] = relationship(back_populates='groups')



# class HomeworkGroup(Base):
#     pass
#
#
# class Homework(Base):
#     pass
#
#
# class Task(Base):
#     pass

class Teacher(Base):
    __tablename__ = 'teacher'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)

    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tg_chat_token: Mapped[int] = mapped_column(BigInteger, nullable=True)

    groups: Mapped[List['Group']] = relationship(back_populates='teacher')


    def __repr__(self):
        return f'Teacher: {self.first_name} {self.second_name} | token: {self.tg_chat_token}\n'