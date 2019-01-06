import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
    QFileDialog, QMessageBox
from PyQt5.QtWidgets import QColorDialog, QInputDialog


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        # счётчик нажатий при рисовании прямоугольника, прямой и элипса
        self.counter = 0
        # переменная обозначающая мод кисти сейчас, всего модов 5:
        #  кривая, прямая, элипс, прямоугольник и балончик
        self.mode = 0
        # координаты первого из углов фигуры
        # (для элипса: первого из углов прямоугольника, в который элипс вписан)
        self.left_corner = 0
        # координаты ворого из углов фигуры
        # (для элипса - второго из углов прямоугольника,
        #  в который элипс вписан,
        #  а для прямой - её конец) на момент выбора
        self.now = 0
        # ширина кисти
        self.width = 9
        # колличество модов
        self.n = 4
        # колличество точек при рисовании балончиком
        self.x = 13
        # размеры окна
        self.sizes = (700, 700)
        # место для рисования
        self.image = QImage(self.sizes[0], self.sizes[1], QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.initUI()
        # цвет кисти или контуров
        self.color = QColor('#000000')
        # цвет заливки
        self.color1 = QColor('#000000')

    def initUI(self):
        self.setFixedSize(self.sizes[0], self.sizes[1])
        self.setWindowTitle('Paint 2.0')
        self.setWindowIcon(QIcon("pictures/Icon.png"))

        # меню
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
        # рисование кривой
        if self.mode == 0:
            if not self.left_corner == [-1, -1]:
                qp = QPainter(self.image)
                qp.begin(self.image)
                pen = QPen(QColor(self.color), self.width)
                qp.setPen(pen)
                qp.drawLine(self.left_corner[0], self.left_corner[1],
                            QMouseEvent.x(), QMouseEvent.y())
            self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]

        # рисование балончиком
        elif self.mode == 4:
            self.draw_spray(QMouseEvent.x(), QMouseEvent.y())

        # изменение второго угла временного прямоугольника, элипса или прямой
        elif self.mode == 3 or self.mode == 2 or self.mode == 1:
            if not self.left_corner == [-1, -1]:
                self.now = [QMouseEvent.x(), QMouseEvent.y()]
        self.update()

    def mousePressEvent(self, QMouseEvent):
        # рисование балончиком
        if self.mode == 4:
            self.draw_spray(QMouseEvent.x(), QMouseEvent.y())
        # рисование начала или левого угла
        if self.counter % 2 == 0:
            self.left_corner = [-1, -1]
            if self.mode == 2 or self.mode == 3 or self.mode == 1:
                self.setMouseTracking(True)
                self.left_corner = [QMouseEvent.x(), QMouseEvent.y()]
                self.now = [QMouseEvent.x(), QMouseEvent.y()]
        # рисование фигуры
        else:
            qp = QPainter(self.image)
            qp.begin(self.image)
            pen = QPen(
                QColor(self.color),
                self.width,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin
            )
            qp.setPen(pen)
            qp.setBrush(QBrush(self.color1, Qt.SolidPattern))
            # рисование прямой
            if self.mode == 1:
                qp.drawLine(self.left_corner[0], self.left_corner[1],
                            QMouseEvent.x(), QMouseEvent.y())
            # рисование елипса
            elif self.mode == 2:
                qp.drawEllipse(
                    self.left_corner[0],
                    self.left_corner[1],
                    QMouseEvent.x() - self.left_corner[0],
                    QMouseEvent.y() - self.left_corner[1]
                )
            # рисование прямоугольника
            elif self.mode == 3:
                qp.drawRect(
                    self.left_corner[0],
                    self.left_corner[1],
                    QMouseEvent.x() - self.left_corner[0],
                    QMouseEvent.y() - self.left_corner[1]
                )
            self.setMouseTracking(False)
            self.left_corner = [-1, -1]
        self.update()
        self.counter += 1
        self.counter %= 2

    # формула для рисования балончиком
    def draw_spray(self, x, y):
        qp = QPainter(self.image)
        qp.begin(self.image)
        pen = QPen(QColor(self.color), 1)
        qp.setPen(pen)
        my_count = 0
        while my_count < self.x:
            a = random.randint(-self.width // 2, self.width // 2)
            b = random.randint(-self.width // 2, self.width // 2)
            if a ** 2 + b ** 2 < (self.width // 2) ** 2:
                my_count += 1
                qp.drawPoint(x + a, y + b)

    # изменение экрана
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(self.rect(), self.image, self.image.rect())
        pen = QPen(
            QColor(self.color),
            self.width,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
        )
        qp.setPen(pen)
        qp.setBrush(QBrush(self.color1, Qt.SolidPattern))
        # рисование временного прямогольника
        if self.mode == 3:
            if not self.left_corner == [-1, -1]:
                qp.drawRect(
                    self.left_corner[0],
                    self.left_corner[1],
                    self.now[0] - self.left_corner[0],
                    self.now[1] - self.left_corner[1]
                )
        # рисование временного элипса
        elif self.mode == 2:
            if not self.left_corner == [-1, -1]:
                qp.drawEllipse(
                    self.left_corner[0],
                    self.left_corner[1],
                    self.now[0] - self.left_corner[0],
                    self.now[1] - self.left_corner[1]
                )
        # рисование временной прямой
        elif self.mode == 1:
            if not self.left_corner == [-1, -1]:
                qp.drawLine(
                    self.left_corner[0],
                    self.left_corner[1],
                    self.now[0],
                    self.now[1]
                )

    # раздел форм
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

    # все формы
    # прямоугольник
    def rectangle(self):
        self.mode = 3
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    # элипс
    def circle(self):
        self.mode = 2
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    # прямая
    def straight(self):
        self.mode = 1
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    # раздел кистей
    def brushes(self, brushes):
        brush = QAction(QIcon("pictures/Brush.png"), "Brush", self)
        brushes.addAction(brush)
        brush.triggered.connect(self.brush)

        spray = QAction(QIcon("pictures/Spray.png"), "Spray", self)
        brushes.addAction(spray)
        spray.triggered.connect(self.spray)

    # все кисти
    # обычная кисть
    def brush(self):
        self.mode = 0
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    # балончик
    def spray(self):
        self.mode = 4
        self.setMouseTracking(False)
        self.left_corner = [-1, -1]
        self.counter = 0

    # раздел файл
    def file(self, fileMenu):
        save = QAction(QIcon("pictures/save.png"), "Save As...", self)
        save.setShortcut("Ctrl+S")
        fileMenu.addAction(save)
        save.triggered.connect(self.save)

    # сохранение
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG(*.png);;" " JPEG(*.jpg *.jpeg);;" " ALL Files(*.*)"
        )
        if filePath == '':
            return
        else:
            self.image.save(filePath)

    # раздел цвета
    def colors(self, colors):
        change_color = colors.addAction(
            QIcon("pictures/colors.png"),
            'change Color'
        )
        change_color.setShortcut("Ctrl+F")
        change_color.triggered.connect(self.change_color)

        change_color1 = colors.addAction(
            QIcon("pictures/colors.png"),
            'change Brush Color'
        )
        change_color1.setShortcut("Ctrl+Shift+F")
        change_color1.triggered.connect(self.change_color1)

    # обработка изменение цвета контуров
    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    # обработка изменение цвета заливки
    def change_color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color1 = color

    # раздел ширины
    def widths(self, widths):
        change_width = widths.addAction(
            QIcon("pictures/width.png"),
            'change Width'
        )
        change_width.setShortcut("Ctrl+W")
        change_width.triggered.connect(self.change_width)

    # обработка изменения ширины
    def change_width(self):
        i, okBtnPressed = QInputDialog.getInt(
            self, "Введите ширину", "Ширина:", self.width, 9, 30, 1
        )
        if okBtnPressed:
            self.width = int(i)

    # обработка закрытия окна и сохранение изменений
    def closeEvent(self, event):
        flag = QMessageBox.question(
            self,
            'Exit',
            "Do you want to save changes?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
        if flag == QMessageBox.Yes:
            self.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    ex.qp.end()
