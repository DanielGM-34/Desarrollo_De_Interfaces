#Daniel García Méndez 2º DAM
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventanita")

        textoAyuda = QTextEdit()

        self.textoA = textoAyuda

        #Si no centras el widget no aparecerá en pantalla
        self.setCentralWidget(textoAyuda)
        textoAyuda.setPlaceholderText("Escribe aquí tu mensaje...")

        # Texto que sale al principio
        textoAyuda.setPlainText("Bienvenido/a al editor de texto")
        textoAyuda.textChanged.connect(self.texto_modificado)



    def texto_modificado(self):
        texto_actual = self.textoA.toPlainText()
        print("Texto modificado", texto_actual)


app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()