import sys
import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QColorDialog, QInputDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.names = ['line', 'straight', 'circle', 'rectangle', 'spray']
        self.counter = 0
        self.mode = 0
        self.left_corner = 0
        self.now = 0
        self.width = 9
        self.n = 4
        self.x = 13
        self.sizes = (700, 700)
        self.image = QImage(self.sizes[0], self.sizes[1], QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.initUI()
        self.color = '#ffffff'
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def initUI(self):
        self.setFixedSize(self.sizes[0], self.sizes[1])
        self.setWindowTitle('Paint 2.0')
        self.setWindowIcon(QIcon("pictures/Icon.png"))

        Menu = self.menuBar()
        file = Menu.addMenu("File")
        forms = Menu.addMenu("Forms")
        brushes = Menu.addMenu("Brushes")
        colors = Menu.addMenu("Color")
        widths = Menu.addMenu("Width")

        self.widths(widths)
        self.file(file)
        self.brushes(brushes)
        self.colors(colors)
        self.forms(forms)

        self.show()

    def mouseMoveEvent(self, QMouseEvent):
        if self.mode == 0:
            if not self.left_corner == [-1, -1]:
                qp = QPainter(self.image)
                qp.begin(self.image)
                pen = QPen(QColor(self.color), self.width)
                qp.setPen(pen)
                qp.drawLine(self.left_corner[0], self.left_corner[1], QMouseEvent.x(), QMouseEvent.y())
            self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]

        elif self.mode == 4:
            self.draw_spray(QMouseEvent.x(), QMouseEvent.y())

        elif self.mode == 3 or self.mode == 2 or self.mode == 1:
            if not self.left_corner == [-1, -1]:
                self.now = [QMouseEvent.x(), QMouseEvent.y()]
        self.update()

    def mousePressEvent(self, QMouseEvent):
        if self.mode == 4:
            self.draw_spray(QMouseEvent.x(), QMouseEvent.y())
        if self.counter % 2 == 0:
            self.left_corner = [-1, -1]
            if self.mode == 2 or self.mode == 3 or self.mode == 1:
                self.setMouseTracking(True)
                self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]
                self.now = [QMouseEvent.x(), QMouseEvent.y()]
        else:
            qp = QPainter(self.image)
            qp.begin(self.image)
            pen = QPen(QColor(self.color), self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            qp.setPen(pen)
            if self.mode == 1:
                qp.drawLine(self.left_corner[0], self.left_corner[1], QMouseEvent.x(), QMouseEvent.y())
            elif self.mode == 2:
                qp.drawEllipse(self.left_corner[0], self.left_corner[1], QMouseEvent.x() - self.left_corner[0], QMouseEvent.y() - self.left_corner[1])
            elif self.mode == 3:
                pen = QPen(QColor(self.color), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                qp.setPen(pen)
                qp.setBrush(QBrush(self.color, Qt.SolidPattern))
                qp.drawRect(self.left_corner[0], self.left_corner[1], QMouseEvent.x() - self.left_corner[0], QMouseEvent.y() - self.left_corner[1])
            self.setMouseTracking(False)
            self.left_corner = [-1, -1]
        self.update()
        self.counter += 1
        self.counter %= 2

    def draw_spray(self, x, y):
        qp = QPainter(self.image)
        qp.begin(self.image)
        pen = QPen(QColor(self.color), 1)
        qp.setPen(pen)
        my_count = 0
        while my_count < self.x:
            a, b = random.randint(-self.width // 2, self.width // 2), random.randint(-self.width // 2, self.width // 2)
            if a ** 2 + b ** 2 < (self.width // 2) ** 2:
                my_count += 1
                qp.drawPoint(x + a, y + b)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(self.rect(), self.image, self.image.rect())
        pen = QPen(QColor(self.color), self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        qp.setPen(pen)
        if self.mode == 3:
            if not self.left_corner == [-1, -1]:
                pen = QPen(QColor(self.color), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                qp.setPen(pen)
                qp.setBrush(QBrush(self.color, Qt.SolidPattern))
                qp.drawRect(self.left_corner[0], self.left_corner[1], self.now[0] - self.left_corner[0], self.now[1] - self.left_corner[1])
        elif self.mode == 2:
            if not self.left_corner == [-1, -1]:
                qp.drawEllipse(self.left_corner[0], self.left_corner[1], self.now[0] - self.left_corner[0], self.now[1] - self.left_corner[1])
        elif self.mode == 1:
            if not self.left_corner == [-1, -1]:
                qp.drawLine(self.left_corner[0], self.left_corner[1], self.now[0], self.now[1])

    def forms(self, form):
        rectangle = QAction(QIcon("pictures/rectangle.png"), "Rectangle", self)
        form.addAction(rectangle)
        rectangle.triggered.connect(self.rectangle)

        circle = QAction(QIcon("pictures/circle.png"), "Circle", self)
        form.addAction(circle)
        circle.triggered.connect(self.circle)

        straight = QAction(QIcon("pictures/straight.png"), "Straight", self)
        form.addAction(straight)
        straight.triggered.connect(self.straight)

    def rectangle(self):
        self.mode = 3
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    def circle(self):
        self.mode = 2
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    def straight(self):
        self.mode = 1
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    def brushes(self, brushes):
        brush = QAction(QIcon("pictures/Brush.png"), "Brush", self)
        brushes.addAction(brush)
        brush.triggered.connect(self.brush)

        spray = QAction(QIcon("pictures/Spray.png"), "Spray", self)
        brushes.addAction(spray)
        spray.triggered.connect(self.spray)

    def brush(self):
        self.mode = 0
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    def spray(self):
        self.mode = 4
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    def file(self, fileMenu):
        save = QAction(QIcon("pictures/save.png"), "Save As...", self)
        save.setShortcut("Ctrl+S")
        fileMenu.addAction(save)
        save.triggered.connect(self.save)

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;" " JPEG(*.jpg *.jpeg);;" " ALL Files(*.*)")
        if filePath == '':
            return
        else:
            self.image.save(filePath)

    def colors(self, colors):
        change_color = colors.addAction(QIcon("pictures/colors.png"), 'change Color')
        change_color.setShortcut("Ctrl+F")
        change_color.triggered.connect(self.change_color)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def widths(self, widths):
        change_width = widths.addAction(QIcon("pictures/width.png"), 'change Width')
        change_width.setShortcut("Ctrl+W")
        change_width.triggered.connect(self.change_width)

    def change_width(self):
        i, okBtnPressed = QInputDialog.getInt(
            self, "Введите ширину", "Ширина:", self.width, 9, 30, 1
        )
        if okBtnPressed:
            self.width = int(i)

    def closeEvent(self, event):
        flag = QMessageBox.question(self, 'Exit', "Do you want to save changes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if flag == QMessageBox.Yes:
            self.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    ex.qp.end()
