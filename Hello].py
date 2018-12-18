import sys
import math

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QPainter, QColor, QPen


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.names = ['line', 'straight', 'circle', 'rectangle']
        self.counter = 0
        self.mode = 0
        self.end1 = 0
        self.begin1 = 0
        self.left_corner = 0
        self.width = 5
        self.n = 4
        self.pole = [['#ffffff' for j in range(660)] for i in range(660)]
        self.circles = []
        self.straights = []
        self.rectangles = []
        self.initUI()
        self.color = QColorDialog.getColor()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setFixedSize(600, 600)
        self.setWindowTitle('Paint 2.0(line) width = 5')
        self.show()

    def mouseMoveEvent(self, QMouseEvent):
        if self.color.isValid():
            if self.mode == 0:
                for i in range(self.width):
                    for j in range(self.width):
                        self.pole[QMouseEvent.x() + i][QMouseEvent.y() + j] = self.color

    def mousePressEvent(self, QMouseEvent):
        if self.counter % 2 == 0:
            if self.mode == 0:
                self.setMouseTracking(True)
            elif self.mode == 1:
                self.begin1 = [QMouseEvent.x(), QMouseEvent.y()]
            elif self.mode == 2 or self.mode == 3:
                self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]
        else:
            if self.mode == 0:
                self.setMouseTracking(False)
            elif self.mode == 1:
                print(1)
                A = self.left_corner[1] - QMouseEvent.y()
                print(1)
                B = QMouseEvent.x() - self.left_corner[0]
                C = self.left_corner[0] * QMouseEvent.y() - QMouseEvent.x() * self.left_corner[1]

                for i in range(min(QMouseEvent.x(), self.left_corner[0]),
                               max(QMouseEvent.x(), self.left_corner[0])):
                    for j in range(min(QMouseEvent.x(), self.left_corner[0]),
                                   max(QMouseEvent.x(), self.left_corner[0])):
                        if abs(A * i + B * j + C) < self.width // 2:
                            self.pole[i][j] = self.color

            elif self.mode == 2:
                self.circles.append(([self.left_corner,
                                      [-self.left_corner[0] + QMouseEvent.x(), -self.left_corner[1] + QMouseEvent.y()]],
                                     self.color.name(), self.width))
            elif self.mode == 3:
                for i in range(min(self.left_corner[0], QMouseEvent.x()), max(self.left_corner[0], QMouseEvent.x())):
                    for i1 in range(self.width):
                        for j1 in range(self.width):
                            self.pole[i + i1][self.left_corner[1] + j1] = self.color
                            self.pole[i + i1][QMouseEvent.y() + j1] = self.color
                print(1)
                for i in range(min(self.left_corner[1], QMouseEvent.y()), max(self.left_corner[1], QMouseEvent.y())):
                    for i1 in range(self.width):
                        for j1 in range(self.width):
                            self.pole[self.left_corner[0] + i1][i + j1] = self.color
                            self.pole[QMouseEvent.x() + i1][i + j1] = self.color
            self.update()
        self.counter += 1
        self.counter %= 2

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for i in range(600):
            for j in range(600):
                qp.setPen(QColor(self.pole[i][j]))
                qp.drawPoint(i, j)
        for i in self.straights:
            pen = QPen(QColor(i[1]), i[2])
            qp.setPen(pen)
            qp.drawLine(i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1])
        for i in self.circles:
            pen = QPen(QColor(i[1]), i[2])
            qp.setPen(pen)
            qp.drawEllipse(i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.width = min(30, self.width + 1)
        if event.key() == Qt.Key_Left:
            self.width = max(5, self.width - 1)
        if event.key() == Qt.Key_F:
            self.color = QColorDialog.getColor()
            self.color = (int(self.color.name()[1:3], 16),
                          int(self.color.name()[3:5], 16),
                          int(self.color.name()[5:7], 16))
        if event.key() == Qt.Key_D:
            self.mode += 1
            self.mode %= self.n
        if event.key() == Qt.Key_A:
            self.mode += self.n - 1
            self.mode %= self.n
        self.setWindowTitle('Paint 2.0(' + self.names[self.mode] + ') width = ' + str(self.width))
        self.counter = 0

    def resizeEvent(self, QResizeEvent):
        print(self.frameGeometry().height(),
        self.frameGeometry().width())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    ex.qp.end()
