from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF

class Cell(QWidget):
    def __init__(self, alive=False):
        super().__init__()
        self.alive = alive
        self.setFixedSize(20, 20)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.alive:
            painter.setBrush(QBrush(QColor(46, 204, 113)))
        else:
            painter.setBrush(QBrush(QColor(52, 73, 94)))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 2, 2)

    def toggle(self):
        self.alive = not self.alive
        self.animate_toggle()
        self.update()

    def animate_toggle(self):
        start = self.geometry()
        end = QRectF(start)
        end.setSize(end.size() * 1.2)
        end.moveCenter(start.center())
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()
