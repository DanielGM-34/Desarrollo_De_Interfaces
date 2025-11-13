from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PySide6.QtCore import QSize

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hOLA MUNDILLO")
        self.setMinimumSize(QSize(480,320))

        texto = QLineEdit()
        texto.textChanged.connect(self.texto_modificado)
        self.setCentralWidget(texto)

        self.texto= texto

    def texto_modificado(self):
        texto_recuperado=self.texto.text()
        self.setWindowTitle(texto_recuperado)
    

app=QApplication([])
windows = VentanaPrincipal()
windows.show()
app.exec()