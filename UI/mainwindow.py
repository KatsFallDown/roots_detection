from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QTableWidgetItem
from PyQt6.QtCore import Qt
from school import Ui_MainWindow

class SchoolApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Переменные для хранения данных
        self.classes_data = []
        self.groups_data = []
        self.homework_data = []
        self.students_data = []

        # Подключение кнопок к обработчикам
        self.ui.classes_pushButton_add.clicked.connect(self.open_add_class_dialog)
        self.ui.classes_pushButton_edit.clicked.connect(self.open_edit_class_dialog)
        self.ui.groups_pushButton_add.clicked.connect(self.open_add_group_dialog)
        self.ui.groups_pushButton_edit.clicked.connect(self.open_edit_group_dialog)
        self.ui.homework_pushButton_add.clicked.connect(self.open_add_homework_dialog)
        self.ui.homework_pushButton_edit.clicked.connect(self.open_edit_homework_dialog)
        self.ui.students_pushButton_add.clicked.connect(self.open_add_student_dialog)
        self.ui.students_pushButton_edit.clicked.connect(self.open_edit_student_dialog)

        self.load_initial_data()

        # Блокировка редактирования таблиц напрямую
        self.ui.classes_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.groups_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.homework_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.students_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    def load_initial_data(self):
        """Загрузка данных в таблицы при запуске приложения."""
        self.classes_data = [
            {"№": "9", "Группа ДЗ": "Python", "Классный руководитель": "Иван Иванов",
             "Ссылка на аккаунт классного руководителя в мессенджере": ""}
        ]
        self.groups_data = [
            {"Название группы": "Pro", "Примечание": "Для самых умных"}
        ]
        self.homework_data = [
            {"Название": "Задача 1", "Группа домашних работ": "Pro", "Тип": "Автопроверяемая", "Статус": "Черновик",
             "Методические рекомендации": "//методичка", "Входные данные для контестера": "28 42 56",
             "Выходные данные для контестера": ""}
        ]
        self.students_data = [
            {"ФИО": "Петр Петров", "Класс": "9", "Количество выполненных ДЗ": "5"}
        ]

        # Обновление таблиц с автоподстройкой ширины
        self.update_classes_table()
        self.update_groups_table()
        self.update_homework_table()
        self.update_students_table()

    def update_classes_table(self):
        """Обновляет таблицу классов с данными."""
        self.ui.classes_table.setRowCount(len(self.classes_data))
        for row, class_data in enumerate(self.classes_data):
            self.ui.classes_table.setItem(row, 0, QTableWidgetItem(class_data["№"]))
            self.ui.classes_table.setItem(row, 1, QTableWidgetItem(class_data["Группа ДЗ"]))
            self.ui.classes_table.setItem(row, 2, QTableWidgetItem(class_data["Классный руководитель"]))
            self.ui.classes_table.setItem(row, 3, QTableWidgetItem(class_data["Ссылка на аккаунт классного руководителя в мессенджере"]))

        # Автоматическое подстраивание ширины столбцов
        self.ui.classes_table.resizeColumnsToContents()

    def update_groups_table(self):
        """Обновляет таблицу групп с данными."""
        self.ui.groups_table.setRowCount(len(self.groups_data))
        for row, group_data in enumerate(self.groups_data):
            self.ui.groups_table.setItem(row, 0, QTableWidgetItem(group_data["Название группы"]))
            self.ui.groups_table.setItem(row, 1, QTableWidgetItem(group_data["Примечание"]))

        # Автоматическое подстраивание ширины столбцов
        self.ui.groups_table.resizeColumnsToContents()

    def update_homework_table(self):
        """Обновляет таблицу домашних заданий с данными."""
        self.ui.homework_table.setRowCount(len(self.homework_data))
        for row, homework_data in enumerate(self.homework_data):
            self.ui.homework_table.setItem(row, 0, QTableWidgetItem(homework_data["Название"]))
            self.ui.homework_table.setItem(row, 1, QTableWidgetItem(homework_data["Группа домашних работ"]))
            self.ui.homework_table.setItem(row, 2, QTableWidgetItem(homework_data["Тип"]))
            self.ui.homework_table.setItem(row, 3, QTableWidgetItem(homework_data["Статус"]))
            self.ui.homework_table.setItem(row, 4, QTableWidgetItem(homework_data["Методические рекомендации"]))
            self.ui.homework_table.setItem(row, 5, QTableWidgetItem(homework_data["Входные данные для контестера"]))
            self.ui.homework_table.setItem(row, 6, QTableWidgetItem(homework_data["Выходные данные для контестера"]))

        # Автоматическое подстраивание ширины столбцов
        self.ui.homework_table.resizeColumnsToContents()

    def update_students_table(self):
        """Обновляет таблицу учеников с данными."""
        self.ui.students_table.setRowCount(len(self.students_data))
        for row, student_data in enumerate(self.students_data):
            self.ui.students_table.setItem(row, 0, QTableWidgetItem(student_data["ФИО"]))
            self.ui.students_table.setItem(row, 1, QTableWidgetItem(student_data["Класс"]))
            self.ui.students_table.setItem(row, 2, QTableWidgetItem(student_data["Количество выполненных ДЗ"]))

        # Автоматическое подстраивание ширины столбцов
        self.ui.homework_table.resizeColumnsToContents()

    def open_add_class_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить класс", ["№", "Группа ДЗ", "Классный руководитель", "Ссылка на аккаунт классного руководителя в мессенджере"])
        if dialog.exec():
            new_class = {
                "№": inputs["№"].text(),
                "Группа ДЗ": inputs["Группа ДЗ"].text(),
                "Классный руководитель": inputs["Классный руководитель"].text(),
                "Ссылка на аккаунт классного руководителя в мессенджере": inputs["Ссылка на аккаунт классного руководителя в мессенджере"].text()
            }
            self.classes_data.append(new_class)
            self.update_classes_table()
            QMessageBox.information(self, "Добавление класса", "Класс добавлен успешно!")

    def open_edit_class_dialog(self):
        selected_row = self.ui.classes_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        if selected_row >= len(self.classes_data):
            QMessageBox.warning(self, "Редактирование", "Вы выбрали пустую строку.")
            return

        class_data = self.classes_data[selected_row]
        dialog, inputs = self.create_input_dialog("Редактировать класс", ["№", "Группа ДЗ", "Классный руководитель", "Ссылка на аккаунт классного руководителя в мессенджере"])

        # Заполнение текущих значений
        inputs["№"].setText(class_data["№"])
        inputs["Группа ДЗ"].setText(class_data["Группа ДЗ"])
        inputs["Классный руководитель"].setText(class_data["Классный руководитель"])
        inputs["Ссылка на аккаунт классного руководителя в мессенджере"].setText(class_data["Ссылка на аккаунт классного руководителя в мессенджере"])

        if dialog.exec():
            updated_class = {
                "№": inputs["№"].text(),
                "Группа ДЗ": inputs["Группа ДЗ"].text(),
                "Классный руководитель": inputs["Классный руководитель"].text(),
                "Ссылка на аккаунт классного руководителя в мессенджере": inputs["Ссылка на аккаунт классного руководителя в мессенджере"].text()
            }
            self.classes_data[selected_row] = updated_class
            self.update_classes_table()
            QMessageBox.information(self, "Редактирование класса", "Класс обновлен успешно!")

    def open_add_group_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить группу", ["Название группы", "Примечание"])
        if dialog.exec():
            new_group = {
                "Название группы": inputs["Название группы"].text(),
                "Примечание": inputs["Примечание"].text()
            }
            self.groups_data.append(new_group)
            self.update_groups_table()
            QMessageBox.information(self, "Добавление группы", "Группа добавлена успешно!")

    def open_edit_group_dialog(self):
        selected_row = self.ui.groups_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        if selected_row >= len(self.groups_data):
            QMessageBox.warning(self, "Редактирование", "Вы выбрали пустую строку.")
            return

        group_data = self.groups_data[selected_row]
        dialog, inputs = self.create_input_dialog("Редактировать группу", ["Название группы", "Примечание"])

        # Заполнение текущих значений
        inputs["Название группы"].setText(group_data["Название группы"])
        inputs["Примечание"].setText(group_data["Примечание"])

        if dialog.exec():
            updated_group = {
                "Название группы": inputs["Название группы"].text(),
                "Примечание": inputs["Примечание"].text()
            }
            self.groups_data[selected_row] = updated_group
            self.update_groups_table()
            QMessageBox.information(self, "Редактирование группы", "Группа обновлена успешно!")

    def open_add_homework_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить домашнее задание", ["Название", "Группа домашних работ", "Тип", "Статус", "Методические рекомендации", "Входные данные для контестера", "Выходные данные для контестера"])
        if dialog.exec():
            new_homework = {
                "Название": inputs["Название"].text(),
                "Группа домашних работ": inputs["Группа домашних работ"].text(),
                "Тип": inputs["Тип"].text(),
                "Статус": inputs["Статус"].text(),
                "Методические рекомендации": inputs["Методические рекомендации"].text(),
                "Входные данные для контестера": inputs["Входные данные для контестера"].text(),
                "Выходные данные для контестера": inputs["Выходные данные для контестера"].text()
            }
            self.homework_data.append(new_homework)
            self.update_homework_table()
            QMessageBox.information(self, "Добавление ДЗ", "Домашнее задание добавлено успешно!")

    def open_edit_homework_dialog(self):
        selected_row = self.ui.homework_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        if selected_row >= len(self.homework_data):
            QMessageBox.warning(self, "Редактирование", "Вы выбрали пустую строку.")
            return

        homework_data = self.homework_data[selected_row]
        dialog, inputs = self.create_input_dialog("Редактировать домашнее задание",
                                                  ["Название", "Группа домашних работ", "Тип", "Статус",
                                                   "Методические рекомендации", "Входные данные для контестера",
                                                   "Выходные данные для контестера"])

        # Заполнение текущих значений
        inputs["Название"].setText(homework_data["Название"])
        inputs["Группа домашних работ"].setText(homework_data["Группа домашних работ"])
        inputs["Тип"].setText(homework_data["Тип"])
        inputs["Статус"].setText(homework_data["Статус"])
        inputs["Методические рекомендации"].setText(homework_data["Методические рекомендации"])
        inputs["Входные данные для контестера"].setText(homework_data["Входные данные для контестера"])
        inputs["Выходные данные для контестера"].setText(homework_data["Выходные данные для контестера"])

        if dialog.exec():
            updated_homework = {
                "Название": inputs["Название"].text(),
                "Группа домашних работ": inputs["Группа домашних работ"].text(),
                "Тип": inputs["Тип"].text(),
                "Статус": inputs["Статус"].text(),
                "Методические рекомендации": inputs["Методические рекомендации"].text(),
                "Входные данные для контестера": inputs["Входные данные для контестера"].text(),
                "Выходные данные для контестера": inputs["Выходные данные для контестера"].text()
            }
            self.homework_data[selected_row] = updated_homework
            self.update_homework_table()
            QMessageBox.information(self, "Редактирование ДЗ", "Домашнее задание обновлено успешно!")

    def open_add_student_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить ученика", ["ФИО", "Класс", "Количество выполненных ДЗ"])
        if dialog.exec():
            new_student = {
                "ФИО": inputs["ФИО"].text(),
                "Класс": inputs["Класс"].text(),
                "Количество выполненных ДЗ": inputs["Количество выполненных ДЗ"].text()
            }
            self.students_data.append(new_student)
            self.update_students_table()
            QMessageBox.information(self, "Добавление ученика", "Ученик добавлен успешно!")

    def open_edit_student_dialog(self):
        selected_row = self.ui.students_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        if selected_row >= len(self.students_data):
            QMessageBox.warning(self, "Редактирование", "Вы выбрали пустую строку.")
            return

        student_data = self.students_data[selected_row]
        dialog, inputs = self.create_input_dialog("Редактировать ученика",
                                                  ["ФИО", "Класс", "Количество выполненных ДЗ"])

        # Заполнение текущих значений
        inputs["ФИО"].setText(student_data["ФИО"])
        inputs["Класс"].setText(student_data["Класс"])
        inputs["Количество выполненных ДЗ"].setText(student_data["Количество выполненных ДЗ"])

        if dialog.exec():
            updated_student = {
                "ФИО": inputs["ФИО"].text(),
                "Класс": inputs["Класс"].text(),
                "Количество выполненных ДЗ": inputs["Количество выполненных ДЗ"].text()
            }
            self.students_data[selected_row] = updated_student
            self.update_students_table()
            QMessageBox.information(self, "Редактирование ученика", "Информация об ученике обновлена успешно!")

    def create_input_dialog(self, title, fields):
        """Создает диалоговое окно с полями ввода."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)

        layout = QFormLayout(dialog)

        inputs = {}
        for field in fields:
            input_field = QLineEdit(dialog)
            layout.addRow(QLabel(field), input_field)
            inputs[field] = input_field

        buttons_layout = QVBoxLayout()
        submit_button = QPushButton("Сохранить", dialog)
        cancel_button = QPushButton("Отмена", dialog)
        buttons_layout.addWidget(submit_button)
        buttons_layout.addWidget(cancel_button)

        submit_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        layout.addRow(buttons_layout)
        dialog.setLayout(layout)

        return dialog, inputs

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SchoolApp()
    window.show()
    sys.exit(app.exec())