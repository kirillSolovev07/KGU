from SecondW import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from BAZE import *


class FirstW(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(350, 250, 305, 405)
        self.setFixedSize(305, 405)

        self.top_menu_create()

        self.formula = QLabel("Выберите формулу", self)
        self.formula.move(0, 30)
        self.formula.setAlignment(Qt.AlignCenter)
        self.formula.setStyleSheet("font-size: 30px;")
        self.formula.setFixedSize(305, 155)

        self.nums_create()

        self.show()

    def top_menu_create(self):
        self.frame = QFrame(self)
        self.frame.setFixedSize(305, 30)

        self.combobox_create()

        self.menu = QPushButton("Формулы", self.frame)
        self.menu.setStyleSheet("font-size: 18px; background-color: rgb(120,120, 120); color: white;")
        self.menu.setFixedSize(150, 30)
        self.menu.clicked.connect(self.secondW_create)

    def nums_create(self):
        group_number_button = QButtonGroup(self)
        x, y, i = 5, 185, 0
        for row in num_pad:
            for item in row:
                number_button = QPushButton(item, self)
                group_number_button.addButton(number_button, i)
                number_button.setFixedSize(70, 50)
                number_button.setStyleSheet("font-size: 20px;")
                number_button.move(x, y)
                i += 1
                if x == 230:
                    x = 5
                else:
                    x += 75

            y += 55

    def combobox_create(self):
        sections = ["Механика", "Термодинамика", "Электричество", "Оптика"]
        self.combobox = QComboBox(self.frame)
        self.combobox.addItems(sections)
        self.combobox.move(150, 0)
        self.combobox.setFixedSize(155, 30)
        self.combobox.setStyleSheet("font-size: 18px;")

    def secondW_create(self):
        index, text = self.combobox.currentIndex(), self.combobox.currentText()
        self.secondW = SecondW(index, text)
        self.secondW.show()


class SecondW(QWidget):
    def __init__(self, index, text):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 250, 250, 312)
        self.setFixedSize(250, 312)

        self.frame = QFrame(self)
        self.frame.setFixedSize(250, 32)

        self.group_buttons = QButtonGroup(self)
        self.variable_group = QButtonGroup(self)

        self.back_button = QPushButton("<", self.frame)
        self.back_button.setStyleSheet("font-size: 28px; color: white; background-color: rgb(31,147,255); border: 0;")
        self.back_button.setFixedSize(32, 32)

        self.title = QLabel(text, self.frame)
        self.title.setFixedWidth(250)
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setStyleSheet("font-size: 28px;color: white; background-color: rgb(140,140,140);")
        self.title.move(0, 0)

        self.check_index(index)

    def check_index(self, index, back=False):
        if back:
            for but in self.variable_group.buttons():
                self.variable_group.removeButton(but)
                but.hide()

        y = 32
        for text in BAZE[index]:
            button = QPushButton(text, self)
            self.group_buttons.addButton(button)
            button.setFixedSize(250, 40)
            button.setFont(QFont("Comic Sans mc", 15))
            button.move(0, y)
            button.clicked.connect(lambda b, ind=index, btn=button: self.variable_create(ind, btn))
            button.show()
            y += 40

    def variable_create(self, index, btn):
        self.back_create(index)

        for but in self.group_buttons.buttons():
            self.group_buttons.removeButton(but)
            but.hide()

        y = 32
        for text in BAZE[index][btn.text()]:
            button = QPushButton(text, self)
            self.variable_group.addButton(button)
            button.setFixedSize(250, 40)
            button.setFont(QFont("Comic Sans mc", 15))
            button.move(0, y)
            button.clicked.connect(lambda a, t=button.text(): self.ret_text_formul(t))
            button.show()
            y += 40

    def back_create(self, index):
        self.back_button.clicked.connect(lambda a, ind=index: self.back(ind))
        self.back_button.move(0, 0)

        self.title.setFixedWidth(218)
        self.title.move(32, 0)

    def back(self, index):
        self.check_index(index, back=True)
        self.title.setFixedWidth(250)
        self.title.move(0, 0)

    def ret_text_formul(self, text):
        win.formula.setText(text)


# CONST = {"G": 6.6743 * 10 ** (-11)}
app = QApplication([])
win = FirstW()
app.exec_()
print(globals()["win"])
