# Daniel García Méndez 2ºDAM
from PySide6.QtWidgets import QApplication, QMainWindow, QDial

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.cadenaDial = QDial()
        self.cadenaDial.setRange(0, 10)
        self.cadenaDial.setNotchesVisible(True)
        self.cadenaDial.setValue(5) 

        
        self.cadenaDial.valueChanged.connect(self.cambiar_volumen)
        
        self.setCentralWidget(self.cadenaDial)
        
        self.cambiar_volumen(self.cadenaDial.value())

    def cambiar_volumen(self, volumenActual):
        self.setWindowTitle("Volumen: " +  str(volumenActual) + "/10")
        
        if volumenActual == 10:
            print("¡Volumen máximo alcanzado!")

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()
