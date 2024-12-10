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

    def add_student(self, student_id: int, group_id: int):
        student = self.__session.query(Student).filter_by(id=student_id).first()
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if student and group:
            student.group_id = group.id
            self.__session.commit()
            return True

        return False

    def head(self, value: int):
        groups = self.__session.query(Group).limit(value).all()
        for group in groups:
            print(group)

    def set_number(self, group_id: int, new_number: int):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.number = new_number
            self.__session.commit()
            return True

        return False

    def set_class_letter(self, group_id: int, new_class_letter: str):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.class_letter = new_class_letter
            self.__session.commit()
            return True

        return False

    def set_tutor_first_name(self, group_id: int, tutor_first_name: str):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.tutor_first_name = tutor_first_name
            self.__session.commit()
            return True

        return False

    def set_tutor_second_name(self, group_id: int, tutor_second_name: str):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.tutor_second_name = tutor_second_name
            self.__session.commit()
            return True

        return False

    def set_tutor_patronymic(self, group_id: int, tutor_patronymic: str):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.tutor_patronymic = tutor_patronymic
            self.__session.commit()
            return True

        return False

    def set_tutor_link(self, group_id: int, tutor_link: str):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.tutor_link = tutor_link
            self.__session.commit()
            return True

        return False

    def set_info(self, group_id: int, info: int):
        group = self.__session.query(Group).filter_by(id=group_id).first()

        if group:
            group.info = info
            self.__session.commit()
            return True

        return False

    def get_group_info(self, id: int):
        group = self.__session.query(Group).filter_by(id=id).first()

        info = {
            'id': group.id,
            'number': group.number,
            'class_letter': group.class_letter,
            'tutor_first_name': group.tutor_first_name,
            'tutor_second_name': group.tutor_second_name,
            'tutor_patronymic': group.tutor_patronymic,
            'tutor_link': group.tutor_link,
            'info': group.info,
            'students': [student.id for student in group.students]
        }
        return info if info else False