import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.high_score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_board()

    def initUI(self):
        self.setWindowTitle('2048')
        self.setGeometry(300, 300, 400, 550)
        layout = QVBoxLayout()
        self.score_label = QLabel('Score: 0')
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet('font-size: 18px; font-weight: bold; margin-bottom: 10px;')
        layout.addWidget(self.score_label)
        self.grid = QGridLayout()
        self.labels = [[QLabel('0') for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.labels[i][j].setAlignment(Qt.AlignCenter)
                self.labels[i][j].setStyleSheet('background-color: #cdc1b4; color: #c9efff; font-size: 24px; font-weight: bold; border: 1px solid #bbada0; border-radius: 10px;')
                self.labels[i][j].setFixedSize(80, 80)
                self.grid.addWidget(self.labels[i][j], i, j)

        layout.addLayout(self.grid)
        button_layout = QHBoxLayout()
        buttons = ['left', 'up', 'down', 'right']
        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.on_button_click)
            button_layout.addWidget(button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_button_click(self):
        sender = self.sender()
        if sender.text() == 'left':
            self.move_left()
        elif sender.text() == 'right':
            self.move_right()
        elif sender.text() == 'up':
            self.move_up()
        elif sender.text() == 'down':
            self.move_down()
        self.add_new_tile()
        self.update_board()
        self.update_score()
        if not self.can_move():
            self.game_over()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_board(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                self.labels[i][j].setText(str(value) if value != 0 else '')
                self.labels[i][j].setStyleSheet(self.get_color(value))

    def get_color(self, value):
        colors = {
            0: '#cdc1b4',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e'
        }
        return f'background-color: {colors.get(value, "#3c3a32")}; color: {"#f9f6f2" if value > 4 else "#776e65"}; font-size: 24px; font-weight: bold; border: 1px solid #bbada0; border-radius: 10px;'

    def move_left(self):
        self.board, score_increase = self.merge_row_left(self.board)
        self.score += score_increase

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        self.board, score_increase = self.merge_row_left(self.board)
        self.board = [row[::-1] for row in self.board]
        self.score += score_increase

    def move_up(self):
        self.board = list(map(list, zip(*self.board)))
        self.board, score_increase = self.merge_row_left(self.board)
        self.board = list(map(list, zip(*self.board)))
        self.score += score_increase

    def move_down(self):
        self.board = list(map(list, zip(*self.board)))
        self.board = [row[::-1] for row in self.board]
        self.board, score_increase = self.merge_row_left(self.board)
        self.board = [row[::-1] for row in self.board]
        self.board = list(map(list, zip(*self.board)))
        self.score += score_increase

    def merge_row_left(self, board):
        new_board = []
        score_increase = 0
        for row in board:
            new_row = [i for i in row if i != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    score_increase += new_row[i]
                    new_row[i + 1] = 0
            new_row = [i for i in new_row if i != 0]
            new_row += [0] * (4 - len(new_row))
            new_board.append(new_row)
        return new_board, score_increase

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score_label.setText(f'Score: {self.score}')

    def can_move(self):
        if any(0 in row for row in self.board):
            return True
        for i in range(4):
            for j in range(4):
                current = self.board[i][j]
                if (j < 3 and current == self.board[i][j+1]) or (i < 3 and current == self.board[i+1][j]):
                    return True
        return False

    def game_over(self):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"Game Over! Your score: {self.score}")
        msg.setInformativeText("Replay?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        ret = msg.exec_()
        if ret == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()
            
    def reset_game(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_board()
        self.update_score()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
