# Paint 2.0
## Автор: Манаев Иван Александрович
Этот проект является попыткой реализации программы Paint, с меньшим колличеством функций. Это чисто графический редактор, где не возможно вставить картинку, а можно только рисовать самому. Эта идея пришла ко мне, когда нам предложили сделать проект по PyQt5.

Я рисую объекты в объекте класса QImage и рисую на главный экран этот объект, так создаётся впечатление, что пользователь рисует на главном экране. Для рисования фигуры (прямой, прямоугольника, элипса) нужны два нажатия в одном из углов(концов) и в противоположном, для элипса нужно указать два противоположных угла описанного вокруг него прямоугольника. Для рисования кистью и балончиком достаточно простого зажимания и движения мыши.

У меня имеется один класс Example наследуемый от QMainWindow. Также в нём я создаю меню, в котором можно выбрать один из 5 инструментов: кисть, прямая, прямоугольник, элипс, балончик. Смену инструмента я сделал с помощью переменной mode. В нём также можно откорректировать цвет контурных линий, их ширину и заливку фигуры (прямоугольника и элипса).

Свой рисунок, сделанный в программе можно легко сохранить во время работы, но даже забыв его сохранить, программа напомнит вам об этом перед закрытием. Я использовал библиотеки: random, sys, PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets.
![скриншот рисования](https://github.com/ManaeffIvan/MyProject/blob/master/pictures/screen1.png)
![скриншот меню](https://github.com/ManaeffIvan/MyProject/blob/master/pictures/screen2.png)
![скриншот выбора цвета](https://github.com/ManaeffIvan/MyProject/blob/master/pictures/screen3.png)
![скриншот выбора ширины](https://github.com/ManaeffIvan/MyProject/blob/master/pictures/screen4.png)
![скриншот предупреждения перед выходом](https://github.com/ManaeffIvan/MyProject/blob/master/pictures/screen5.png)
