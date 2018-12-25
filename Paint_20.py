import sys

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QPainter, QColor, QPen


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.names = ['line', 'straight', 'circle', 'rectangle', 'casting']
        self.counter = 0
        self.mode = 0
        self.left_corner = 0
        self.x_begin = 0
        self.y_begin = 0
        self.width = 5
        self.n = 5
        self.pole = [['#ffffff' for j in range(360)] for i in range(360)]
        self.initUI()
        self.color = '#ffffff'
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def initUI(self):
        self.setGeometry(0, 0, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle('Paint 2.0(line) width = 5')
        self.show()

    def myPoint(self, x, y):
        for i in range(self.width):
            for j in range(self.width):
                self.pole[x + i][y + j] = self.color

    def mouseMoveEvent(self, QMouseEvent):
        if self.color.isValid():
            if self.mode == 0:
                self.myPoint(QMouseEvent.x(), QMouseEvent.y())

    def recursion(self, x, y, n):
        if x in range(-1, 401) and y in range(-1, 401) and self.pole[x][y] == self.pole[self.x_begin][self.y_begin]:
            if x != self.x_begin or self.y_begin != y:
                self.pole[x][y] = self.color
            self.recursion(x - 1, y, n)
            self.recursion(x, y - 1, n)
            self.recursion(x + 1, y, n)
            self.recursion(x, y + 1, n)

    def mousePressEvent(self, QMouseEvent):
        if self.mode == 4:
            self.x_begin = QMouseEvent.x()
            self.y_begin = QMouseEvent.y()
            self.recursion(QMouseEvent.x(), QMouseEvent.y(), 0)
            self.pole[QMouseEvent.x()][QMouseEvent.y()] = self.color
            self.update()
        if self.counter % 2 == 0:
            if self.mode == 0:
                self.setMouseTracking(True)
            elif self.mode == 2 or self.mode == 3 or self.mode == 1:
                self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]
        else:
            if self.mode == 0:
                self.setMouseTracking(False)
            elif self.mode == 1:
                A = self.left_corner[1] - QMouseEvent.y()
                B = QMouseEvent.x() - self.left_corner[0]
                C = self.left_corner[0] * QMouseEvent.y() - QMouseEvent.x() * self.left_corner[1]
                for i in range(min(QMouseEvent.x(), self.left_corner[0]),
                               max(QMouseEvent.x(), self.left_corner[0])):
                    for j in range(min(QMouseEvent.y(), self.left_corner[1]),
                                   max(QMouseEvent.y(), self.left_corner[1])):
                        if abs(A * i + B * j + C) < self.width * 5:
                            self.myPoint(i, j)
            elif self.mode == 2:
                center = ((self.left_corner[0] + QMouseEvent.x()) // 2, (self.left_corner[1] + QMouseEvent.y()) // 2)
                for i in range(min(QMouseEvent.x(), self.left_corner[0]) - self.width * 2,
                               max(QMouseEvent.x(), self.left_corner[0]) + self.width * 2):
                    for j in range(min(QMouseEvent.y(), self.left_corner[1] - self.width * 2),
                                   max(QMouseEvent.y(), self.left_corner[1]) + self.width * 2):
                        my_circle = (((i - center[0]) ** 2) * (((QMouseEvent.y() - self.left_corner[1]) // 2) ** 2) + (
                                ((QMouseEvent.x() - self.left_corner[0]) // 2) ** 2) * ((j - center[1]) ** 2)) / (
                                            ((QMouseEvent.x() - self.left_corner[0]) // 2) ** 2) / (
                                            ((QMouseEvent.y() - self.left_corner[1]) // 2) ** 2)
                        if my_circle < 1.05 and my_circle > 0.95:
                            self.myPoint(i, j)
            elif self.mode == 3:
                for i in range(min(self.left_corner[0], QMouseEvent.x()), max(self.left_corner[0], QMouseEvent.x())):
                    self.myPoint(i, self.left_corner[1])
                    self.myPoint(i, QMouseEvent.y())
                for i in range(min(self.left_corner[1], QMouseEvent.y()), max(self.left_corner[1], QMouseEvent.y())):
                    self.myPoint(self.left_corner[0], i)
                    self.myPoint(QMouseEvent.x(), i)
            self.update()
        self.counter += 1
        self.counter %= 2

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(QColor(self.pole[0][0]))
        for i in range(300):
            for j in range(300):
                pen = QPen(QColor(self.pole[i][j]))
                qp.setPen(pen)
                qp.drawPoint(i, j)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.width = min(30, self.width + 1)
        if event.key() == Qt.Key_Left:
            self.width = max(5, self.width - 1)
        if event.key() == Qt.Key_F:
            color = QColorDialog.getColor()
            if color.isValid():
                self.color = color
        if event.key() == Qt.Key_D:
            self.mode += 1
            self.mode %= self.n
        if event.key() == Qt.Key_A:
            self.mode += self.n - 1
            self.mode %= self.n
        self.setWindowTitle('Paint 2.0(' + self.names[self.mode] + ') width = ' + str(self.width))
        self.counter = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    ex.qp.end()
