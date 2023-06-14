from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog, QDialog, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys

class DamageTypeButton(QPushButton):
    def __init__(self, damage_name: str, damage_value: int):
        super().__init__()
        self.damage_name = damage_name
        self.damage_value = damage_value
        self.setText(self.damage_name)
        self.clicked.connect(self.print_damage_value)

    def print_damage_value(self):
        print(self.damage_value)

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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("player.ico"))
        self.setWindowTitle("Destiny DPS Calculator")
        self.setGeometry(350, 100, 1920, 1080)
        self.setPalette(QPalette(QColor(22, 22, 22)))

        self.create_video_player()

    def create_video_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        video_widget = QVideoWidget()

        self.open_btn = QPushButton("Open Video")
        self.open_btn.clicked.connect(self.open_file)

        self.play_btn = QPushButton()
        self.play_btn.setEnabled(False)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.plus_frame_btn = QPushButton()
        self.plus_frame_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.plus_frame_btn.clicked.connect(self.advance_frame)

        self.minus_frame_btn = QPushButton()
        self.minus_frame_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.minus_frame_btn.clicked.connect(self.subtract_frame)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.play_btn)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.plus_frame_btn)
        hbox.addWidget(self.minus_frame_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(video_widget)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(video_widget)

        self.add_weapon_type_btn = QPushButton("Add Damage Type")
        self.add_weapon_type_btn.clicked.connect(self.open_damage_value_popup)

        self.sidebar = QVBoxLayout()
        self.sidebar.addWidget(self.add_weapon_type_btn)


        main_layout = QHBoxLayout()
        main_layout.addLayout(vbox)
        main_layout.addLayout(self.sidebar)

        self.setLayout(main_layout)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.play_btn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def advance_frame(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + int(1000.0 / 60.0))

    def subtract_frame(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - int(1000.0 / 60.0))

    def open_damage_value_popup(self):
        popup = PopupWindow()
        if popup.exec_() == QDialog.Accepted:
            damage_name = popup.text1.text()
            damage_value = int(popup.text2.text())
            damage_button = DamageTypeButton(damage_name, damage_value)
            self.sidebar.addWidget(damage_button)


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec_())
