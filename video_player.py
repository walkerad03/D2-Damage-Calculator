from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QStyle, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()
        self.media_player.setVideoOutput(video_widget)
        self.media_player.stateChanged.connect(self.mediastate_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        self.open_video_button = QPushButton("Open Video")
        self.open_video_button.clicked.connect(self.open_file)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.minus_frame_button = QPushButton()
        self.minus_frame_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.minus_frame_button.clicked.connect(self.subtract_frame)

        self.plus_frame_button = QPushButton()
        self.plus_frame_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.plus_frame_button.clicked.connect(self.advance_frame)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)

        bottom_bar.addWidget(self.open_video_button)
        bottom_bar.addWidget(self.play_button)
        bottom_bar.addWidget(self.slider)
        bottom_bar.addWidget(self.minus_frame_button)
        bottom_bar.addWidget(self.plus_frame_button)

        vbox = QVBoxLayout()
        vbox.addWidget(video_widget)
        vbox.addLayout(bottom_bar)

        self.setLayout(vbox)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.play_button.setEnabled(True)

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediastate_changed(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def advance_frame(self):
        self.media_player.setPosition(self.media_player.position() + int(1000.0 / 60.0))

    def subtract_frame(self):
        self.media_player.setPosition(self.media_player.position() - int(1000.0 / 60.0))
