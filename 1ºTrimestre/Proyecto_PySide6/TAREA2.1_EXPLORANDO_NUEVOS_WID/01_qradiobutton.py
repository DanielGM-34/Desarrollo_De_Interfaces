#Daniel García Méndez 2º DAM
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi aplicación radio botón.")

        
        # Muestra el texto por defecto
        self.botonConTexto=QRadioButton("Activar función")
        self.botonConTexto.setChecked(False)


        self.botonConTexto.toggled.connect(self.toggle) 
        self.botonConTexto.text()


        self.setCentralWidget(self.botonConTexto)

    def toggle(self, cheked):
        if cheked:
            self.setWindowTitle("Funcion ACTIVADA")
        
        else:
            self.setWindowTitle("Funcion DESACTIVADA")

app= QApplication([])
window=VentanaPrincipal()
window.show()
app.exec()
        




