import time
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox, QLineEdit
from random import randint


class Guess:
    def __init__(self, down=1, up=2000):
        self.up = up
        self.down = down
        self.answer = randint(self.down, self.up)
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.resize(640, 360)
        self.button = QPushButton('guess', self.window)
        self.button.resize(80, 25)
        self.button.move(260, 70)
        self.textEdit = QLineEdit(self.window)
        self.textEdit.setPlaceholderText('请输入想猜的数字')
        self.textEdit.resize(120, 25)
        self.textEdit.move(260, 40)
        self.textEdit.returnPressed.connect(self.guess_number)
        self.button.clicked.connect(self.guess_number)
        self.logText = QPlainTextEdit(self.window)
        self.logText.resize(300, 250)
        self.logText.move(170, 100)
        self.logText.setEnabled(False)

    def begin(self):
        self.window.show()
        self.app.exec_()

    def guess_number(self):
        your_guess = int(self.textEdit.text())
        if your_guess > 2000 or your_guess < 1:
            QMessageBox.information(self.window, '提示', f'数字范围在1-2000')
            self.textEdit.clear()
            return
        elif your_guess > self.up or your_guess < self.down:
            QMessageBox.information(self.window, '提示', f'数字范围在{self.down}~{self.up}之间')
            self.textEdit.clear()
            return
        if your_guess > self.answer:
            self.up = your_guess
            QMessageBox.information(self.window, '提示', f'{your_guess}太大了')
            self.logText.appendPlainText(f'{your_guess}太大了,范围{self.down}~{self.up}')
        elif your_guess == self.answer:
            QMessageBox.information(self.window, '提示', f'{your_guess},恭喜您猜对了')
            self.logText.appendPlainText(f'{your_guess},恭喜您猜对了')
            # 猜对直接重置游戏
            time.sleep(3)
            self.init_data()
        else:
            self.down = your_guess
            QMessageBox.information(self.window, '提示', f'{your_guess}太小了')
            self.logText.appendPlainText(f'{your_guess}太小了,范围{self.down}~{self.up}')
        self.textEdit.clear()

    def init_data(self):
        """初始化数据，并清空记录框的内容"""
        self.up = 2000
        self.down = 1
        self.answer = randint(self.down, self.up)
        self.logText.clear()


g = Guess()
g.begin()
