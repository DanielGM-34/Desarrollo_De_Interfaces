# Daniel García Méndez 2ºDAM
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventanitaaa")

        texto = QLineEdit()
        texto.setMaxLength(20)
        texto.setPlaceholderText("Escribe tu ciudad")
        self.setCentralWidget(texto)

        texto.returnPressed.connect(self.cambiar_titulo)
        texto.textChanged.connect(self.texto_modificado)

        self.texto = texto

    def cambiar_titulo(self):
        texto = self.texto.text()
        if texto == "":
            self.setWindowTitle("Sin ciudad")
        else:
            self.setWindowTitle(texto)

    def texto_modificado(self, s):
        print("Texto modificado", s)

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()
