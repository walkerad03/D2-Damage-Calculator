from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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