from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPolygonF
from random import randint

class example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ui.ui", self)
        self.pushButton.clicked.connect(self.run)
        self.qp = QPainter()
        self.flag = False

    def run(self):
        self.drawf()

    def drawf(self):
        self.flag = True
        self.update()

    def paintEvent(self, event):
        if self.flag:
            self.qp = QPainter()
            self.qp.begin(self)
            self.draw()
            self.qp.end()

    def draw(self):
        R = randint(20, 100)
        self.qp.setBrush(QColor(255, 255, 0))
        self.qp.drawEllipse(QPointF(randint(20, 700), randint(20, 700)), R, R)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = example()
    ex.show()
    sys.exit(app.exec())