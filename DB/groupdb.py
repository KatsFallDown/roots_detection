from typing import List
from tables import Group, Student

class GroupDB:
    def __init__(self, session):
        self.__session = session

    def add_one(self, number: int, class_letter: str, tutor_first_name: str = None, tutor_second_name: str = None,
                tutor_patronymic: str = None, tutor_link: str = None, info: str = None, students: List[Student] = [],
                teacher_id: int = None):
        new_group = Group(
            number=number,
            class_letter=class_letter,
            tutor_first_name=tutor_first_name.lower() if tutor_second_name else None,
            tutor_second_name=tutor_second_name.lower() if tutor_second_name else None,
            tutor_patronymic=tutor_patronymic.lower() if tutor_second_name else None,
            tutor_link=tutor_link if tutor_second_name else None,
            info=info if tutor_second_name else None,
            students=students if tutor_second_name else [],
            teacher_id=teacher_id if tutor_second_name else None
        )
        self.__session.add(new_group)
        self.__session.commit()
        return new_group.id

    def add_students(self, student_id: int, group_id: int):
        student = self.__session.query(Student).filter_by(id=student_id).first()
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if student and group:
            student.group_id = group.id
            self.__session.commit()
            return True

        return False