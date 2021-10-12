from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox, QLineEdit
from random import randint


class Guess:
    def __init__(self):
        self.answer = randint(1, 2000)
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
        if your_guess > self.answer:
            QMessageBox.information(self.window, '提示', f'{your_guess}太大了')
            self.logText.appendPlainText(f'{your_guess}太大了')
        elif your_guess == self.answer:
            QMessageBox.information(self.window, '提示', f'{your_guess},恭喜您猜对了')
            self.logText.appendPlainText(f'{your_guess},恭喜您猜对了')
        else:
            QMessageBox.information(self.window, '提示', f'{your_guess}太小了')
            self.logText.appendPlainText(f'{your_guess}太小了')
        self.textEdit.clear()


g = Guess()
g.begin()
