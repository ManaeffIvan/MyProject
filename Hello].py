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
        self.pole = [[(255, 255, 255) for j in range(660)] for i in range(660)]
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
                        self.pole[QMouseEvent.x() + i][QMouseEvent.y() + j] = (int(self.color.name()[1:3], 16),
                                                                       int(self.color.name()[3:5], 16),
                                                                       int(self.color.name()[5:7], 16))

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
                self.end1 = [QMouseEvent.x(), QMouseEvent.y()]
                self.straights.append(([self.begin1, self.end1], self.color.name(), self.width))
            elif self.mode == 2:
                self.circles.append(([self.left_corner,
                                      [-self.left_corner[0] + QMouseEvent.x(), -self.left_corner[1] + QMouseEvent.y()]],
                                     self.color.name(), self.width))
            elif self.mode == 3:
                self.rectangles.append(([self.left_corner,
                                      [-self.left_corner[0] + QMouseEvent.x(), -self.left_corner[1] + QMouseEvent.y()]],
                                     self.color.name(), self.width))
            self.update()
        self.counter += 1
        self.counter %= 2

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for i in range(600):
            for j in range(600):
                qp.setPen(QColor(self.pole[i][j][0], self.pole[i][j][1], self.pole[i][j][2]))
                qp.drawPoint(i, j)
        for i in self.straights:
            pen = QPen(QColor(int(i[1][1:3], 16),
                              int(i[1][3:5], 16),
                              int(i[1][5:7], 16)), i[2])
            qp.setPen(pen)
            qp.drawLine(i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1])
        for i in self.circles:
            pen = QPen(QColor(int(i[1][1:3], 16),
                              int(i[1][3:5], 16),
                              int(i[1][5:7], 16)), i[2])
            qp.setPen(pen)
            qp.drawEllipse(i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1])
        for i in self.rectangles:
            pen = QPen(QColor(int(i[1][1:3], 16),
                              int(i[1][3:5], 16),
                              int(i[1][5:7], 16)), i[2])
            qp.setPen(pen)
            qp.drawRect(i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1])
        qp.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.width = min(30, self.width + 1)
        if event.key() == Qt.Key_Left:
            self.width = max(5, self.width - 1)
        if event.key() == Qt.Key_F:
            self.color = QColorDialog.getColor()
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