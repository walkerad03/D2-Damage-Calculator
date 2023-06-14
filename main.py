from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
import sys

from video_player import VideoPlayer
from damage_type_button import DamageTypeButton


class PopupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popup Window")

        self.label1 = QLabel("Damage Name:", self)
        self.text1 = QLineEdit(self)

        self.label2 = QLabel("Damage Value:", self)
        self.text2 = QLineEdit(self)

        self.ok_button = QPushButton("Add", self)
        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.text1)
        layout.addWidget(self.label2)
        layout.addWidget(self.text2)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Destiny DPS Calculator")
        self.setGeometry(0, 0, 960, 540)

        video_player = VideoPlayer()

        self.add_weapon_type_btn = QPushButton("Add Damage Type")
        self.add_weapon_type_btn.clicked.connect(self.open_damage_value_popup)

        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.addWidget(self.add_weapon_type_btn)

        main_layout = QHBoxLayout()
        main_layout.addWidget(video_player)
        main_layout.addLayout(self.sidebar)

        self.setLayout(main_layout)

    def open_damage_value_popup(self):
        popup = PopupWindow()
        if popup.exec_() == QDialog.Accepted:
            damage_name = popup.text1.text()
            damage_value = int(popup.text2.text())
            damage_button = DamageTypeButton(damage_name, damage_value)
            self.sidebar.addWidget(damage_button)


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())
