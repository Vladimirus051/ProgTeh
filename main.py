import sys
from PyQt5.QtWidgets import QApplication
from game_of_life import GameOfLife

def main():
    app = QApplication(sys.argv)
    game = GameOfLife()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
