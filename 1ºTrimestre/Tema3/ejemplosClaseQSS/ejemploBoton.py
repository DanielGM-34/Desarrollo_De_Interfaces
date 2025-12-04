from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication

class BotonContador(QPushButton):
    def __init__(self, parent=None):
        texto_inicial = "Pulsado 0 veces"
        super().__init__(texto_inicial, parent)
        self.__contador = 0
        self.clicked.connect(self._incrementar)

    def _incrementar(self):
        self.__contador = self.__contador + 1
        nuevo_texto = "Pulsado " + str(self.__contador) + " veces"
        self.setText(nuevo_texto)
        
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba de BotonContador")

        # Creamos el botón personalizado
        boton = BotonContador(self)

        # Lo establecemos como widget central de la ventana
        self.setCentralWidget(boton)

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()