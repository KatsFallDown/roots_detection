from tables import Student

class StudentDB:
    def __init__(self, session):
        self.__session = session

    def add_one(self, first_name: str, second_name: str, tg_chat_token: int = None, group_id: int = None, patronymic: str = None):

        new_student = Student(first_name=first_name.lower(),
                              second_name=second_name.lower(),
                              patronymic=patronymic.lower() if patronymic else None,
                              tg_chat_token=tg_chat_token,
                              group_id=group_id)

        self.__session.add(new_student)
        self.__session.commit()
        return new_student.id

    def head(self, value: int):
        students = self.__session.query(Student).limit(value).all()
        for student in students:
            print(student)

    def set_first_name(self, first_name: str, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        if student:
            student.first_name = first_name.lower()
            self.__session.commit()
            return True
        return False

    def set_second_name(self, second_name: str, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        if student:
            student.second_name = second_name.lower()
            self.__session.commit()
            return True
        return False

    def set_patronymic(self, patronymic: str, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        if student:
            student.patronymic = patronymic.lower()
            self.__session.commit()
            return True
        return False

    def set_tg_chat_token(self, new_tg_chat_token: int, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        if student:
            student.tg_chat_token = new_tg_chat_token
            self.__session.commit()
            return True
        return False

    # TODO: Дописать метод!!!
    def set_group(self, first_name: str, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        if student:
            student.first_name = first_name
            self.__session.commit()
            return True
        return False

    # TODO: Дописать метод!!!
    def get_student_info(self, id: int = None, tg_chat_token: int = None):
        student = 0
        if id:
            student = self.__session.query(Student).filter_by(id=id).first()

        elif tg_chat_token:
            student = self.__session.query(Student).filter_by(tg_chat_token=tg_chat_token).first()

        info = {
            'id': student.id,
            'first_name': student.first_name,
            'second_name': student.second_name,
            'patronymic': student.patronymic,
            'tg_chat_token': student.tg_chat_token,
            'group_id': student.group_id,
            'done_homework': student.done_homework
        }
        return info if info else False
