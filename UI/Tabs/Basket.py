from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox)

from gasket import Gasket


class Basket:
    def __init__(self,mainwindow, gasket: Gasket):
        self.gasket = gasket
        self.mainwindow = mainwindow


    # def restore_selected_objects(self):
    #     selected_rows = self.get_selected_trash_rows()
    #     if not selected_rows:
    #         QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите объекты для восстановления.")
    #         return
    #
    #     # Сортируем индексы строк в обратном порядке, чтобы корректно удалять строки
    #     selected_rows.sort(reverse=True)
    #
    #     for row in selected_rows:
    #         try:
    #             item = self.mainwindow.trash_data[row]  # Получаем объект из корзины
    #             object_type = item["Тип"]
    #
    #             # Возвращаем объект в соответствующую таблицу
    #             if object_type == "Ученик":
    #                 self.gasket.update_student(student_id=item['Данные']["id"], draft_status=False)
    #                 self.mainwindow.data.load_initial_data()
    #             elif object_type == "Домашнее задание":
    #                 self.gasket.update_homework(homework_id=item['Данные']["id"], is_deleted=False)
    #                 self.mainwindow.data.load_initial_data()
    #             elif object_type == "Класс":
    #                 self.gasket.update_class(class_id=item['Данные']["id"], draft_status=False)
    #                 self.mainwindow.data.load_initial_data()
    #             elif object_type == "Группа ДЗ":
    #                 self.gasket.update_homework_group(homework_group_id=item['Данные']["id"], draft_status=False)
    #                 self.mainwindow.data.load_initial_data()
    #
    #         except IndexError:
    #             QMessageBox.critical(self.mainwindow, "Ошибка", f"Не удалось восстановить объект на строке {row + 1}.")
    #             continue
    #         except KeyError as e:
    #             QMessageBox.critical(self.mainwindow, "Ошибка", f"Отсутствует ключ: {e}.")
    #             continue
    #
    #     QMessageBox.information(self.mainwindow, "Восстановление", "Выбранные объекты успешно восстановлены.")

    def restore_selected_objects(self):
        selected_rows = self.get_selected_trash_rows()
        if not selected_rows:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите объекты для восстановления.")
            return

        # Сортируем индексы строк в обратном порядке, чтобы корректно удалять строки
        selected_rows.sort(reverse=True)

        restored_any = False  # Флаг, отслеживающий, был ли восстановлен хотя бы один объект

        for row in selected_rows:
            try:
                item = self.mainwindow.trash_data[row]  # Получаем объект из корзины
                object_type = item["Тип"]
                object_data = item["Данные"]

                # Проверка наличия объекта вне корзины
                if object_type == "Ученик":
                    existing_student = next(
                        (student for student in self.mainwindow.students_data
                         if student["ФИО"] == object_data["ФИО"] and student.get("Класс") == object_data.get("Класс")),
                        None
                    )
                    if existing_student:
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            f"Ученик {object_data['ФИО']} уже существует в классе {object_data.get('Класс', 'Без класса')}.")
                        continue
                    self.gasket.update_student(student_id=object_data["id"], draft_status=False)
                    restored_any = True

                elif object_type == "Домашнее задание":
                    existing_homework = next(
                        (hw for hw in self.mainwindow.homework_data
                         if hw["Название"] == object_data["Название"] and hw.get("Группа ДЗ") == object_data.get(
                            "Группа ДЗ")),
                        None
                    )
                    if existing_homework:
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            f"Домашнее задание '{object_data['Название']}' уже существует в группе {object_data.get('Группа ДЗ', 'Без группы')}.")
                        continue
                    self.gasket.update_homework(homework_id=object_data["id"], is_deleted=False)
                    restored_any = True

                elif object_type == "Класс":
                    existing_class = next(
                        (cls for cls in self.mainwindow.classes_data if cls["№"] == object_data["№"]),
                        None
                    )
                    if existing_class:
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            f"Класс {object_data['№']} уже существует.")
                        continue
                    self.gasket.update_class(class_id=object_data["id"], draft_status=False)
                    restored_any = True

                elif object_type == "Группа ДЗ":
                    existing_group = next(
                        (group for group in self.mainwindow.groups_data if
                         group["Название группы"] == object_data["Название группы"]),
                        None
                    )
                    if existing_group:
                        QMessageBox.warning(self.mainwindow, "Ошибка",
                                            f"Группа ДЗ '{object_data['Название группы']}' уже существует.")
                        continue
                    self.gasket.update_homework_group(homework_group_id=object_data["id"], draft_status=False)
                    restored_any = True

                self.mainwindow.data.load_initial_data()

            except IndexError:
                QMessageBox.critical(self.mainwindow, "Ошибка", f"Не удалось восстановить объект на строке {row + 1}.")
                continue
            except KeyError as e:
                QMessageBox.critical(self.mainwindow, "Ошибка", f"Отсутствует ключ: {e}.")
                continue

        if restored_any:
            QMessageBox.information(self.mainwindow, "Восстановление", "Выбранные объекты успешно восстановлены.")

    def delete_selected_objects(self):
        selected_rows = self.get_selected_trash_rows()
        if not selected_rows:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите объекты для удаления.")
            return

        # Сортируем строки в обратном порядке
        selected_rows.sort(reverse=True)

        for row in selected_rows:
            try:
                item = self.mainwindow.trash_data[row]  # Получаем объект из корзины
                object_type = item["Тип"]

                # Возвращаем объект в соответствующую таблицу
                if object_type == "Ученик":
                    self.gasket.delete_student(student_id=item['Данные']["id"])
                    self.mainwindow.data.load_initial_data()
                elif object_type == "Домашнее задание":
                    self.gasket.delete_homework(homework_id=item['Данные']["id"])
                    self.mainwindow.data.load_initial_data()
                elif object_type == "Класс":
                    self.gasket.delete_class(class_id=item['Данные']["id"])
                    self.mainwindow.data.load_initial_data()
                elif object_type == "Группа ДЗ":
                    self.gasket.delete_homework_group(homework_group_id=item['Данные']["id"])
                    self.mainwindow.data.load_initial_data()
            except IndexError:
                QMessageBox.critical(self.mainwindow, "Ошибка", f"Не удалось удалить объект на строке {row + 1}.")
                continue

        QMessageBox.information(self.mainwindow, "Удаление", "Выбранные объекты успешно удалены.")

    def view_selected_item_cards(self):
        """Открывает карточки для выбранных объектов с возможностью переключения."""
        selected_rows = self.get_selected_trash_rows()
        if not selected_rows:
            QMessageBox.warning(self.mainwindow, "Ошибка", "Выберите объекты для просмотра.")
            return

        # Собираем данные выбранных объектов
        selected_items = [self.mainwindow.trash_data[row] for row in selected_rows]

        # Создаем и отображаем карточки
        self.show_item_card_dialog(selected_items)


    def update_trash(self):
        """Обновляет таблицу корзины с данными."""
        self.mainwindow.ui.trash_table.clearContents()
        self.mainwindow.ui.trash_table.setRowCount(len(self.mainwindow.trash_data))
        for row, item in enumerate(self.mainwindow.trash_data):
            type_item = QtWidgets.QTableWidgetItem(item["Тип"])
            name_item = QtWidgets.QTableWidgetItem(item["Наименование"])
            type_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Блокируем редактирование
            name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.mainwindow.ui.trash_table.setItem(row, 0, type_item)
            self.mainwindow.ui.trash_table.setItem(row, 1, name_item)

            # Добавляем чекбокс в третий столбец
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")  # Для выравнивания
            checkbox_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(checkbox_widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем чекбокс
            layout.setContentsMargins(0, 0, 0, 0)
            self.mainwindow.ui.trash_table.setCellWidget(row, 2, checkbox_widget)

            # Автоматическое подстраивание ширины столбцов
            self.mainwindow.ui.trash_table.resizeColumnsToContents()

    def show_item_card_dialog(self, items):
        """Показывает карточки объектов с переключением между ними."""
        dialog = QDialog(self.mainwindow)
        dialog.setWindowTitle("Карточки объектов")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)

        # Поле для отображения номера текущей карточки
        page_label = QLabel(dialog)
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(page_label)

        # Поле для отображения информации
        info_label = QLabel(dialog)
        info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Индекс текущего объекта
        current_index = [0]

        def update_info():
            """Обновляет содержимое карточки и отображает номер текущей."""
            item = items[current_index[0]]
            # Обновление текста с информацией о карточке
            page_label.setText(f"<b>Карточка {current_index[0] + 1} из {len(items)}</b>")

            # Обновление содержимого карточки
            info_text = f"<p><b style='color:blue;'>Тип:</b> {item['Тип']}</p>"
            for key, value in item['Данные'].items():
                info_text += f"<p><b style='color:blue;'>{key}:</b> {value}</p>"
            info_label.setText(info_text)

        # Кнопка "Предыдущий"
        prev_button = QPushButton("Предыдущий", dialog)
        prev_button.setEnabled(False)  # Начинаем с первого объекта
        prev_button.clicked.connect(lambda: go_to_previous())
        layout.addWidget(prev_button)

        # Кнопка "Следующий"
        next_button = QPushButton("Следующий", dialog)
        next_button.setEnabled(len(items) > 1)  # Отключаем, если объектов меньше 2
        next_button.clicked.connect(lambda: go_to_next())
        layout.addWidget(next_button)

        # Функции переключения
        def go_to_previous():
            """Переход к предыдущей карточке."""
            if current_index[0] > 0:
                current_index[0] -= 1
                update_info()
                next_button.setEnabled(True)  # Всегда включаем кнопку "Следующий"
                if current_index[0] == 0:
                    prev_button.setEnabled(False)  # Отключаем "Предыдущий" на первой карточке

        def go_to_next():
            """Переход к следующей карточке."""
            if current_index[0] < len(items) - 1:
                current_index[0] += 1
                update_info()
                prev_button.setEnabled(True)  # Всегда включаем кнопку "Предыдущий"
                if current_index[0] == len(items) - 1:
                    next_button.setEnabled(False)  # Отключаем "Следующий" на последней карточке

        # Кнопка "Закрыть"
        close_button = QPushButton("Закрыть", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        # Инициализируем содержимое первой карточки
        update_info()

        # Устанавливаем макет и отображаем диалог
        dialog.setLayout(layout)
        dialog.exec()

    def get_selected_trash_rows(self):
        """Возвращает список индексов выбранных строк."""
        selected_rows = []
        for row in range(self.mainwindow.ui.trash_table.rowCount()):
            checkbox_widget = self.mainwindow.ui.trash_table.cellWidget(row, 2)
            if checkbox_widget:
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                if checkbox.isChecked():
                    selected_rows.append(row)
        return selected_rows

    def select_all_trash(self, checked):
        """Отмечает или снимает галочки со всех объектов."""
        for row in range(self.mainwindow.ui.trash_table.rowCount()):
            checkbox_widget = self.mainwindow.ui.trash_table.cellWidget(row, 2)
            if checkbox_widget:
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                checkbox.setChecked(checked)