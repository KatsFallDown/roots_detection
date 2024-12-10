from tables import Teacher


class TeacherDB:
    def __init__(self, session):
        self.__session = session

    def add_one(self, first_name: str, second_name: str, login: str, password: str, tg_chat_token: int = None):
        if self.is_login_exist(login):
            new_teacher = Teacher(first_name=first_name.lower(),
                                  second_name=second_name.lower(),
                                  login=login,
                                  password=password,
                                  tg_chat_token=tg_chat_token)
            self.__session.add(new_teacher)
            self.__session.commit()
            return new_teacher.id

        return -1

    def is_login_exist(self, login):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            print('Такой пользователь уже существует')
            return False
        else:
            return True

    def head(self, value: int):
        teachers = self.__session.query(Teacher).limit(value).all()
        for teacher in teachers:
            print(teacher)

    def authenticate(self, login: str, password: str):
        teacher = self.__session.query(Teacher).filter_by(login=login, password=password).first()
        if teacher:
            print(f'Авторизация успешна! Добро пожаловать, {teacher.first_name} {teacher.second_name}!')
            return True
        else:
            print('Неверный логин или пароль. Попробуй снова!')
            return False

    def set_chat_token(self, login: str, token: int):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            teacher.tg_chat_token = token
            self.__session.commit()
            return True

        return False

    def set_first_name(self, login: str, first_name: str):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            teacher.first_name = first_name
            self.__session.commit()
            return True

        return False

    def set_second_name(self, login: str, second_name: str):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            teacher.second_name = second_name
            self.__session.commit()
            return True
        return False

    def set_login(self, login: str, new_login: str):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            teacher.login = new_login
            self.__session.commit()
            return True

        return False

    def set_password(self, login: str, old_password: str, new_password: str):
        teacher = self.__session.query(Teacher).filter_by(login=login).first()
        if teacher:
            if teacher.password == old_password:
                teacher.password = new_password
                self.__session.commit()
                return True

        return False

    def add_group(self, login: str, group_id: int):
        pass

    def remove_group(self, login: str, group_id: int):
        pass