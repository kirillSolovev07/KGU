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


# CONST = {"G": 6.6743 * 10 ** (-11)}
app = QApplication([])
win = FirstW()
app.exec_()
print(globals()["win"])
