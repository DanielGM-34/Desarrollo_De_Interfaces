from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel,QWidget,QPushButton
from PySide6.QtCore import QSize



# QVBoxLayout
# QHBoxLayout
# QGridLayout
# QFormLayout
# QStackedLayout

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout vertical")

        layoutVertical = QVBoxLayout()

        componente_principal=QWidget()

        componente_principal.setLayout(layoutVertical)

        self.setCentralWidget(componente_principal)

        boton1=QPushButton("Uno")
        # altura
        boton1.setFixedHeight(50)



        layoutVertical.addWidget(boton1)
        layoutVertical.addWidget(QPushButton("Dos"))
        layoutVertical.addWidget(QPushButton("Tres"))
        layoutVertical.addWidget(QPushButton("Cuatro"))
        layoutVertical.addWidget(QPushButton("Cinco"))

        print()


app=QApplication([])
windows = VentanaPrincipal()
windows.show()
app.exec()