from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox

from UI.Design.autorization import Ui_Dialog  # Подключаем файл авторизации
from gasket import Gasket
from mainwindow import (SchoolApp)  # Подключаем главное окно


class AuthorizationWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.gasket = Gasket("http://94.241.140.18:8000")


        try:
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)

            # Подключение кнопки "Войти"
            self.ui.pushButton.clicked.connect(self.handle_login)

            # Отображение пароля (кнопка "глаз")
            self.ui.pushButton_2.clicked.connect(self.toggle_password_visibility)
            self.password_visible = False
            self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        except Exception as e:
            self.show_error("Ошибка инициализации", str(e))

    def handle_login(self):
        """Обработка входа пользователя."""
        try:

            login = self.ui.lineEdit.text().strip()
            password = self.ui.lineEdit_2.text().strip()

            request = self.gasket.login(login=login,
                                        password=password)

            # Проверка логина и пароля
            if request == -1:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

            else:
                QMessageBox.information(self, "Успех", f"Добро пожаловать, {request}!")
                self.open_main_window()

        except Exception as e:
            self.show_error("Ошибка входа", str(e))

    def open_main_window(self):
        """Открыть главное окно и закрыть авторизацию."""
        try:
            #teacher_info = self.teacher_data[login]  # Данные преподавателя

            self.mainwindow = SchoolApp(self.gasket)  # Передаем данные преподавателя
            self.mainwindow.show()
            self.close()  # Закрываем окно авторизации
        except Exception as e:
            self.show_error("Ошибка открытия главного окна", str(e))


    def toggle_password_visibility(self):
        """Переключить видимость пароля."""
        try:
            if self.password_visible:
                self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            else:
                self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.password_visible = not self.password_visible
        except Exception as e:
            self.show_error("Ошибка отображения пароля", str(e))


    def show_error(self, title, message):
        """Показать сообщение об ошибке."""
        QMessageBox.critical(self, title, message)


if __name__ == "__main__":
    import sys
    try:
        app = QApplication(sys.argv)
        auth_window = AuthorizationWindow()
        auth_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Ошибка в главном блоке: {e}")