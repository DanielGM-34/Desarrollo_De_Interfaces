import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Signal

class BotonContador(QPushButton):
    contador_actualizado=Signal(int)
    def __init__(self,parent=None): 
        super().__init__("Pulsado 0 veces", parent)
        self.__contador=0
        self.clicked.connect(self.__incrementar)

    def __incrementar(self):
        self.__contador=self.__contador+1
        nuevo_texto="Pulsado " + str(self.__contador) + " veces."
        self.setText(nuevo_texto)

        self.contador_actualizado.emit(self.__contador)
    
    def contador(self):
        return self.__contador
    

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba de botón contador con señal personalizada.")

        contenedor = QWidget()
        layout = QVBoxLayout()

        self.boton = BotonContador()
        self.etiqueta= QLabel("Aún no has pulsado el botón.")

        self.boton.contador_actualizado.connect(self.actualizar_etiqueta)
        layout.addWidget(self.boton)
        layout.addWidget(self.etiqueta)
        
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

    def actualizar_etiqueta(self,valor):
        self.etiqueta.setText("La señal avisó: contador = " + str(valor))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
