from PyQt6.QtCore import QDateTime

from gasket import Gasket


class Data:
    def __init__(self, gasket: Gasket, main_window):
        self.gasket = gasket
        self.mainwindow = main_window


    def load_initial_data(self):
        """Загрузка данных в таблицы при запуске приложения."""

        # Устанавливаем ФИО преподавателя
        teacher_info = self.gasket.get_teacher_info()
        fio = teacher_info.get("fio", "Неизвестный преподаватель")
        self.mainwindow.ui.teacher_label_name.setText(fio)

        # Устанавливаем количество классов и групп домашних работ
        classes = teacher_info.get("classes", [])
        homework_groups = teacher_info.get("homework_group")
        self.mainwindow.ui.teacher_label_numclasses.setText(f"Количество классов: {len(classes)}")
        self.mainwindow.ui.teacher_label_numgroups.setText(f"Количество групп ДЗ: {homework_groups}")

        self.mainwindow.classes_data = self.gasket.get_classes()
        self.mainwindow.groups_data = self.gasket.get_groups()
        self.mainwindow.homework_data = self.gasket.get_homework()
        self.mainwindow.students_data = self.gasket.get_students()
        self.gasket.get_students()
        self.mainwindow.trash_data = self.gasket.get_trash()

        # Обновление таблиц
        self.mainwindow.teacher.update_teacher_classes(classes)
        self.mainwindow.classes.update_classes()
        self.mainwindow.homework_groups.update_groups()
        self.mainwindow.homeworks.update_homework()
        self.mainwindow.students.update_students()
        self.mainwindow.basket.update_trash()


        # Обновляем время в статус-баре
        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        self.mainwindow.last_updated_label.setText(f"Последнее обновление: {current_time}")