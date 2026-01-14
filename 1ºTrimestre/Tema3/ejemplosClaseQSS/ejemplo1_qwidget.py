from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow
)
from PySide6.QtCore import Qt
import sys


class ContadorSimple(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__valor = 0

        self.__etiqueta = QLabel("0", self)
        self.__etiqueta.setAlignment(Qt.AlignCenter)

        self.__boton_mas = QPushButton("+", self)
        self.__boton_menos = QPushButton("-", self)

        self.__boton_mas.clicked.connect(self.__incrementar)
        self.__boton_menos.clicked.connect(self.__decrementar)

        layout = QHBoxLayout(self)
        layout.addWidget(self.__boton_menos)
        layout.addWidget(self.__etiqueta)
        layout.addWidget(self.__boton_mas)

    def __incrementar(self):
        self.__valor = self.__valor + 1
        self.__etiqueta.setText(str(self.__valor))

    def __decrementar(self):
        self.__valor = self.__valor - 1
        self.__etiqueta.setText(str(self.__valor))

    def valor(self):
        return self.__valor

    def reiniciar(self): 
        self.__valor = 0
        self.__etiqueta.setText("0")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo: Contador Simple con QMainWindow")

        # Crear widget central
        contenedor = QWidget(self)
        layout = QVBoxLayout(contenedor)

        self.contador = ContadorSimple(self)
        self.boton_reiniciar = QPushButton("Reiniciar")
        self.boton_reiniciar.clicked.connect(self.__reiniciar_contador)

        layout.addWidget(self.contador)
        layout.addWidget(self.boton_reiniciar)

        # Asignar el widget al área central del QMainWindow
        self.setCentralWidget(contenedor)

    def __reiniciar_contador(self):
        self.contador.reiniciar()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())

