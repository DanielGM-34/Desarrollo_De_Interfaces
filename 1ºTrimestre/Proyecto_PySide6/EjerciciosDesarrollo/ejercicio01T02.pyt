# Daniel García Méndez 2ºDAM 
from PySide6.QtWidgets import QApplication, QMainWindow,QPushButton,QWidget
from PySide6.QtCore import QSize

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        boton = QPushButton("Pulsa!")
        boton.clicked.connect(self.botonPresionado)
        self.setCentralWidget(boton)
        # Ajustar tamaño
        self.setFixedSize(QSize(400,300))
        # self.setMinimumSize(QSize(600,400))
        # self.setMaximumSize(QSize(300,200))
        
    def botonPresionado(self):
        print("botón pulsado")

class VentanaSecundaria(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Secundaria")

        


app = QApplication([])
window = VentanaPrincipal()
window2 = VentanaSecundaria()
window.show() 
window2.show()
app.exec()

