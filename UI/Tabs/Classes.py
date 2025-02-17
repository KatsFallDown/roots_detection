import re

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QTableWidgetItem, QFileDialog, QTextBrowser)

from gasket import Gasket


class Classes:
    def __init__(self,mainwindow, gasket: Gasket):
        self.gasket = gasket
        self.mainwindow = mainwindow


    def create_class_dialog(self, title, dz_groups, existing_data=None):
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        inputs = {
            "№": QLineEdit(dialog),
            "Классный руководитель": QLineEdit(dialog),
            "Ссылка на аккаунт классного руководителя в мессенджере": QLineEdit(dialog),
            "Группа ДЗ": QComboBox(dialog),
            "Список учеников": QTextEdit(dialog),
        }

        inputs["Группа ДЗ"].addItems(dz_groups)

        if existing_data:
            inputs["№"].setText(existing_data["№"])
            inputs["Классный руководитель"].setText(existing_data["Классный руководитель"])
            inputs["Ссылка на аккаунт классного руководителя в мессенджере"].setText(
                existing_data["Ссылка на аккаунт классного руководителя в мессенджере"]
            )
            inputs["Группа ДЗ"].setCurrentText(existing_data["Группа ДЗ"])
            inputs["Список учеников"].setText(existing_data["Список учеников"])

        form_layout.addRow("№ Класса:", inputs["№"])
        form_layout.addRow("Классный руководитель:", inputs["Классный руководитель"])
        form_layout.addRow("Ссылка на аккаунт классного руководителя в мессенджере:",
                           inputs["Ссылка на аккаунт классного руководителя в мессенджере"])
        form_layout.addRow("Группа ДЗ:", inputs["Группа ДЗ"])
        form_layout.addRow("Список учеников:", inputs["Список учеников"])
        layout.addLayout(form_layout)

        # Кнопка для загрузки
        load_button = QPushButton("Загрузить список учеников из файла", dialog)
        load_button.setObjectName("Загрузить список учеников из файла")  # Добавлено
        load_button.clicked.connect(lambda: self.load_students_from_file(inputs["Список учеников"]))
        layout.addWidget(load_button)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить", dialog)
        save_button.setObjectName("Сохранить")  # Добавлено
        cancel_button = QPushButton("Отмена", dialog)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        save_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        return dialog, inputs

    def create_update_class_dialog(self, title, dz_groups, existing_data=None):
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        inputs = {
            "№": QLineEdit(dialog),
            "Классный руководитель": QLineEdit(dialog),
            "Ссылка на аккаунт классного руководителя в мессенджере": QLineEdit(dialog),
            "Группа ДЗ": QComboBox(dialog),
            "Список учеников": QTextEdit(dialog),
        }

        inputs["Группа ДЗ"].addItems(dz_groups)

        if existing_data:
            inputs["№"].setText(existing_data["№"])
            inputs["Классный руководитель"].setText(existing_data["Классный руководитель"])
            inputs["Ссылка на аккаунт классного руководителя в мессенджере"].setText(
                existing_data["Ссылка на аккаунт классного руководителя в мессенджере"]
            )
            inputs["Группа ДЗ"].setCurrentText(existing_data["Группа ДЗ"])
            inputs["Список учеников"].setText(existing_data["Список учеников"])

        form_layout.addRow("№ Класса:", inputs["№"])
        form_layout.addRow("Классный руководитель:", inputs["Классный руководитель"])
        form_layout.addRow("Ссылка на аккаунт классного руководителя в мессенджере:",
                           inputs["Ссылка на аккаунт классного руководителя в мессенджере"])
        form_layout.addRow("Группа ДЗ:", inputs["Группа ДЗ"])
        form_layout.addRow("Список учеников:", inputs["Список учеников"])
        layout.addLayout(form_layout)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить", dialog)
        save_button.setObjectName("Сохранить")  # Добавлено
        cancel_button = QPushButton("Отмена", dialog)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        save_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        return dialog, inputs

    def update_classes(self):
        """Обновляет таблицу классов с данными."""
        self.mainwindow.ui.classes_table.clearContents()
        self.mainwindow.ui.classes_table.setRowCount(len(self.mainwindow.classes_data))
        for row, class_data in enumerate(self.mainwindow.classes_data):
            self.mainwindow.ui.classes_table.setItem(row, 0, QTableWidgetItem(str(class_data["№"])))
            self.mainwindow.ui.classes_table.setItem(row, 1, QTableWidgetItem(class_data["Группа ДЗ"]))

            # Проверяем наличие студентов в классе
            if class_data["Список учеников"]:
                # Если есть студенты, добавляем кнопку "Просмотреть список"
                view_button = QPushButton("Просмотреть список", self.mainwindow.ui.classes_table)
                view_button.clicked.connect(lambda checked, r=row: self.open_view_students_dialog(r))
                self.mainwindow.ui.classes_table.setCellWidget(row, 2, view_button)
            else:
                # Если студентов нет, отображаем текст "Пусто"
                self.mainwindow.ui.classes_table.setItem(row, 2, QTableWidgetItem("Пусто"))

            self.mainwindow.ui.classes_table.setItem(row, 3, QTableWidgetItem(class_data["Классный руководитель"]))
            self.mainwindow.ui.classes_table.setItem(
                row, 4, QTableWidgetItem(class_data["Ссылка на аккаунт классного руководителя в мессенджере"])
            )
        self.mainwindow.ui.classes_table.resizeColumnsToContents()
        self.mainwindow.ui.classes_table.resizeRowsToContents()


    def open_add_class_dialog(self):
        """
        Открытие диалогового окна для добавления нового класса.
        В случае ошибки введенные данные сохраняются в полях.
        """
        try:
            # Создаем словарь {название группы: ID}, добавляем пустое значение для класса без группы
            homework_group_mapping = {"": None}
            homework_group_mapping.update(
                {str(groups_data["Название группы"]): groups_data["id"] for groups_data in self.mainwindow.groups_data})

            # Получаем список существующих классов (отображаем пользователю только названия)
            existing_groups = list(homework_group_mapping.keys())

            # Создаем диалог и вводимые поля
            dialog, inputs = self.create_class_dialog("Добавить класс", existing_groups)

            # Запускаем диалог и обрабатываем данные
            while True:
                if dialog.exec():
                    # Извлекаем данные из полей
                    new_class = {
                        "№": inputs["№"].text(),
                        "Группа ДЗ": inputs["Группа ДЗ"].currentText(),
                        "Список учеников": inputs["Список учеников"].toPlainText(),
                        "Классный руководитель": inputs["Классный руководитель"].text(),
                        "Ссылка на аккаунт классного руководителя в мессенджере": inputs[
                            "Ссылка на аккаунт классного руководителя в мессенджере"
                        ].text(),
                    }

                    # Преобразуем список учеников

                    new_class["Список учеников"] = [
                        student.strip() for student in new_class["Список учеников"].split("\n") if student.strip()
                    ]

                    # Проверяем данные
                    error = self.validate_class_data(new_class)
                    if error:
                        QMessageBox.warning(self.mainwindow, "Ошибка данных", error)
                        # Данные остаются в полях, даем возможность их исправить
                        continue



                    # Получаем ID группы ДЗ (или None, если класс без группы)
                    groups_id = homework_group_mapping.get(new_class["Группа ДЗ"], None)

                    class_id = self.gasket.add_class(number=new_class["№"],
                                          teacher=new_class["Классный руководитель"],
                                          link=new_class[ "Ссылка на аккаунт классного руководителя в мессенджере"],
                                          homework_group= groups_id)

                    for student_name in new_class["Список учеников"]:
                        new_student = {"ФИО": student_name, "Класс": class_id, "Количество выполненных ДЗ": "0"}
                        self.gasket.add_student(name= new_student["ФИО"], group_id=new_student["Класс"] )
                    self.mainwindow.data.load_initial_data()

                    QMessageBox.information(self.mainwindow, "Добавление класса", "Класс и студенты добавлены успешно!")
                    break
                else:
                    # Нажата кнопка "Отмена", выходим
                    break
        except Exception as e:
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка: {str(e)}")

    def open_edit_class_dialog(self):
        """
        Открытие диалогового окна для редактирования класса.
        В случае ошибки введенные данные сохраняются в полях.
        """
        selected_row = self.mainwindow.ui.classes_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.mainwindow, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        class_data = self.mainwindow.classes_data[selected_row]  # Получаем данные класса для редактирования

        # Создаем словарь {название группы: ID}, добавляем пустое значение для класса без группы
        homework_group_mapping = {"": None}
        homework_group_mapping.update(
            {str(groups_data["Название группы"]): groups_data["id"] for groups_data in self.mainwindow.groups_data})

        # Получаем список существующих групп (отображаем пользователю только названия)
        existing_groups = list(homework_group_mapping.keys())

        # Определяем ID группы по названию (если она есть в базе)
        group = class_data.get("Группа ДЗ", None)  # Название класса (например, "10А")

        # Если группа не найдена в списке, устанавливаем ""
        current_group_name = group if group in homework_group_mapping else ""

        try:

            # Преобразование данных класса для передачи в диалог
            existing_data = {
                "№": str(class_data["№"]),
                "Группа ДЗ": current_group_name,
                "Список учеников": "\n".join(class_data["Список учеников"]),
                "Классный руководитель": class_data.get("Классный руководитель", ""),
                "Ссылка на аккаунт классного руководителя в мессенджере": class_data.get(
                    "Ссылка на аккаунт классного руководителя в мессенджере", ""
                ),
            }

            dialog, inputs = self.create_update_class_dialog("Редактировать класс", existing_groups, existing_data=existing_data)
            # --- Блокируем редактирование старых учеников ---
            inputs["Список учеников"].setReadOnly(True)  # Не разрешаем ввод новых имен

            while True:
                if dialog.exec():
                    # Извлекаем обновленные данные из полей
                    updated_class = {
                        "id": class_data["id"],
                        "№": inputs["№"].text(),
                        "Группа ДЗ": inputs["Группа ДЗ"].currentText(),
                        "Классный руководитель": inputs["Классный руководитель"].text(),
                        "Ссылка на аккаунт классного руководителя в мессенджере": inputs[
                            "Ссылка на аккаунт классного руководителя в мессенджере"
                        ].text(),
                    }

                    # Проверяем данные
                    error = self.validate_class_data(updated_class, exclude_row=selected_row)
                    if error:
                        QMessageBox.warning(self.mainwindow, "Ошибка данных", error)
                        # Данные остаются в полях, даем возможность их исправить
                        continue

                     # Получаем новый ID класса (или None, если выбран "Без класса")
                    new_group_id = homework_group_mapping.get(updated_class["Группа ДЗ"], None)

                    # Обновляем данные класса
                    self.gasket.update_class(class_id= updated_class["id"] ,
                                             number= updated_class["№"],
                                             teacher= updated_class["Классный руководитель"],
                                             link= updated_class["Ссылка на аккаунт классного руководителя в мессенджере"],
                                             homework_group= new_group_id)
                    self.mainwindow.data.load_initial_data()



                    QMessageBox.information(self.mainwindow, "Редактирование класса", "Класс и студенты обновлены успешно!")
                    break
                else:
                    # Нажата кнопка "Отмена", выходим
                    break

        except Exception as e:
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка при редактировании класса:\n{str(e)}")


    def open_view_students_dialog(self, row):
        """
        Открывает новое окно для просмотра списка учеников класса.
        :param row: Индекс строки таблицы классов.
        """
        try:
            class_data = self.mainwindow.classes_data[row]

            # Получаем номер класса
            class_number = str(class_data['№'])

            # Создаем новое окно
            dialog = QDialog(self.mainwindow)
            dialog.setWindowTitle(f"Просмотр списка учеников для класса №{class_number}")
            dialog.setModal(True)

            # Макет окна
            layout = QVBoxLayout(dialog)

            # Поля для отображения данных
            layout.addWidget(QLabel(f"<b>Класс №:</b> {class_number}"))
            layout.addWidget(
                QLabel(f"<b>Классный руководитель:</b> {class_data.get('Классный руководитель', 'Не указан')}"))
            layout.addWidget(QLabel(
                f"<b>Ссылка на мессенджер:</b> {class_data.get('Ссылка на аккаунт классного руководителя в мессенджере', 'Не указана')}"))
            layout.addWidget(QLabel(f"<b>Группа ДЗ:</b> {class_data.get('Группа ДЗ', 'Не указана')}"))

            # Список учеников, которые действительно принадлежат этому классу
            students_in_class = []

            # Добавляем только тех студентов, у которых класс не изменился
            for student in self.mainwindow.students_data:
                if str(student["Класс"]) == class_number:
                    students_in_class.append(student["ФИО"])

            # Преобразуем список учеников в строку с разделением по строкам
            students_text = "\n".join(students_in_class) if students_in_class else "Нет учеников в классе."

            # Отображение списка учеников
            student_list = QTextEdit(dialog)
            student_list.setPlainText(students_text)
            student_list.setReadOnly(True)
            layout.addWidget(QLabel("<b>Список учеников:</b>"))
            layout.addWidget(student_list)

            # Кнопка закрытия
            close_button = QPushButton("Закрыть", dialog)
            close_button.clicked.connect(dialog.close)
            layout.addWidget(close_button)

            # Устанавливаем макет и открываем окно
            dialog.setLayout(layout)
            dialog.exec()
        except Exception as e:
            import traceback
            print("Ошибка при просмотре списка учеников:")
            traceback.print_exc()
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка:\n{str(e)}")

    def shadow_class(self):
        """
        Перемещает выбранный класс и, при необходимости, его учеников в корзину.
        """
        try:
            selected_row = self.mainwindow.ui.classes_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите класс для перемещения в корзину.")
                return

            if selected_row >= len(self.mainwindow.classes_data):
                QMessageBox.warning(self.mainwindow, "Ошибка", "Выбрана пустая строка.")
                return

            # Получаем данные класса
            class_data = self.mainwindow.classes_data[selected_row]

            # Создаем диалог подтверждения с пользовательскими кнопками
            confirm_dialog = QMessageBox(self.mainwindow)
            confirm_dialog.setIcon(QMessageBox.Icon.Question)
            confirm_dialog.setWindowTitle("Перевод в корзину")
            confirm_dialog.setText("Вы хотите переместить только класс или класс и учеников?")

            # Создаем кнопки вручную
            only_class_button = confirm_dialog.addButton("Только класс", QMessageBox.ButtonRole.YesRole)
            class_and_students_button = confirm_dialog.addButton("Класс и учеников", QMessageBox.ButtonRole.NoRole)
            cancel_button = confirm_dialog.addButton(QMessageBox.StandardButton.Cancel)

            # Запускаем диалог и получаем результат
            confirm_dialog.exec()
            clicked_button = confirm_dialog.clickedButton()

            if clicked_button == cancel_button:
                return

            if clicked_button==only_class_button:
                # Удаляем класс из данных и добавляем его в корзину
                self.gasket.update_class(class_id= class_data["id"], draft_status= True)
                self.mainwindow.data.load_initial_data()
                QMessageBox.information(self.mainwindow, "Перевод в корзину", "Класс успешно перемещен в корзину.")

            # Если выбрано "Класс и учеников", добавляем учеников в корзину
            if clicked_button == class_and_students_button:

                students_to_remove = [student for student in self.mainwindow.students_data if student["Класс"] == class_data["№"]]
                for student in students_to_remove:
                    self.gasket.update_student(student_id= student["id"], draft_status= True)

                self.gasket.update_class(class_id=class_data["id"], draft_status=True)
                self.mainwindow.data.load_initial_data()
                QMessageBox.information(self.mainwindow, "Перевод в корзину",
                                        "Класс и ученики этого класса успешно перемещен в корзину.")

        except IndexError:
            QMessageBox.critical(self.mainwindow, "Ошибка", "Возникла проблема с выбором строки.")
        except Exception as e:
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка: {str(e)}")




    def validate_class_data(self, data, exclude_row=None):
        """
        Проверка данных для класса школьников.
        """

        # Проверка формата номера класса ("10А", "7Б")
        if not re.match(r"^(?:[1-9]|10|11)[А-ЯЁ]$", data["№"]):
            return "Номер класса должен состоять из числа (1-11) и буквы (А-Я)."

        # Проверка уникальности номера класса
        if not self.is_unique_class_number(data["№"], exclude_row=exclude_row):
            return "Класс с таким номером уже существует!"

        # Проверка ФИО классного руководителя (опционально)
        if "Классный руководитель" in data and data["Классный руководитель"].strip():
            if not self.is_valid_fio(data["Классный руководитель"]):
                return "Некорректное ФИО классного руководителя. Оно должно содержать фамилию и имя, отчество — опционально."

        # Проверка списка учеников
        if "Список учеников" in data:
            if isinstance(data["Список учеников"], list):
                seen_students = set()  # Множество для хранения уже встречавшихся учеников
                for student in data["Список учеников"]:
                    if not self.is_valid_fio(student):
                        return f"Некорректное ФИО ученика: {student}. ФИО должно содержать фамилию и имя, отчество — опционально."

                    # Проверяем, есть ли ученик уже в другом классе
                    existing_class = self.find_student_class(student)
                    if existing_class and existing_class != data["№"]:
                        return f"Ошибка: Ученик {student} уже числится в классе {existing_class}!"

                    # Проверяем на дубликаты в этом же классе
                    if student in seen_students:
                        return f"Ошибка: Ученик {student} уже добавлен в этот класс!"
                    seen_students.add(student)

            else:
                return "Список учеников должен быть передан в виде списка строк."

        return None

    def is_valid_fio(self, fio):
        """
        Проверка корректности ФИО (Фамилия[-Фамилия] Имя[-Имя] [Отчество])
        """
        if not fio or not isinstance(fio, str):  # Проверяем, что fio — строка и не пустая
            return False

        pattern = r"^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)? [А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?( [А-ЯЁ][а-яё]+)?$"
        match = re.match(pattern, fio)
        is_valid = bool(match)
        return is_valid

    def find_student_class(self, student_fio):
        """
        Проверяет, в каком классе уже числится ученик.
        Если ученик найден, возвращает номер класса.
        Если не найден — возвращает None.
        """
        if not student_fio or not isinstance(student_fio, str):  # Проверяем, что передано ФИО
            return None

        for cls in self.mainwindow.classes_data:
            if "Список учеников" in cls and isinstance(cls["Список учеников"], list):
                if student_fio in cls["Список учеников"]:
                    return cls["№"]  # Ученик найден, возвращаем номер класса

        return None  # Ученик не найден

    def is_unique_class_number(self, class_number, exclude_row=None):
        """
        Проверка, что номер класса уникален.
        :param class_number: Проверяемый номер класса.
        :param exclude_row: Индекс строки, которую следует исключить из проверки (например, при редактировании).
        :return: True, если номер уникален, иначе False.
        """
        for row in range(self.mainwindow.ui.classes_table.rowCount()):
            if row == exclude_row:  # Игнорируем текущую строку
                continue
            existing_number = self.mainwindow.ui.classes_table.item(row, 0)
            if existing_number and existing_number.text() == str(class_number):
                return False
        return True

    def load_students_from_file(self, text_edit):
        """
        Загрузка списка студентов из текстового файла в поле ввода.
        """
        file_dialog = QFileDialog(self.mainwindow)
        file_path, _ = file_dialog.getOpenFileName(
            self.mainwindow,
            "Выберите текстовый файл с именами студентов",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    # Читаем список студентов из файла
                    students_from_file = file.read().splitlines()

                    # Получаем текущий список студентов из поля ввода
                    current_students = text_edit.toPlainText().splitlines()

                    # Объединяем оба списка, исключая дубликаты
                    updated_students = set(current_students) | set(students_from_file)

                    # Преобразуем обратно в строку с новыми студентами
                    updated_students_text = "\n".join(updated_students)

                    # Обновляем поле с новым списком студентов
                    text_edit.setPlainText(updated_students_text)

            except Exception as e:
                QMessageBox.critical(self.mainwindow, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
