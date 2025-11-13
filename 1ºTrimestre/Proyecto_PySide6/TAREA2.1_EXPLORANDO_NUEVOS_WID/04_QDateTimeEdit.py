# Daniel García Méndez 2ºDAM 
from PySide6.QtWidgets import QApplication, QMainWindow, QDateTimeEdit
from PySide6.QtCore import QDateTime

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timeEdicion = QDateTimeEdit()
        self.timeEdicion.setDateTime(QDateTime.currentDateTime())

        self.timeEdicion.setDisplayFormat("dddd, d 'de' MMMM 'de' yyyy hh:mm")
        self.setCentralWidget(self.timeEdicion)

        self.timeEdicion.dateTimeChanged.connect(self.fecha_cambiada)


    def fecha_cambiada(self,fecha):
        print("La nueva fecha es: ", str(fecha))
        
app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()