import random
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
from cell import Cell

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра 'Жизнь'")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 18px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.title_label = QLabel("Игра 'Жизнь'")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.main_layout.addWidget(self.title_label)

        self.info_label = QLabel("Поколение: 0 | Живых клеток: 0")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.rows = 30
        self.cols = 30
        self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.grid_layout.addWidget(self.cells[i][j], i, j)
                self.cells[i][j].mousePressEvent = lambda event, r=i, c=j: self.toggle_cell(r, c)

        self.setup_buttons()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_grid)

        self.generation = 0
        self.is_running = False
        self.history = []
        self.repeat_count = 0
        self.max_repeat = 3

    def setup_buttons(self):
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        buttons = [
            ("Старт", self.start_game),
            ("Стоп", self.stop_game),
            ("Очистить", self.clear_grid),
            ("Случайно", self.randomize_grid)
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            button.clicked.connect(callback)
            self.button_layout.addWidget(button)

    def toggle_cell(self, row, col):
        self.cells[row][col].toggle()
        self.update_info()

    def start_game(self):
        self.timer.start(200)
        self.is_running = True

    def stop_game(self):
        self.timer.stop()
        self.is_running = False

    def clear_grid(self):
        self.stop_game()
        for row in self.cells:
            for cell in row:
                cell.alive = False
                cell.update()
        self.generation = 0
        self.history = []
        self.repeat_count = 0
        self.update_info()

    def randomize_grid(self):
        self.stop_game()
        for row in self.cells:
            for cell in row:
                cell.alive = random.choice([True, False])
                cell.update()
        self.generation = 0
        self.history = []
        self.repeat_count = 0
        self.update_info()

    def update_grid(self):
        new_state = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        current_tuple = tuple(tuple(cell.alive for cell in row) for row in self.cells)

        if current_tuple in self.history:
            self.repeat_count += 1
            if self.repeat_count >= self.max_repeat:
                self.add_random_cells()
                self.repeat_count = 0
        else:
            self.repeat_count = 0

        self.history.append(current_tuple)
        if len(self.history) > 10:
            self.history.pop(0)

        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                if self.cells[i][j].alive:
                    new_state[i][j] = neighbors in [2, 3]
                else:
                    new_state[i][j] = neighbors == 3

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].alive = new_state[i][j]
                self.cells[i][j].update()

        self.generation += 1
        self.update_info()

        if self.check_game_over():
            self.stop_game()
            self.show_game_over_message()

    def add_random_cells(self):
        for _ in range(5):
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if not self.cells[row][col].alive:
                self.cells[row][col].alive = True
                self.cells[row][col].update()

    def count_neighbors(self, row, col):
        count = 0
        for i in range(max(0, row-1), min(self.rows, row+2)):
            for j in range(max(0, col-1), min(self.cols, col+2)):
                if (i, j) != (row, col) and self.cells[i][j].alive:
                    count += 1
        return count

    def update_info(self):
        alive_cells = sum(cell.alive for row in self.cells for cell in row)
        self.info_label.setText(f"Поколение: {self.generation} | Живых клеток: {alive_cells}")

    def check_game_over(self):
        return all(not cell.alive for row in self.cells for cell in row)

    def show_game_over_message(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Игра завершена")
        msg_box.setInformativeText("На поле не осталось живых клеток.")
        msg_box.setWindowTitle("Конец игры")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
