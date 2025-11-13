# Daniel García Méndez 2ºDAM

from PySide6.QtWidgets import QApplication, QMainWindow,QPushButton
from PySide6.QtCore import QSize



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa principal.")
        boton = QPushButton("Encender")
        boton.setCheckable(True)
        self.setCentralWidget(boton)
        boton.clicked.connect(self.botonPresionado)
        boton.clicked.connect(self.encendido)


    def encendido(self, checked):
        if checked==True:
            self.setWindowTitle("Ventada encendida")
        else:
            self.setWindowTitle("Ventada apagada")

    def botonPresionado(self):
        print("Boton pulsado.")
    






app = QApplication([])
window = Window()
window.show() 
app.exec()