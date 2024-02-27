from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
import random

"""
Mortal combat game:

User vs computer

2 types of attack.
1 type of defense.

Choose 3 actions. Computer will also choose 3. Then FIGHT.
Attacks will do different amounts of damage to players health meter.
Display Health Meter value.
Once fight is happening, a different picture will display for each action.
Players first action will be played against computer’s first action and on and on.
If defense is played, the attack will only do minor damage.

Once health meter is at zero for either player, their picture will show defeat, and the winner will show a victory picture.

Bonus for:
reset Btn
character selection
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mortal Combat")

        self.moves = []
        self.moves.append(self.create_move("Attack 1", 25, 0, "nuclear-explosion.png"))
        self.moves.append(self.create_move("Attack 2", 30, 0, "sword.png"))
        self.moves.append(self.create_move("Defense 1", 0, 15, "shield.png"))
        self.reset()

    def create_move(self, name: str, damage: int, defend: int, img: str):
        return {"name": name, "damage": damage, "defend": defend, "img": img}

    def reset(self):
        self.initialize_new_game_state()
        self.load_screen()
        return

    def initialize_new_game_state(self):
        self.user_health = 100
        self.pc_health = 100
        self.user_actions = []
        self.pc_actions = []

    def select_move(self, move: dict):
        self.user_actions.append(move)
        if len(self.user_actions) == 3:
            self.select_pc_moves()
            self.play()
            self.user_actions = []
            self.pc_actions = []

    def select_pc_moves(self):
        self.pc_actions = [random.choice(self.moves) for _ in range(3)]

    def turn_lambda(self, user_action, pc_action):
        return lambda: self.evaluate_turn(user_action, pc_action)

    def play(self):
        milis = 500
        for user_action, pc_action in zip(self.user_actions, self.pc_actions):
            QTimer.singleShot(milis, self.turn_lambda(user_action, pc_action))
            milis += 1000

    def evaluate_turn(self, user_action: dict, pc_action: dict):
        self.user_health -= pc_action["damage"] - user_action["defend"]
        self.pc_health -= user_action["damage"] - pc_action["defend"]
        self.pc_image.setPixmap(QPixmap(f'./assets/{pc_action["img"]}'))
        self.pc_image.setVisible(True)
        self.user_image.setPixmap(QPixmap(f'./assets/{user_action["img"]}'))
        self.user_image.setVisible(True)

        self.lbl_user_health.setText(f"Your health: {self.user_health}")
        self.lbl_pc_health.setText(f"Opponent health: {self.pc_health}")

        if self.pc_health <= 0:
            self.pc_image.setPixmap(QPixmap("./assets/defeat.png"))
            self.user_image.setPixmap(QPixmap("./assets/victory.png"))
        elif self.user_health <= 0:
            self.pc_image.setPixmap(QPixmap("./assets/victory.png"))
            self.user_image.setPixmap(QPixmap("./assets/defeat.png"))

    def move_lambda(self, move: dict):
        return lambda: self.select_move(move)

    def load_screen(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        # Labels
        self.lbl_user_health = QLabel(f"Your health: {self.user_health}")
        self.lbl_pc_health = QLabel(f"Opponent health: {self.pc_health}")

        # Buttons
        move_buttons = []
        for move in self.moves:
            btn = QPushButton(move["name"])
            btn.clicked.connect(self.move_lambda(move))
            move_buttons.append(btn)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset)

        # Images
        self.user_image = QLabel("")
        self.user_image.setVisible(False)
        self.pc_image = QLabel("")
        self.pc_image.setVisible(False)

        row = 0
        self.layout.addWidget(self.lbl_user_health, row, 0)
        self.layout.addWidget(self.lbl_pc_health, row, 1)

        row = 1
        for col in range(len(move_buttons)):
            self.layout.addWidget(move_buttons[col], row, col)

        row = 2
        self.layout.addWidget(self.user_image, row, 0, 1, 2)
        self.layout.addWidget(self.pc_image, row, 2, 1, 2)

        row = 3
        self.layout.addWidget(self.btn_reset, row, 0, 1, 2)


app = QApplication()
window = MainWindow()
window.show()
app.exec()
