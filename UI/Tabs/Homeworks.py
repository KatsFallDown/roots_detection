from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QTableWidgetItem, QFileDialog)
import traceback

from gasket import Gasket


class Homeworks:
    def __init__(self,mainwindow, gasket: Gasket):
        self.gasket = gasket
        self.mainwindow = mainwindow

    def create_homework_dialog(self, title, dz_groups, existing_data=None):
        """
        Создает диалоговое окно для добавления или редактирования домашнего задания.
        """
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        # Поле "Название"
        title_input = QLineEdit(dialog)
        title_input.setText(existing_data.get("Название", "") if existing_data else "")
        form_layout.addRow("Название:", title_input)

        # Комбобокс для выбора группы ДЗ
        dz_group_combobox = QComboBox(dialog)
        dz_group_combobox.addItems(dz_groups)
        if existing_data:
            dz_group_combobox.setCurrentText(existing_data.get("Группа ДЗ", ""))
        form_layout.addRow("Группа ДЗ:", dz_group_combobox)

        # Комбобокс для выбора статуса
        status_combobox = QComboBox(dialog)
        status_combobox.addItems(["Черновик", "Опубликована"])
        if existing_data:
            status_combobox.setCurrentText(existing_data.get("Статус", "Черновик"))
        form_layout.addRow("Статус:", status_combobox)

        # Поле "Входные данные контестера"
        input_data_input = QTextEdit(dialog)
        input_data_input.setPlaceholderText("Введите входные данные для контестера.")
        if existing_data:
            input_data_input.setText(existing_data.get("Входные данные для контестера", ""))
        form_layout.addRow("Входные данные для контестера:", input_data_input)

        # Поле "Выходные данные контестера"
        output_data_input = QTextEdit(dialog)
        output_data_input.setPlaceholderText("Введите выходные данные для контестера.")
        if existing_data:
            output_data_input.setText(existing_data.get("Выходные данные для контестера", ""))
        form_layout.addRow("Выходные данные для контестера:", output_data_input)

        # Блок загрузки методички
        methodic_file_path = existing_data.get("Методические рекомендации", "") if existing_data else ""

        methodic_status_label = QLabel(dialog)
        methodic_status_label.setText("Методичка: Загружена" if methodic_file_path else "Методичка: Не загружена")
        methodic_label= QTextEdit(dialog)

        upload_methodic_button = QPushButton("Загрузить методические рекомендации", dialog)

        def upload_methodic():
            nonlocal methodic_file_path
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(dialog, "Выберите файл методички", "",
                                                       "PDF файлы (*.pdf);;Все файлы (*)")
            if file_path:
                methodic_file_path = file_path
                methodic_label.setText(f"{methodic_file_path}")

        upload_methodic_button.clicked.connect(upload_methodic)

        form_layout.addRow("Методичка:", methodic_status_label)
        form_layout.addRow("Путь к файлу:", methodic_label)
        form_layout.addRow(upload_methodic_button)


        layout.addLayout(form_layout)

        # Проверка поля "Выходные данные для контестера" для статуса "Опубликована"
        def validate_status():
            if not output_data_input.toPlainText().strip():
                if status_combobox.currentText() == "Опубликована":
                    QMessageBox.warning(dialog, "Ошибка",
                                        "Статус 'Опубликована' можно установить только при заполнении поля 'Выходные данные для контестера'.")
                    status_combobox.setCurrentText("Черновик")

        output_data_input.textChanged.connect(validate_status)
        status_combobox.currentIndexChanged.connect(validate_status)

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
            "Название": title_input,
            "Группа ДЗ": dz_group_combobox,
            "Статус": status_combobox,
            "Методические рекомендации": methodic_label,
            "Входные данные для контестера": input_data_input,
            "Выходные данные для контестера": output_data_input,
        }

    def update_homework(self):
        """Обновляет таблицу домашних заданий с данными, включая статус методички."""
        self.mainwindow.ui.homework_table.clearContents()
        self.mainwindow.ui.homework_table.setRowCount(len(self.mainwindow.homework_data))

        for row, homework_data in enumerate(self.mainwindow.homework_data):
            self.mainwindow.ui.homework_table.setItem(row, 0, QTableWidgetItem(homework_data["Название"]))
            self.mainwindow.ui.homework_table.setItem(row, 1, QTableWidgetItem(homework_data["Группа ДЗ"]))
            self.mainwindow.ui.homework_table.setItem(row, 2, QTableWidgetItem(homework_data["Статус"]))

            # Проверяем наличие методички
            if homework_data.get("Методические рекомендации"):
                methodic_item = QTableWidgetItem("✅")  # Зеленая галочка
                methodic_item.setForeground(QBrush(QColor(0, 128, 0)))  # Зеленый цвет
            else:
                methodic_item = QTableWidgetItem("❌")  # Красный крестик
                methodic_item.setForeground(QBrush(QColor(255, 0, 0)))  # Красный цвет

            methodic_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем иконку
            self.mainwindow.ui.homework_table.setItem(row, 3, methodic_item)

            self.mainwindow.ui.homework_table.setItem(row, 4,
                                                      QTableWidgetItem(homework_data["Входные данные для контестера"]))
            self.mainwindow.ui.homework_table.setItem(row, 5,
                                                      QTableWidgetItem(homework_data["Выходные данные для контестера"]))

        # Автоматическое подстраивание ширины столбцов
        self.mainwindow.ui.homework_table.resizeColumnsToContents()

    def open_add_homework_dialog(self):
        """
        Открытие окна для добавления нового домашнего задания.
        """
        try:
            # Создаем словарь {название группы: ID}, добавляем пустое значение для дз без группы
            homework_group_mapping = {"": None}
            homework_group_mapping.update(
                {str(groups_data["Название группы"]): groups_data["id"] for groups_data in self.mainwindow.groups_data})

            # Получаем список существующих групп (отображаем пользователю только названия)
            existing_groups = list(homework_group_mapping.keys())
            # Получаем список групп ДЗ

            dialog, inputs = self.create_homework_dialog("Добавить домашнее задание", existing_groups)

            while True:
                if dialog.exec():
                    # Извлекаем данные из виджетов
                    homework_title = inputs["Название"].text()
                    if not homework_title.strip():  # Проверка на пустое название
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            "Название домашнего задания обязательно для заполнения.")
                        continue  # Продолжаем цикл, чтобы не закрывать диалог и позволить исправить ошибку



                    methodic_file_path = inputs["Методические рекомендации"].toPlainText()

                    if methodic_file_path:
                        methodic_file = open(methodic_file_path, "rb")
                    else: methodic_file = None

                    new_homework = {
                        "Название": homework_title,
                        "Группа ДЗ": inputs["Группа ДЗ"].currentText(),
                        "Статус": inputs["Статус"].currentText(),
                        "Методические рекомендации": methodic_file,
                        "Входные данные для контестера": inputs["Входные данные для контестера"].toPlainText(),
                        "Выходные данные для контестера": inputs["Выходные данные для контестера"].toPlainText(),
                    }

                    if not self.validate_homework(homework_title, new_homework["Группа ДЗ"]):
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            f"Домашнее задание '{homework_title}' уже существует в группе {new_homework['Группа ДЗ']}.")
                        continue  # Не даем продолжить создание, если такое ДЗ уже есть

                    # Получаем ID группы ДЗ (или None, если ДЗ без группы)
                    groups_id = homework_group_mapping.get(new_homework["Группа ДЗ"], None)
                    status=new_homework["Статус"]
                    if status== "Черновик":
                        draft_status= True
                    else: draft_status=False



                    # Добавляем домашнее задание в данные
                    self.gasket.add_homework(
                        name=new_homework["Название"],
                        input_data=new_homework["Входные данные для контестера"],
                        output_data=new_homework["Выходные данные для контестера"],
                        manual=methodic_file,
                        group_id=groups_id,
                        draft_status=draft_status

                    )

                    if methodic_file_path: methodic_file.close()

                    self.mainwindow.data.load_initial_data()

                    QMessageBox.information(self.mainwindow, "Добавление задания",
                                            "Домашнее задание успешно добавлено!")
                    break  # Выход из цикла, если данные введены корректно
                else:
                    break  # Если нажата кнопка "Отмена", выходим из цикла
        except Exception as e:
            # Показываем сообщение об ошибке
            QMessageBox.critical(self.mainwindow, "Ошибка",
                                 f"Произошла ошибка при добавлении домашнего задания:\n{str(e)}")

    def open_edit_homework_dialog(self):
        """
        Открытие окна для редактирования домашнего задания на основе выбранной строки в таблице.
        """
        selected_row = self.mainwindow.ui.homework_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Пожалуйста, выберите строку для редактирования.")
            return

        # Получаем данные домашнего задания из таблицы
        existing_homework = self.mainwindow.homework_data[selected_row]

        # Создаем словарь {название группы: ID}, добавляем пустое значение для класса без группы
        homework_group_mapping = {"": -1}
        homework_group_mapping.update(
            {str(groups_data["Название группы"]): groups_data["id"] for groups_data in self.mainwindow.groups_data})

        # Получаем список существующих групп (отображаем пользователю только названия)
        existing_groups = list(homework_group_mapping.keys())

        # Определяем ID группы по названию (если она есть в базе)
        group = existing_homework.get("Группа ДЗ", None)  # Название класса (например, "10А")

        # Если группа не найдена в списке, устанавливаем ""
        current_group_name = group if group in homework_group_mapping else ""


        while True:

            dialog, inputs = self.create_homework_dialog("Редактировать домашнее задание", existing_groups,
                                                         existing_homework)
            # Устанавливаем текущий класс в выпадающий список
            inputs["Группа ДЗ"].setCurrentText(current_group_name)


            if dialog.exec():
                # Извлекаем обновленные данные из виджетов
                homework_title = inputs["Название"].text()
                if not homework_title.strip():  # Проверка на пустое название
                    QMessageBox.warning(self.mainwindow, "Ошибка",
                                        "Название домашнего задания обязательно для заполнения.")
                    continue  # Продолжаем цикл, чтобы не закрывать диалог и позволить исправить ошибку

                methodic_file_path = inputs["Методические рекомендации"].toPlainText()

                if methodic_file_path:
                    methodic_file = open(methodic_file_path, "rb")
                else:
                    methodic_file = None

                updated_homework = {
                    "id": existing_homework["id"],
                    "Название": homework_title,
                    "Группа ДЗ": inputs["Группа ДЗ"].currentText(),
                    "Статус": inputs["Статус"].currentText(),
                    "Методические рекомендации": methodic_file,
                    "Входные данные для контестера": inputs["Входные данные для контестера"].toPlainText(),
                    "Выходные данные для контестера": inputs["Выходные данные для контестера"].toPlainText(),
                }

                if not self.validate_homework(homework_title, updated_homework["Группа ДЗ"], exclude_homework_id=existing_homework["id"]):
                    QMessageBox.warning(self.mainwindow, "Ошибка",
                                        f"Домашнее задание '{homework_title}' уже существует в группе {updated_homework['Группа ДЗ']}.")
                    continue  # Не даем продолжить создание, если такое ДЗ уже есть

                # Получаем новый ID класса (или None, если выбран "Без класса")
                new_group_id = homework_group_mapping.get(updated_homework["Группа ДЗ"], None)
                status = updated_homework["Статус"]
                if status == "Черновик":
                    draft_status = True
                else:
                    draft_status = False

                # Обновляем данные домашнего задания
                self.gasket.update_homework(
                    homework_id=updated_homework["id"],
                    name=updated_homework["Название"],
                    input_data=updated_homework["Входные данные для контестера"],
                    output_data=updated_homework["Выходные данные для контестера"],
                    manual=updated_homework["Методические рекомендации"],   # Добавляем методичку
                    group_id=new_group_id,
                    draft_status=draft_status
                )

                if methodic_file_path: methodic_file.close()

                self.mainwindow.data.load_initial_data()

                QMessageBox.information(self.mainwindow, "Редактирование задания",
                                        "Домашнее задание успешно обновлено!")
                break  # Выход из цикла, если данные введены корректно
            else:
                break  # Если нажата кнопка "Отмена", выходим из цикла

    def shadow_homework(self):
        """Перемещает выбранное ДЗ в корзину."""
        selected_row = self.mainwindow.ui.homework_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите ДЗ для перемещения в корзину.")
            return
        homework_data = self.mainwindow.homework_data[selected_row]

        self.gasket.update_homework(homework_id= homework_data["id"], is_deleted= True)
        self.mainwindow.data.load_initial_data()

        QMessageBox.information(self.mainwindow, "Перевод в корзину", "Домашнее задание успешно перемещено в корзину.")


    def validate_homework(self, homework_title, group_name, exclude_homework_id=None):
        """
        Проверяет, существует ли уже домашнее задание с таким названием в той же группе.

        :param homework_title: Название домашнего задания
        :param group_name: Название группы ДЗ (или None, если без группы)
        :param exclude_homework_id: ID текущего задания (при редактировании, чтобы не учитывать его самого)
        :return: True если валидация прошла успешно, False если такое ДЗ уже существует
        """
        for homework in self.mainwindow.homework_data:
            if homework["Название"] == homework_title and homework.get("Группа ДЗ") == group_name:
                if exclude_homework_id is None or homework["id"] != exclude_homework_id:
                    return False  # Такое ДЗ уже существует
        return True

