from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle


class DamageTypeButton(QWidget):
    def __init__(self, damage_name: str, damage_value: int):
        super().__init__()
        self.damage_name = damage_name
        self.damage_value = damage_value

        name_button = QPushButton(self.damage_name)
        delete_button = QPushButton()
        delete_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(name_button)
        hbox.addWidget(delete_button)

        self.setLayout(hbox)

        name_button.clicked.connect(self.print_damage_value)
        delete_button.clicked.connect(self.delete_widget)

    def print_damage_value(self):
        print(self.damage_value)

    def delete_widget(self):
        self.deleteLater()
