from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QLabel, \
    QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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


class ChartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib Example")
        self.setGeometry(300, 200, 600, 400)

        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        fig = Figure()
        canvas = FigureCanvas(fig)

        layout.addWidget(canvas)

        self.plot_chart(fig)

    def plot_chart(self, fig):
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'b-o')

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Sample Chart')


class VideoWindow(QWidget):
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
        popup = PopupWindow()
        if popup.exec_() == QDialog.Accepted:
            damage_name = popup.text1.text()
            damage_value = int(popup.text2.text())
            damage_button = DamageTypeButton(damage_name, damage_value, self.video_player)
            self.sidebar.addWidget(damage_button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
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
