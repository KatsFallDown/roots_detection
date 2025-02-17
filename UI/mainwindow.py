from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QStatusBar

from Helper import Helper
from UI.Design.school import Ui_MainWindow
from UI.Tabs.Basket import Basket
from UI.Tabs.Classes import Classes
from UI.Tabs.HomeworkGroups import HomeworkGroups
from UI.Tabs.Homeworks import Homeworks
from UI.Tabs.Students import Students
from UI.Tabs.Teacher import Teacher
from data import Data
from gasket import Gasket


class SchoolApp(QMainWindow):
    def __init__(self, gasket: Gasket):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("School Management System")

        # Центрируем окно при запуске
        self.center_on_screen()

        self.gasket = gasket

        self.teacher = Teacher(self)
        self.classes = Classes(self,gasket)
        self.homeworks = Homeworks(self, gasket)
        self.homework_groups= HomeworkGroups(self, gasket)
        self.students = Students(self, gasket)
        self.basket = Basket(self, gasket)

        self.data = Data(gasket, self)
        self.helper = Helper(self)

        # Переменные для хранения данных
        self.classes_data = []
        self.groups_data = []
        self.homework_data = []
        self.students_data = []
        self.trash_data= []

        # Подключение кнопок к обработчикам и блокировка редактирования таблиц напрямую
        #Вкладка классов
        self.ui.classes_pushButton_add.clicked.connect(self.classes.open_add_class_dialog)
        self.ui.classes_pushButton_edit.clicked.connect(self.classes.open_edit_class_dialog)
        self.ui.classes_pushButton_shadow.clicked.connect(self.classes.shadow_class)
        self.ui.classes_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


        # Вкладка групп ДЗ
        self.ui.groups_pushButton_add.clicked.connect(self.homework_groups.open_add_group_dialog)
        self.ui.groups_pushButton_edit.clicked.connect(self.homework_groups.open_edit_group_dialog)
        self.ui.groups_pushButton_shadow.clicked.connect(self.homework_groups.shadow_group)
        self.ui.groups_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


        # Вкладка домашек
        self.ui.homework_pushButton_add.clicked.connect(self.homeworks.open_add_homework_dialog)
        self.ui.homework_pushButton_edit.clicked.connect(self.homeworks.open_edit_homework_dialog)
        self.ui.homework_pushButton_shadow.clicked.connect(self.homeworks.shadow_homework)
        self.ui.homework_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


        # Вкладка учеников
        self.ui.students_pushButton_add.clicked.connect(self.students.open_add_student_dialog)
        self.ui.students_pushButton_edit.clicked.connect(self.students.open_edit_student_dialog)
        self.ui.students_pushButton_shadow.clicked.connect(self.students.shadow_student)
        self.ui.students_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


        # Вкладка корзины
        self.ui.basket_pushButton_recover.clicked.connect(self.basket.restore_selected_objects)
        self.ui.basket_pushButton_view.clicked.connect(self.basket.view_selected_item_cards)
        self.ui.basket_pushButton_delete.clicked.connect(self.basket.delete_selected_objects)
        self.ui.trash_select_all_checkbox.stateChanged.connect(self.basket.select_all_trash)
        self.ui.trash_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Вкладка преподавателя
        self.ui.teacher_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)



        # Создаем статус-бар вручную
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.setFixedHeight(30)  # Устанавливаем высоту статус-бара

        # Метка для отображения времени последнего обновления
        self.last_updated_label = QLabel("Последнее обновление: -", self)

        # Кнопка обновления 🔄
        self.refresh_button = QPushButton(self)
        self.refresh_button.setIcon(QIcon("Design/icons/reload.png"))
        self.refresh_button.setToolTip("Обновить данные")

        # Добавляем в статус-бар (сначала метку, потом кнопку)
        self.statusBar().addWidget(self.last_updated_label)  # Слева
        self.statusBar().addPermanentWidget(self.refresh_button)  # Справа


        # Подключаем кнопку к обновлению
        self.refresh_button.clicked.connect(self.data.load_initial_data)


        #Фильтрация
        self.helper.setup_filters()

        self.data.load_initial_data()

    def center_on_screen(self):
        width = 870
        height = 705
        screen_geometry = self.screen().geometry()  # Получаем размеры экрана
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Проверяем, не выходит ли окно за границы экрана
        width = min(width, screen_width)  # Ограничиваем ширину
        height = min(height, screen_height)  # Ограничиваем высоту

        # Вычисляем координаты для центрирования
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.setMinimumSize(width, height)  # Минимальный размер
        self.setGeometry(x, y, width, height)

