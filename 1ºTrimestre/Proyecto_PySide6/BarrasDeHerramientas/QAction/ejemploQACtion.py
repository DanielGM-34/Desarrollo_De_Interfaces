from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, 
)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout cuadrícula")
        

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()