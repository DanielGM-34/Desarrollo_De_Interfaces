import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QPushButton
)
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRect, Qt


class IndicadorSimple(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Texto que se mostrará dentro del círculo.
        # Se puede cambiar desde fuera con setTexto().
        self._texto = "OK"

    def setTexto(self, texto):
        # Guardamos el nuevo texto.
        self._texto = texto
        # update() avisa a Qt de que debe volver a dibujar el widget.
        self.update()

    def paintEvent(self, event):
        # QPainter es el objeto que permite dibujar dentro del widget.
        painter = QPainter(self)

        # Activamos el suavizado de bordes para evitar formas “dentadas”.
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Configuramos el color de relleno del círculo (verde).
        painter.setBrush(QColor("#4CAF50"))

        # Borde del círculo en color negro.
        painter.setPen(QPen(Qt. GlobalColor.black))

        # Calculamos el tamaño máximo posible de un cuadrado dentro del widget.
        # Esto asegura que el círculo no se deforme aunque el widget no sea cuadrado.
        lado = min(self.width(), self.height())

        # Creamos un rectángulo cuadrado, centrado en el widget.
        recto = QRect(
            (self.width() - lado) // 2,   # posición X centrada
            (self.height() - lado) // 2,  # posición Y centrada
            lado,                         # ancho del cuadrado
            lado                          # alto del cuadrado
        ) 
        # Dibujamos el círculo dentro del rectángulo calculado.
        painter.drawEllipse(recto)

        # Cambiamos el lápiz para dibujar texto en blanco.
        painter.setPen(QPen(Qt.GlobalColor.white))

        # Dibujamos el texto centrado dentro del círculo mediante AlignCenter.
        painter.drawText(recto, Qt.AlignmentFlag.AlignCenter, self._texto)
        
    
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo 2: Indicador con Texto")
        self.resize(300, 300)

        contenedor = QWidget(self)
        layout = QVBoxLayout(contenedor)

        # Nuestro widget personalizado
        self.indicador = IndicadorSimple(self)

        # Botón opcional para cambiar el texto
        boton = QPushButton("Cambiar texto")
        boton.clicked.connect(self.cambiar_texto)

        layout.addWidget(self.indicador)
        layout.addWidget(boton)

        self.setCentralWidget(contenedor)

    def cambiar_texto(self):
        # Cambiamos el texto para demostrar el update()
        self.indicador.setTexto("READY") 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
    