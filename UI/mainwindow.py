from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QTableWidgetItem
from school import Ui_MainWindow

class SchoolApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключение кнопок к обработчикам
        self.ui.classes_pushButton_add.clicked.connect(self.open_add_class_dialog)
        self.ui.groups_pushButton_add.clicked.connect(self.open_add_group_dialog)
        self.ui.homework_pushButton_add.clicked.connect(self.open_add_homework_dialog)
        self.ui.students_pushButton_add.clicked.connect(self.open_add_student_dialog)

        self.load_initial_data()

    def load_initial_data(self):
        """Загрузка данных в таблицы при запуске приложения."""
        self.ui.classes_table.setRowCount(3)  # Количество строк
        self.ui.classes_table.setItem(0, 0, QTableWidgetItem("9"))
        self.ui.classes_table.setItem(0, 1, QTableWidgetItem("Математика"))
        self.ui.classes_table.setItem(0, 2, QTableWidgetItem("Иван Иванов"))

    def open_add_class_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить класс", ["№", "Группа ДЗ", "Классный руководитель"])
        if dialog.exec():
            row_position = self.ui.classes_table.rowCount()
            self.ui.classes_table.insertRow(row_position)
            self.ui.classes_table.setItem(row_position, 0, QTableWidgetItem(inputs["№"].text()))
            self.ui.classes_table.setItem(row_position, 1, QTableWidgetItem(inputs["Группа ДЗ"].text()))
            self.ui.classes_table.setItem(row_position, 2, QTableWidgetItem(inputs["Классный руководитель"].text()))
            QMessageBox.information(self, "Добавление класса", "Класс добавлен успешно!")

    def open_add_group_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить группу", ["Название группы", "Примечание"])
        if dialog.exec():
            row_position = self.ui.groups_table.rowCount()
            self.ui.groups_table.insertRow(row_position)
            self.ui.groups_table.setItem(row_position, 0, QTableWidgetItem(inputs["Название группы"].text()))
            self.ui.groups_table.setItem(row_position, 1, QTableWidgetItem(inputs["Примечание"].text()))
            QMessageBox.information(self, "Добавление группы", "Группа добавлена успешно!")

    def open_add_homework_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить домашнее задание", ["№", "Название", "Группа домашних работ", "Статус", "Методические рекомендации", "Входные данные для контестера", "Выходные данные для контестера"])
        if dialog.exec():
            row_position = self.ui.homework_table.rowCount()
            self.ui.homework_table.insertRow(row_position)
            self.ui.homework_table.setItem(row_position, 0, QTableWidgetItem(inputs["№"].text()))
            self.ui.homework_table.setItem(row_position, 1, QTableWidgetItem(inputs["Название"].text()))
            self.ui.homework_table.setItem(row_position, 2, QTableWidgetItem(inputs["Группа домашних работ"].text()))
            self.ui.homework_table.setItem(row_position, 3, QTableWidgetItem(inputs["Статус"].text()))
            self.ui.homework_table.setItem(row_position, 4, QTableWidgetItem(inputs["Методические рекомендации"].text()))
            self.ui.homework_table.setItem(row_position, 5, QTableWidgetItem(inputs["Выходные данные для контестера"].text()))
            QMessageBox.information(self, "Добавление ДЗ", "Домашнее задание добавлено успешно!")

    def open_add_student_dialog(self):
        dialog, inputs = self.create_input_dialog("Добавить ученика", ["ФИО", "Класс", "Номер телефона","Ссылка на аккаунт в мессенджере",])
        if dialog.exec():
            row_position = self.ui.students_table.rowCount()
            self.ui.students_table.insertRow(row_position)
            self.ui.students_table.setItem(row_position, 0, QTableWidgetItem(inputs["ФИО"].text()))
            self.ui.students_table.setItem(row_position, 1, QTableWidgetItem(inputs["Класс"].text()))
            self.ui.students_table.setItem(row_position, 2, QTableWidgetItem(inputs["Номер телефона"].text()))
            self.ui.students_table.setItem(row_position, 3, QTableWidgetItem(inputs["Ссылка на аккаунт в мессенджере"].text()))
            QMessageBox.information(self, "Добавление ученика", "Ученик добавлен успешно!")

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
