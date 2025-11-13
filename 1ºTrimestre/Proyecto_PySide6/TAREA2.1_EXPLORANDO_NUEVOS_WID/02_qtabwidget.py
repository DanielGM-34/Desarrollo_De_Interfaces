# Daniel García Méndez 2ºDAM 
from PySide6.QtWidgets import QApplication, QMainWindow,QTabWidget,QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgetCentral = QTabWidget()
        self.pestanya1= QLabel("Bienvenido")
        self.pestanya2= QLabel("Segunda pestaña")
        self.pestanya3= QLabel("Tercera pestaña")

        self.setWindowTitle("Pestaña 1")

        self.setCentralWidget(self.widgetCentral)

        self.widgetCentral.addTab( self.pestanya1, "Pestanya1")
        self.widgetCentral.addTab( self.pestanya2, "Pestanya2")
        self.widgetCentral.addTab( self.pestanya3, "Pestanya3")

        self.widgetCentral.currentChanged.connect(self.cambio_pestanya)
    

    # Pongo str para que no me dé error en la conversión
    def cambio_pestanya(self, i):
        self.setWindowTitle("Pestaña" + str(i + 1))
        print("índice seleccionado", str(i))

        
app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()



