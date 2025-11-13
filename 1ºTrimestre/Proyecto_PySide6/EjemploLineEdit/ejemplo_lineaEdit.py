from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PySide6.QtCore import QSize

class VentanaP(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo linea edit")

        texto = QLineEdit()
        texto.setMaxLength(40)
        texto.setPlaceholderText("Introduce un texto")
        self.setCentralWidget(texto)
        
        texto.returnPressed.connect(self.mostrar_mensaje)
        texto.textChanged.connect(self.texto_modificado)
        texto.textEdited.connect(self.texto_editado)

        self.texto=texto

    def mostrar_mensaje(self):
        print("Se pulsó ENTER")
        self.texto.setText("Hola!")

    def texto_modificado(self,s):
        print("Texto modificado ", s)

    def texto_editado(self,s):
        print("Texto editado por el usuario", s)

    

app= QApplication([])
window=VentanaP()
window.show()
app.exec()
