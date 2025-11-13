# Daniel García Méndez 2ºDAM 

from PySide6.QtWidgets import QApplication, QMainWindow,QPushButton
from PySide6.QtCore import QSize



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa principal.")
        self.boton = QPushButton("Pulsar")
        self.boton.setCheckable(True)

        self.setCentralWidget(self.boton)

        self.boton.clicked.connect(self.encendido)

    def botonPresionado(self):
        print("Boton pulsado.") 
    
    def encendido(self, checked):
        if checked==True:
            self.boton.setText("Soltar")  
            print("Boton pulsado.") 

        else:
            self.boton.setText("Pulsar")  
            print("Boton liberado.") 

app = QApplication([])
window = Window()
window.show() 
app.exec()