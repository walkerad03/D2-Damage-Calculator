from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle

from video_player import VideoPlayer


class DamageTypeButton(QWidget):
    def __init__(self, damage_name: str, damage_value: int, video_player: VideoPlayer):
        super().__init__()
        self.damage_name = damage_name
        self.damage_value = damage_value
        self.video_player = video_player

        name_button = QPushButton(self.damage_name)
        delete_button = QPushButton()
        delete_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        button_size = delete_button.sizeHint().height()
        delete_button.setFixedSize(button_size, button_size)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(name_button)
        hbox.addWidget(delete_button)

        self.setLayout(hbox)

        name_button.clicked.connect(self.log_damage_value)
        delete_button.clicked.connect(self.delete_widget)

    def log_damage_value(self):
        damage = self.damage_value
        position = int(self.video_player.media_player.position() * 60 / 1000)

        with open("damage_values.csv", "a") as file:
            file.write(f"{position}, {damage}\n")

    def delete_widget(self):
        self.deleteLater()
