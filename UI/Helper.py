from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QMessageBox
)
import re
class Helper:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
    
    def setup_filters(self):
        """Настройка фильтрации для каждой вкладки."""
        # Настраиваем фильтры для вкладки "Классы"
        self.setup_filter_for_table(
            self.mainwindow.ui.classes_table,
            self.mainwindow.ui.classes_comboBox_filter,
            self.mainwindow.ui.classes_lineEdit_input
        )

        # Настраиваем фильтры для вкладки "Группы"
        self.setup_filter_for_table(
            self.mainwindow.ui.groups_table,
            self.mainwindow.ui.groups_comboBox_filter,
            self.mainwindow.ui.groups_lineEdit_input
        )

        # Настраиваем фильтры для вкладки "Домашка"
        self.setup_filter_for_table(
            self.mainwindow.ui.homework_table,
            self.mainwindow.ui.homework_comboBox_filter,
            self.mainwindow.ui.homework_lineEdit_input
        )

        # Настраиваем фильтры для вкладки "Ученики"
        self.setup_filter_for_table(
            self.mainwindow.ui.students_table,
            self.mainwindow.ui.students_comboBox_filter,
            self.mainwindow.ui.students_lineEdit_input
        )

    def setup_filter_for_table(self, table, comboBox, lineEdit):
        """
        Настройка фильтрации для одной таблицы.

        :param table: QTableWidget - Таблица, для которой настраивается фильтр
        :param comboBox: QComboBox - Выпадающий список со столбцами
        :param lineEdit: QLineEdit - Поле ввода текста для фильтрации
        """
        # Добавляем названия всех столбцов в комбобокс
        comboBox.clear()
        comboBox.addItem("Все столбцы")
        for col in range(table.columnCount()):
            comboBox.addItem(table.horizontalHeaderItem(col).text())

        # Настраиваем действие при изменении текста в QLineEdit
        def apply_filter():
            filter_text = lineEdit.text().lower()
            selected_column = comboBox.currentIndex() - 1  # "Все столбцы" имеет индекс 0

            # Показать все строки перед применением фильтра
            for row in range(table.rowCount()):
                table.setRowHidden(row, False)

            if filter_text:  # Применяем фильтр только если есть текст
                for row in range(table.rowCount()):
                    match_found = False
                    for col in range(table.columnCount()):
                        if selected_column == -1 or col == selected_column:  # Все столбцы или выбранный
                            item = table.item(row, col)
                            if item and filter_text in item.text().lower():
                                match_found = True
                                break
                    table.setRowHidden(row, not match_found)

        # Соединяем сигнал изменения текста с функцией фильтрации
        lineEdit.textChanged.connect(apply_filter)
        comboBox.currentIndexChanged.connect(apply_filter)
