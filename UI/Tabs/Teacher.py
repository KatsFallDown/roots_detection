from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
import os

class Teacher:
    NOTES_FILE = "teacher_notes.txt"  # Файл для сохранения заметок

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.load_notes()  # Загружаем заметки при создании объекта

    def update_teacher_classes(self, classes):
        self.save_notes()  # Сохраняем заметки перед обновлением данных

        self.mainwindow.ui.teacher_table.setRowCount(len(classes))
        for row, class_data in enumerate(classes):
            self.mainwindow.ui.teacher_table.setItem(row, 0, QTableWidgetItem(class_data["number"]))
            self.mainwindow.ui.teacher_table.setItem(row, 1, QTableWidgetItem(str(class_data["students"])))
            self.mainwindow.ui.teacher_table.setItem(row, 2, QTableWidgetItem(class_data["group"]))
            self.mainwindow.ui.teacher_table.setItem(row, 3, QTableWidgetItem(str(class_data["published"])))
            self.mainwindow.ui.teacher_table.setItem(row, 4, QTableWidgetItem(str(class_data["drafts"])))
        self.mainwindow.ui.teacher_table.resizeColumnsToContents()

        self.load_notes()  # Загружаем сохраненные заметки

    def save_notes(self):
        notes = self.mainwindow.ui.teacher_textEdit.toPlainText()
        with open(self.NOTES_FILE, "w", encoding="utf-8") as file:
            file.write(notes)

    def load_notes(self):
        if os.path.exists(self.NOTES_FILE):
            with open(self.NOTES_FILE, "r", encoding="utf-8") as file:
                notes = file.read()
                self.mainwindow.ui.teacher_textEdit.setPlainText(notes)

