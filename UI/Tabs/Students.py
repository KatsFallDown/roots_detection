import re

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QTableWidgetItem)

from gasket import Gasket


class Students:
    def __init__(self,mainwindow, gasket: Gasket):
        self.gasket = gasket
        self.mainwindow = mainwindow

    def create_student_dialog(self, title, existing_classes, initial_data=None):
        """
        Создает диалог для добавления или редактирования ученика.

        :param title: Заголовок окна.
        :param existing_classes: Список существующих классов для выбора.
        :param initial_data: Словарь с начальными данными для редактирования (опционально).
        :return: Кортеж из диалогового окна и словаря виджетов ввода.
        """
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)

        # Поля ввода
        form_layout = QFormLayout()

        # Поле "ФИО"
        fio_input = QLineEdit(dialog)
        fio_input.setText(str(initial_data.get("ФИО", "")) if initial_data else "")
        form_layout.addRow("ФИО:", fio_input)

        # Комбобокс для выбора класса
        class_combobox = QComboBox(dialog)
        class_combobox.addItems(map(str, existing_classes))  # Преобразуем классы в строки
        if initial_data:
            class_combobox.setCurrentText(str(initial_data.get("Класс", "")))
        form_layout.addRow("Класс:", class_combobox)

        layout.addLayout(form_layout)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить", dialog)
        cancel_button = QPushButton("Отмена", dialog)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        # Обработчики кнопок
        save_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)

        # Возвращаем окно и виджеты для обработки данных
        return dialog, {
            "ФИО": fio_input,
            "Класс": class_combobox,
        }

    # def update_students(self):
    #     """Обновляет таблицу учеников с данными."""
    #     # Очищаем только содержимое ячеек, оставляя заголовки колонок нетронутыми
    #     self.mainwindow.ui.students_table.clearContents()
    #
    #     self.mainwindow.ui.students_table.setRowCount(len(self.mainwindow.students_data))
    #     for row, student_data in enumerate(self.mainwindow.students_data):
    #         self.mainwindow.ui.students_table.setItem(row, 0, QTableWidgetItem(student_data["ФИО"]))
    #         self.mainwindow.ui.students_table.setItem(row, 1, QTableWidgetItem(str(student_data["Класс"])))
    #         self.mainwindow.ui.students_table.setItem(row, 2, QTableWidgetItem(str(student_data["Выполненные ДЗ"])))
    #
    #     # Автоматическое подстраивание ширины столбцов
    #     self.mainwindow.ui.students_table.resizeColumnsToContents()

    def update_students(self):
        """Обновляет таблицу учеников с названиями выполненных ДЗ вместо их номеров, учитывая группу ДЗ класса."""
        self.mainwindow.ui.students_table.clearContents()
        self.mainwindow.ui.students_table.setRowCount(len(self.mainwindow.students_data))

        # Создаем словарь { (Группа ДЗ, Номер ДЗ): Название ДЗ } для быстрого поиска
        homework_dict = {(hw["Группа ДЗ"], hw["Номер"]): hw["Название"] for hw in self.mainwindow.homework_data}

        # Создаем словарь {Класс: Группа ДЗ}
        class_group_mapping = {cls["№"]: cls["Группа ДЗ"] for cls in self.mainwindow.classes_data}

        for row, student_data in enumerate(self.mainwindow.students_data):
            self.mainwindow.ui.students_table.setItem(row, 0, QTableWidgetItem(student_data["ФИО"]))
            self.mainwindow.ui.students_table.setItem(row, 1, QTableWidgetItem(str(student_data["Класс"])))

            # Определяем группу ДЗ, к которой относится класс ученика
            student_class = student_data["Класс"]
            student_group = class_group_mapping.get(student_class, None)

            # Преобразуем номера выполненных ДЗ в их названия, учитывая группу
            completed_hw_numbers = student_data["Выполненные ДЗ"]
            completed_hw_names = [
                homework_dict.get((student_group, hw_number), f"ДЗ {hw_number}")
                for hw_number in completed_hw_numbers
            ]

            # Отображаем список названий ДЗ через запятую
            self.mainwindow.ui.students_table.setItem(row, 2, QTableWidgetItem(", ".join(completed_hw_names)))

        # Автоматическое подстраивание ширины столбцов
        self.mainwindow.ui.students_table.resizeColumnsToContents()

    def open_add_student_dialog(self):
        """
        Открытие окна для добавления нового ученика.
        """
        try:
            # Создаем словарь {название класса: ID}, добавляем пустое значение для учеников без класса
            class_mapping = {"": None}
            class_mapping.update(
                {str(class_data["№"]): class_data["id"] for class_data in self.mainwindow.classes_data})

            # Получаем список существующих классов (отображаем пользователю только названия)
            existing_classes = list(class_mapping.keys())

            # Создаем окно добавления ученика
            dialog, inputs = self.create_student_dialog("Добавить ученика", existing_classes)

            while True:
                if dialog.exec():
                    # Извлекаем данные из виджетов
                    fio = inputs["ФИО"].text().strip()
                    class_number = inputs["Класс"].currentText()  # Получаем выбранный пользователем номер класса

                    # Проверка введенных данных
                    error = self.validate_student_data(fio, self.mainwindow.students_data, class_number)
                    if error:
                        QMessageBox.warning(self.mainwindow, "Ошибка", error)
                        continue  # Даем пользователю исправить данные

                    # Получаем ID класса (или None, если ученик без класса)
                    class_id = class_mapping.get(class_number, None)

                    # Добавляем ученика в данные
                    new_student = {
                        "ФИО": fio,
                        "Класс": class_number if class_id is not None else None,  # Сохраняем "Без класса" как None
                    }

                    # Отправка в базу данных
                    self.gasket.add_student(name=new_student["ФИО"], group_id=class_id)
                    self.mainwindow.data.load_initial_data()

                    QMessageBox.information(self.mainwindow, "Добавление ученика", "Ученик успешно добавлен!")
                    break
                else:
                    break
        except Exception as e:
            import traceback
            print("Ошибка при добавлении ученика:")
            traceback.print_exc()
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка:\n{str(e)}")

    def open_edit_student_dialog(self):
        """
        Открытие окна для редактирования ученика.
        """
        try:
            selected_row = self.mainwindow.ui.students_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите строку для редактирования.")
                return

            # Получаем данные текущего ученика
            student_data = self.mainwindow.students_data[selected_row]

            # Создаем словарь {Название класса: ID}, добавляем вариант "Без класса"
            class_mapping = {"": None}
            class_mapping.update(
                {str(class_data["№"]): class_data["id"] for class_data in self.mainwindow.classes_data})


            # Получаем список классов для выпадающего списка
            existing_classes = list(class_mapping.keys())

            # Определяем ID класса по названию (если он есть в базе)
            class_number = student_data.get("Класс", None)  # Название класса (например, "10А")

            # Если класс не найден в списке, устанавливаем ""
            current_class_name = class_number if class_number in class_mapping else ""

            # Создаем окно редактирования ученика
            dialog, inputs = self.create_student_dialog(
                "Редактировать ученика", existing_classes, initial_data=student_data
            )

            # Устанавливаем текущий класс в выпадающий список
            inputs["Класс"].setCurrentText(current_class_name)

            while True:
                if dialog.exec():
                    # Считываем данные из полей ввода
                    fio = inputs["ФИО"].text().strip()
                    new_class_name = inputs["Класс"].currentText().strip()

                    # Проверка введенных данных
                    error = self.validate_student_data(fio, self.mainwindow.students_data, new_class_name)
                    if error:
                        QMessageBox.warning(self.mainwindow, "Ошибка", error)
                        continue  # Даем пользователю исправить данные

                    # Получаем новый ID класса (или None, если выбран "Без класса")
                    new_class_id = class_mapping.get(new_class_name, None)

                    # Обновляем данные ученика
                    student_data["ФИО"] = fio
                    student_data["Класс"] = new_class_name if new_class_id is not None else None

                    # Отправка обновленных данных в базу
                    self.gasket.update_student(student_id=student_data["id"], name=fio, class_id=new_class_id)
                    self.mainwindow.data.load_initial_data()

                    # Выводим сообщение об успешном редактировании
                    QMessageBox.information(self.mainwindow, "Редактирование ученика",
                                            "Данные ученика успешно обновлены!")
                    break
                else:
                    break
        except Exception as e:
            import traceback
            print("Ошибка при редактировании ученика:")
            traceback.print_exc()
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка:\n{str(e)}")

    def shadow_student(self):
        """Перемещает выбранного ученика в корзину и удаляет его из класса."""
        selected_row = self.mainwindow.ui.students_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите ученика для перемещения в корзину.")
            return

        # Получаем данные ученика
        student_data = self.mainwindow.students_data[selected_row]

        # Перемещаем ученика в корзину
        self.gasket.update_student(student_id = student_data["id"] , draft_status=True)
        self.mainwindow.data.load_initial_data()

        QMessageBox.information(self.mainwindow, "Перевод в корзину", "Ученик успешно перемещен в корзину.")


    def validate_student_data(self, fio, students_data, selected_class):
        """
        Проверка валидности данных нового ученика.
        Возвращает строку с ошибкой, если данные некорректны, иначе None.
        """
        # Проверка поля ФИО
        if not fio:
            return "Поле ФИО не может быть пустым!"

        if not re.match(r"^[А-ЯЁ][а-яё]+(?:[- ][А-ЯЁ][а-яё]+){1,2}$", fio):
            return "Поле ФИО должно содержать 2-3 слова, начинающихся с заглавной буквы и состоящих из букв!"

        # Проверка уникальности ФИО в рамках одного класса
        for student in students_data:
            if student["ФИО"] == fio and student.get("Класс") == selected_class:
                return f"Ученик с ФИО '{fio}' уже существует в этом классе!"

        return None  # Ошибок нет

