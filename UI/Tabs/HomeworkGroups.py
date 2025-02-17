from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidgetItem)

from gasket import Gasket


class HomeworkGroups:
    def __init__(self,mainwindow, gasket: Gasket):
        self.gasket = gasket
        self.mainwindow = mainwindow

    def create_input_dialog(self, title, fields, additional_fields=None):
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle(title)

        layout = QFormLayout(dialog)

        inputs = {}
        for field in fields:
            input_field = QLineEdit(dialog)
            layout.addRow(QLabel(field), input_field)
            inputs[field] = input_field

        # Добавляем дополнительные поля, если они переданы
        if additional_fields:
            for field_name, widget in additional_fields.items():
                layout.addRow(QLabel(field_name), widget)
                inputs[field_name] = widget

        # Добавляем кнопки сохранения и отмены
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

    def update_groups(self):
        """Обновляет таблицу групп с данными."""
        # Очищаем только содержимое ячеек, оставляя заголовки колонок нетронутыми
        self.mainwindow.ui.groups_table.clearContents()

        self.mainwindow.ui.groups_table.setRowCount(len(self.mainwindow.groups_data))
        for row, group_data in enumerate(self.mainwindow.groups_data):
            self.mainwindow.ui.groups_table.setItem(row, 0, QTableWidgetItem(group_data["Название группы"]))
            self.mainwindow.ui.groups_table.setItem(row, 1, QTableWidgetItem(group_data["Примечание"]))

        # Автоматическое подстраивание ширины столбцов
        self.mainwindow.ui.groups_table.resizeColumnsToContents()

    def open_add_group_dialog(self):
        # Открываем диалоговое окно для ввода данных
        dialog, inputs = self.create_input_dialog("Добавить группу", ["Название группы", "Примечание"])

        while True:
            if dialog.exec():
                # Извлекаем данные из полей
                group_name = inputs["Название группы"].text().strip()
                note = inputs["Примечание"].text().strip()

                # Проверка, что название группы не пустое
                if not group_name:
                    QMessageBox.warning(self.mainwindow, "Ошибка", "Название группы не может быть пустым!")
                    continue  # Продолжаем цикл, чтобы пользователь исправил ошибку

                # Проверка на уникальность названия группы
                if any(group["Название группы"] == group_name for group in self.mainwindow.groups_data):
                    QMessageBox.warning(self.mainwindow, "Ошибка", f"Группа с названием '{group_name}' уже существует!")
                    continue  # Если группа с таким названием существует, продолжаем цикл

                # Если ошибок нет, добавляем новую группу
                new_group = {
                    "Название группы": group_name,
                    "Примечание": note
                }

                self.gasket.add_homework_group(name= new_group["Название группы"], info = new_group["Примечание"])
                self.mainwindow.data.load_initial_data()

                QMessageBox.information(self.mainwindow, "Добавление группы", "Группа добавлена успешно!")
                break  # Выходим из цикла, завершив процесс
            else:
                break  # Если диалог был закрыт кнопкой "Отмена", выходим

    def open_edit_group_dialog(self):
        selected_row = self.mainwindow.ui.groups_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.mainwindow, "Редактирование", "Пожалуйста, выберите строку для редактирования.")
            return

        if selected_row >= len(self.mainwindow.groups_data):
            QMessageBox.warning(self.mainwindow, "Редактирование", "Вы выбрали пустую строку.")
            return

        group_data = self.mainwindow.groups_data[selected_row]
        dialog, inputs = self.create_input_dialog("Редактировать группу", ["Название группы", "Примечание"])

        # Заполнение текущих значений
        inputs["Название группы"].setText(group_data["Название группы"])
        inputs["Примечание"].setText(group_data["Примечание"])

        while True:
            if dialog.exec():
                # Извлекаем обновленные данные
                updated_group_name = inputs["Название группы"].text().strip()
                updated_note = inputs["Примечание"].text().strip()
                # Проверка, что название группы не пустое
                if not updated_group_name:
                    QMessageBox.warning(self.mainwindow, "Ошибка", "Название группы не может быть пустым!")
                    continue  # Если название пустое, продолжаем цикл

                # Проверка на уникальность названия группы (проверяем, что новое название не совпадает с другим)
                if any(
                        group["Название группы"] == updated_group_name
                        for i, group in enumerate(self.mainwindow.groups_data) if i != selected_row
                ):
                    QMessageBox.warning(self.mainwindow, "Ошибка", f"Группа с названием '{updated_group_name}' уже существует!")
                    continue  # Если группа с таким названием существует, продолжаем цикл

                # Если ошибок нет, обновляем данные группы
                updated_group = {
                    "id": group_data["id"],
                    "Название группы": updated_group_name,
                    "Примечание": updated_note
                }
                self.gasket.update_homework_group(homework_group_id= updated_group["id"],
                                                  name=updated_group["Название группы"],
                                                  info=updated_group["Примечание"] )
                self.mainwindow.data.load_initial_data()


                QMessageBox.information(self.mainwindow, "Редактирование группы", "Группа обновлена успешно!")
                break  # Выходим из цикла, завершив процесс
            else:
                break  # Если диалог был закрыт кнопкой "Отмена", выходим

    def shadow_group(self):
        """
        Перемещает выбранный класс и, при необходимости, его учеников в корзину.
        """
        try:
            selected_row = self.mainwindow.ui.groups_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите группу ДЗ для перемещения в корзину.")
                return

            if selected_row >= len(self.mainwindow.groups_data):
                QMessageBox.warning(self.mainwindow, "Ошибка", "Выбрана пустая строка.")
                return

            # Получаем данные класса
            group_data = self.mainwindow.groups_data[selected_row]

            # Создаем диалог подтверждения с пользовательскими кнопками
            confirm_dialog = QMessageBox(self.mainwindow)
            confirm_dialog.setIcon(QMessageBox.Icon.Question)
            confirm_dialog.setWindowTitle("Перевод в корзину")
            confirm_dialog.setText("Вы хотите переместить только группу или группу и домашние задания этой группы ?")

            # Создаем кнопки вручную
            only_group_button = confirm_dialog.addButton("Только группу", QMessageBox.ButtonRole.YesRole)
            group_and_homework_button = confirm_dialog.addButton("Группу и ДЗ", QMessageBox.ButtonRole.NoRole)
            cancel_button = confirm_dialog.addButton(QMessageBox.StandardButton.Cancel)

            # Запускаем диалог и получаем результат
            confirm_dialog.exec()
            clicked_button = confirm_dialog.clickedButton()

            if clicked_button == cancel_button:
                return

            if clicked_button==only_group_button:
                # Удаляем группу из данных и добавляем его в корзину
                self.gasket.update_homework_group( homework_group_id= group_data["id"], draft_status= True)
                self.mainwindow.data.load_initial_data()
                QMessageBox.information(self.mainwindow, "Перевод в корзину", "Группа ДЗ  успешно перемещена в корзину.")

            # Если выбрано группу и ДЗ
            if clicked_button == group_and_homework_button:

                homeworks_to_remove = [homework for homework in self.mainwindow.homework_data
                                       if homework["Группа ДЗ"] == group_data["Название группы"]]
                for homework in homeworks_to_remove:
                    self.gasket.update_homework(homework_id= homework["id"], draft_status= True)

                self.gasket.update_homework_group( homework_group_id =group_data["id"], draft_status=True)
                self.mainwindow.data.load_initial_data()
                QMessageBox.information(self.mainwindow, "Перевод в корзину",
                                        "Группа и домашние задания этой группы успешно перемещены в корзину.")

        except IndexError:
            QMessageBox.critical(self.mainwindow, "Ошибка", "Возникла проблема с выбором строки.")
        except Exception as e:
            QMessageBox.critical(self.mainwindow, "Ошибка", f"Произошла ошибка: {str(e)}")

    # def shadow_group(self):
    #     """Перемещает выбранного ученика в корзину."""
    #     selected_row = self.mainwindow.ui.groups_table.currentRow()
    #     if selected_row == -1:
    #         QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите группу для перемещения в корзину.")
    #         return
    #
    #     groups_data = self.mainwindow.groups_data[selected_row]
    #     self.gasket.update_homework_group(homework_id= groups_data["id"], draft_status = True)
    #     self.mainwindow.data.load_initial_data()
    #
    #     # self.mainwindow.trash_data.append({"Тип": "Группа ДЗ", "Наименование": groups_data["Название группы"], "Данные":groups_data})
    #     # self.update_groups()
    #     # self.mainwindow.basket.update_trash()
