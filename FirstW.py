from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from BAZE import *
from math import sqrt
from pynput import mouse


class FirstW(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(350, 250, 300, 405)
        self.setFixedSize(300, 405)

        self.top_menu_create()

        self.formula = QLabel("Выберите формулу", self)
        self.formula.move(0, 30)
        self.formula.setAlignment(Qt.AlignCenter)
        self.formula.setStyleSheet("font-size: 30px;")
        self.formula.setFixedSize(300, 155)

        self.inserts = []
        self.labels = []

        self.frame1 = QFrame(self)
        self.frame1.setFixedSize(300, 125)
        self.frame1.move(0, 60)

        self.nums_create()

        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

        self.show()

    def on_click(self, x, y, button, is_pressed):
        global num_insert
        if is_pressed and str(button) == "Button.left":
            if row == 1 and (120 <= x - 350 <= 210):
                if 85 <= y - 250 <= 115:
                    num_insert = 0
                elif 120 <= y - 250 <= 150:
                    num_insert = 1
            elif row > 1 and (50 <= x - 350 <= 140):
                if 85 <= y - 250 <= 115:
                    num_insert = 0
                elif 120 <= y - 250 <= 150:
                    num_insert = 1
            elif row > 1 and (190 <= x - 350 <= 280):
                if 85 <= y - 250 <= 115:
                    num_insert = 2
                elif 120 <= y - 250 <= 150:
                    num_insert = 3
        elif str(button) == "Button.right":
            self.mouse_listener.stop()

    def top_menu_create(self):
        self.frame = QFrame(self)
        self.frame.setFixedSize(300, 30)
        self.combobox_create()
        self.menu = QPushButton("Формулы", self.frame)
        self.menu.setStyleSheet("font-size: 18px; background-color: rgb(120,120, 120); color: white;")
        self.menu.setFixedSize(150, 30)
        self.menu.clicked.connect(self.secondW_create)

    def nums_create(self):
        x, y = 35, 185
        for row in num_pad:
            for item in row:
                number_button = QPushButton(item, self)
                number_button.setFixedSize(70, 50)
                number_button.setStyleSheet("font-size: 20px;")
                number_button.move(x, y)
                if item == "=":
                    number_button.clicked.connect(self.get_calculate)
                elif item == "C":
                    number_button.clicked.connect(self.clear_insert)
                else:
                    number_button.clicked.connect(lambda a, text=number_button.text(): self.insert_num(text))
                if x == 195:
                    x = 35
                else:
                    x += 80

            y += 55

    def clear_insert(self):
        if len(self.inserts) > 0 and num_insert != - 1 and len(self.inserts[num_insert].text()) > 0:
            self.inserts[num_insert].clear()
    def insert_num(self, text):
        if len(self.inserts) > 0 and num_insert != - 1:
            self.inserts[num_insert].insert(text)
    def check_nums(self, number):
        try:
            float(number)
            return True
        except:
            return False

    def get_calculate(self):
        if self.formula.text() != "Выберите формулу":
            self.data_for_calc = []
            for i in self.inserts:
                if len(i.text()) != 0 and self.check_nums(i.text()):
                    self.data_for_calc += [i.text()]
                else:
                    if len(i.text()) == 0:
                        self.msgBox("Не заполнены все поля", "Заполните все поля ввода!")
                    else:
                        self.msgBox("Неккоректные данные", "Можно вводить только цифры!")
                    return 0

            right_part = self.formula.text()
            right_part = right_part.replace(" ", "")[right_part.find("="):]
            for i in u"\u2082\u2081\u00B2\u2080":
                if i in right_part:
                    right_part = right_part.replace(i, "")
            for i in range(len(right_part)):
                if right_part[i] in "/*-+()\u221A":
                    self.data_for_calc.insert(i, right_part[i])
            self.calculate()

    def msgBox(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def calculate(self):
        SQRT = False
        if u"\u221A" in self.data_for_calc:
            SQRT = True
            self.data_for_calc = "".join(self.data_for_calc[1:])
        else:
            self.data_for_calc = "".join(self.data_for_calc)
        # print(self.data_for_calc, type(self.data_for_calc), sep="\t")
        try:
            left_part = self.formula.text()
            left_part = left_part[:left_part.find("=") + 1]
            if SQRT:
                result = left_part + " " + str(round(sqrt(eval(self.data_for_calc)), 2))
            else:
                result = left_part + " " + str(float(round(eval(self.data_for_calc), 2)))
        except ZeroDivisionError:
            self.msgBox("Деление на ноль", "На ноль делить нельзя!")
            return 0
        self.show_result(result)

    def hide_lab_ins(self):
        for i in self.labels:
            i.hide()
        for i in self.inserts:
            i.hide()
        win.inserts = []
        win.labels = []

    def show_result(self, result):
        self.hide_lab_ins()
        self.formula.setFixedSize(300, 155)
        self.formula.setStyleSheet("font-size: 30px;")
        self.formula.setText(result)

    def combobox_create(self):
        sections = ["Механика", "Термодинамика", "Электричество", "Оптика"]
        self.combobox = QComboBox(self.frame)
        self.combobox.addItems(sections)
        self.combobox.move(150, 0)
        self.combobox.setFixedSize(150, 30)
        self.combobox.setStyleSheet("font-size: 18px;")

    def secondW_create(self):
        index, text = self.combobox.currentIndex(), self.combobox.currentText()
        self.secondW = SecondW(index, text, parent=self)
        self.secondW.show()

        # if self.formula.text() != "Выберите формулу":
        #     self.formula.setText("Выберите формулу")
        #     self.formula.setAlignment(Qt.AlignCenter)
        #     self.formula.setStyleSheet("font-size: 30px;")
        #     self.formula.setFixedSize(305, 155)


class SecondW(QWidget):
    def __init__(self, index, text, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
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

    def create_label_equally(self, x, y):
        equ = QLabel("=", win.frame1)
        equ.setFixedWidth(20)
        equ.setStyleSheet("font-size: 20px;")
        equ.move(x, y)
        return equ

    def create_inserts_and_labels(self, s, x, y, row=False):
        count = 1
        for i in range(len(s)):
            if s[i] not in "/*-+":
                if (s[i] != s[-1]) and (s[i] not in u"\u2082\u2081\u00B2\u2080") and (
                        s[i + 1] in u"\u2082\u2081\u00B2\u2080"):
                    t = s[i] + s[i + 1]
                elif s[i] in u"\u2082\u2081\u00B2\u2080()\u221A":
                    continue
                else:
                    t = s[i]

                label = QLabel(t, win.frame1)
                label.setStyleSheet("font-size: 18px;")
                label.setFixedWidth(25)
                label.move(x, y)
                label.show()
                equally = self.create_label_equally(x + 25, y)
                equally.show()
                win.labels += [label]
                win.labels += [equally]

                insert = QLineEdit(win.frame1)
                insert.setStyleSheet("font-size: 18px;")
                insert.move(x + 45, y)
                insert.setFixedSize(90, 30)
                insert.show()
                win.inserts += [insert]
                if row:
                    if count == 2:
                        y = 25
                        count = 0
                        x += 150
                    else:
                        y += 35
                        count += 1
                else:
                    y += 35

    def check_col(self, s):
        global row
        text = s
        for i in u"\u2082\u2081\u00B2\u2080\u221A/*-+()":
            if i in s:
                s = s.replace(i, "")
        y = 25
        if len(s) > 2:
            row = 2
            x = 5
            self.create_inserts_and_labels(text, x, y, row=True)
        else:
            x = 75
            self.create_inserts_and_labels(text, x, y)

    def ret_text_formul(self, text):
        self.hide()

        s = text.replace(" ", "")
        s = s[s.find("=") + 1:]

        if win.formula.text() != "Выберите формулу":
            for i in win.labels:
                i.hide()

            for i in win.inserts:
                i.hide()

            win.inserts = []
            win.labels = []
            self.check_col(s)
        else:
            self.check_col(s)

        win.formula.setText(text)
        win.formula.setStyleSheet("font-size: 22px;")
        win.formula.setFixedHeight(30)


# CONST = {"G": 6.6743 * 10 ** (-11)}
app = QApplication([])
win = FirstW()
img = QIcon("calc.png")
row = 1
num_insert = -1
app.setWindowIcon(img)
app.exec_()
