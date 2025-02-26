import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize

class ResultWindow(QMainWindow):
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle("Result")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("background-color: #2E3440;")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.result_label = QLabel(result, self)
        self.result_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.result_label.setStyleSheet("color: #88C0D0;")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        if result == "YOU WIN!!!":
            image_path = "happy.png"
        elif result == "YOU LOSE!!!":
            image_path = "sad.png"
        else:
            image_path = "neutral.png"
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        else:
            self.image_label.setText("Image not found!")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock Paper Scissors")
        self.setGeometry(100, 100, 600, 400)
        self.set_background_image("background.png")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.title_label = QLabel("", self)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #88C0D0;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        self.play_button = QPushButton("Play Game", self)
        self.play_button.setFont(QFont("Arial", 16))
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                color: #2E3440;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.play_button.setFixedSize(QSize(200, 60))
        self.play_button.clicked.connect(self.open_game_window)
        layout.addWidget(self.play_button, alignment=Qt.AlignCenter)

    def set_background_image(self, image_path):
        self.background_image_path = image_path
        self.update_background()

    def update_background(self):
        palette = self.palette()
        pixmap = QPixmap(self.background_image_path)
        if not pixmap.isNull():
            palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            self.setStyleSheet("background-color: #2E3440;")

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def open_game_window(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.hide()

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock Paper Scissors - Game")
        self.setGeometry(100, 100, 800, 500)
        self.set_background_image("background.jpg")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        left_layout = QVBoxLayout()
        rules_label = QLabel("RULES", self)
        rules_label.setFont(QFont("Arial", 18, QFont.Bold))
        rules_label.setStyleSheet("color: #88C0D0;")
        rules_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(rules_label)
        rules_text = QLabel(
            "1. Rock beats Scissors\n"
            "2. Scissors beats Paper\n"
            "3. Paper beats Rock", self
        )
        rules_text.setFont(QFont("Arial", 14))
        rules_text.setStyleSheet("color: #D8DEE9;")
        left_layout.addWidget(rules_text)
        fate_label = QLabel("CHOOSE YOUR FATE", self)
        fate_label.setFont(QFont("Arial", 18, QFont.Bold))
        fate_label.setStyleSheet("color: #88C0D0;")
        fate_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(fate_label)
        self.choice_dropdown = QComboBox(self)
        self.choice_dropdown.addItem("Choose here")
        self.choice_dropdown.addItems(["Rock", "Paper", "Scissors"])
        self.choice_dropdown.setFont(QFont("Arial", 14))
        self.choice_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #81A1C1;
                color: #2E3440;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        left_layout.addWidget(self.choice_dropdown, alignment=Qt.AlignCenter)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFont(QFont("Arial", 14))
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                color: #2E3440;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.submit_button.setFixedSize(QSize(150, 50))
        self.submit_button.clicked.connect(self.play_game)
        left_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        layout.addLayout(left_layout)
        right_layout = QVBoxLayout()
        self.image_label = QLabel(self)
        pixmap = QPixmap("game.png")
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            self.image_label.setText("Game image not found!")
        self.image_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.image_label)
        layout.addLayout(right_layout)

    def set_background_image(self, image_path):
        self.background_image_path = image_path
        self.update_background()

    def update_background(self):
        palette = self.palette()
        pixmap = QPixmap(self.background_image_path)
        if not pixmap.isNull():
            palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            self.setStyleSheet("background-color: #2E3440;")

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def play_game(self):
        if self.choice_dropdown.currentText() == "Choose here":
            QMessageBox.warning(self, "Warning", "Please select an option!")
            return
        user_choice = self.choice_dropdown.currentText().lower()
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        if user_choice == computer_choice:
            result = "IT'S A TIE!!!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "YOU WIN!!!"
        else:
            result = "YOU LOSE!!!"
        self.result_window = ResultWindow(result)
        self.result_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_page = StartPage()
    start_page.show()
    sys.exit(app.exec_())
