# Daniel García Méndez 2ºDAM 
from PySide6.QtWidgets import QApplication, QMainWindow, QDateTimeEdit, QSlider
from PySide6.QtCore import QDateTime

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Deslizador = QSlider()
        self.Deslizador.setRange(0,100)
        self.Deslizador.setValue(50)
        self.Deslizador.valueChanged.connect(self.cambiar_brillo)


        self.setCentralWidget(self.Deslizador)


    def cambiar_brillo(self, valor):
        self.setWindowTitle("Brillo actual " + str (valor))

        print("Nivel de brillo " + str(valor))



        
app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()