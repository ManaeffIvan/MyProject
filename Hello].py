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
        self.end1 = 0
        self.begin1 = 0
        self.left_corner = 0
        self.width = 5
        self.n = 5
        self.pole = [['#ffffff' for j in range(360)] for i in range(360)]
        self.circles = []
        self.straights = []
        self.rectangles = []
        self.initUI()
        self.color = QColorDialog.getColor()

    def initUI(self):
        self.setGeometry(0, 0, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle('Paint 2.0(line) width = 5')
        self.show()

    def mouseMoveEvent(self, QMouseEvent):
        if self.color.isValid():
            if self.mode == 0:
                for i in range(self.width):
                    for j in range(self.width):
                        self.pole[QMouseEvent.x() + i][QMouseEvent.y() + j] = self.color

    def recursion(self, x, y, x_begin, y_begin, n):
        if x in range(-1, 301) and y in range(-1, 301) and self.pole[x][y] == self.pole[x_begin][y_begin] and n < 900:
            if x != x_begin or y_begin != y:
                self.pole[x][y] = self.color
                n += 1
            n = self.recursion(x - 1, y, x_begin, y_begin, n)
            n = self.recursion(x, y - 1, x_begin, y_begin, n)
            n = self.recursion(x + 1, y, x_begin, y_begin, n)
            n = self.recursion(x, y + 1, x_begin, y_begin, n)
        return n

    def mousePressEvent(self, QMouseEvent):
        if self.mode == 4:
            k = 0
            k1 = 1
            while k != k1:
                k1 = k
                k += self.recursion(QMouseEvent.x(), QMouseEvent.y(), QMouseEvent.x(), QMouseEvent.y(), 0)
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
                            for i1 in range(self.width):
                                for j1 in range(self.width):
                                    self.pole[i + i1][j + j1] = self.color
                                    self.pole[i + i1][j + j1] = self.color
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
                            for i1 in range(self.width):
                                for j1 in range(self.width):
                                    self.pole[i + i1][j + j1] = self.color
                                    self.pole[i + i1][j + j1] = self.color
            elif self.mode == 3:
                for i in range(min(self.left_corner[0], QMouseEvent.x()), max(self.left_corner[0], QMouseEvent.x())):
                    for i1 in range(self.width):
                        for j1 in range(self.width):
                            self.pole[i + i1][self.left_corner[1] + j1] = self.color
                            self.pole[i + i1][QMouseEvent.y() + j1] = self.color
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
        for i in range(300):
            for j in range(300):
                qp.setPen(QColor(self.pole[i][j]))
                qp.drawPoint(i, j)

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
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    ex.qp.end()
