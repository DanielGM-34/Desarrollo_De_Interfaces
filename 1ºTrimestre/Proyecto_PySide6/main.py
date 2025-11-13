from PySide6.QtWidgets import QApplication, QMainWindow,QPushButton
from PySide6.QtCore import QSize

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        boton = QPushButton("Pulsa!")
        self.setCentralWidget(boton)

        # Ajustar tamaño
        # self.setFixedSize(QSize(400,300))
        self.setMinimumSize(QSize(600,400))
        self.setMaximumSize(QSize(300,200))


app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()