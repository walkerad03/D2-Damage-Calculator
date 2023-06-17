"""
Main entrypoint to the program

Handles creation of the window and begins initialization of all other
custom modules.
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QDialog, QLineEdit, QLabel, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon
import sys

from video_player import VideoPlayer
from damage_type_button import DamageTypeButton
from chart_window import ChartWindow


class PopupWindow(QDialog):
    """
    A dialog window to create a new damage type.

    Attributes
    ----------
    label1: QLabel
    text1: QLineEdit
    label2: QLabel
    text2: QLineEdit
    ok_button: QPushButton
    layout: QVBoxLayout
    """
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


class VideoWindow(QWidget):
    """
    A window displayed in the video tab of the main window.

    Attributes
    ----------
    video_player: VideoPlayer
    add_weapon_type_btn: QPushButton
    sidebar: QVBoxLayout
    main_layout: QHBoxLayout

    Methods
    -------
    open_damage_value_popup()
        Handle creation of a new damage type.
    """
    def __init__(self):
        super().__init__()

        self.video_player = VideoPlayer()

        self.add_weapon_type_btn = QPushButton("Add Damage Type")
        self.add_weapon_type_btn.clicked.connect(self.open_damage_value_popup)

        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.addWidget(self.add_weapon_type_btn)
        self.sidebar.addStretch(1)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.video_player)
        main_layout.addLayout(self.sidebar)

        self.setLayout(main_layout)

    def open_damage_value_popup(self):
        """
        Handle creation of a new damage type.

        Spawns a popup window prompting the user to enter a name and
        damage value for the new damage type. Then creates a new button
        in the sidebar corresponding to that damage type.
        """
        popup = PopupWindow()
        if popup.exec_() == QDialog.Accepted:
            damage_name = popup.text1.text()
            damage_value = int(popup.text2.text())
            damage_button = DamageTypeButton(damage_name, damage_value, self.video_player)
            self.sidebar.addWidget(damage_button)


class MainWindow(QMainWindow):
    """
    Window responsible for displaying all UI features.

    The MainWindow class manages features related to the overall
    presentation of the application, such as app title and icon and
    default window size. The app also sets up tabs and assigns other
    widgets to each one.

    Attributes
    ----------
    tab_widget: QTabWidget
    video_tab: VideoWindow
    chart_tab: ChartWindow
    stats_tab: QWidget
    """
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("../icon.ico"))
        self.setWindowTitle("Destiny DPS Calculator")
        self.setGeometry(0, 0, 960, 540)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.video_tab = VideoWindow()
        self.chart_tab = ChartWindow()
        self.stats_tab = QWidget()

        self.tab_widget.addTab(self.video_tab, "Video Player")
        self.tab_widget.addTab(self.chart_tab, "DPS Chart (NOT DONE)")
        self.tab_widget.addTab(self.stats_tab, "Statistics (NOT DONE)")


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())
