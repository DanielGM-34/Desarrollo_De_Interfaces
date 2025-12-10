# Daniel García Méndez 2ºDAM

import sys
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QMainWindow
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from PySide6.QtCore import Qt

class PanelSemaforo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Estado inicial del semáforo
        self.__estado_actual = "rojo"   
        self.setMinimumSize(200, 400)

        # Botón para avanzar al siguiente color
        boton_cambiar = QPushButton("Cambiar")
        # Botón conectado con la función de cambiar color.
        boton_cambiar.clicked.connect(self.avanzar_color)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addStretch()
        layout_principal.addWidget(boton_cambiar)
        self.setLayout(layout_principal)


    # método para cambiar los colores del semáforo
    def avanzar_color(self):
        if self.__estado_actual == "rojo":
            self.__estado_actual = "amarillo"
        elif self.__estado_actual == "amarillo":
            self.__estado_actual = "verde"
        else:
            self.__estado_actual = "rojo"

        # update actualiza el color del semásofo.
        self.update()  


    # Funcion para pintar las luces del semáforo y ajustar sus dimensiones.
    def paintEvent(self, event):
        painter = QPainter(self)

        # Tamaño de cada luz
        radio = 35
        # Calcular posición X para centrar las luces
        x = self.width() // 2 - radio
        # Posición inicial en Y y separación entre luces
        y_inicial = 30
        espacio = 85

        # Dibujar fondo del semáforo (rectángulo)
        ancho = radio * 2 + 30
        alto = espacio * 2 + radio * 2 + 30
        painter.setBrush(QColor(40, 40, 40))
        painter.drawRect(x - 15, y_inicial - 15, ancho, alto)

        # Dibujar luz roja
        color = QColor("red") if self.__estado_actual == "rojo" else QColor("gray")
        painter.setBrush(color)
        painter.drawEllipse(x, y_inicial, radio*2, radio*2)

        # Dibujar luz amarilla
        color = QColor("yellow") if self.__estado_actual == "amarillo" else QColor("gray")
        painter.setBrush(color)
        painter.drawEllipse(x, y_inicial + espacio, radio*2, radio*2)
 
        # Dibujar luz verde
        color = QColor("green") if self.__estado_actual == "verde" else QColor("gray")
        painter.setBrush(color)
        painter.drawEllipse(x, y_inicial + espacio*2, radio*2, radio*2)


# Getter del color actual.
    def estado(self):
        return self.__estado_actual


# Devuelve el color inicial del semáforo.
    def reiniciar(self):
        self.__estado_actual = "rojo"
        self.update()


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semáforo sin timer.")
        self.setMinimumSize(600,200)

        # Widget que contendrá un layout con el semáforo.
        contenedor = QWidget()
        layout_central = QVBoxLayout()

        # Crear semáforo
        self.widget_semaforo = PanelSemaforo()
        layout_central.addWidget(self.widget_semaforo)

        # Botón para reiniciar
        reiniciar_semaforo = QPushButton("Reiniciar semáforo")
        reiniciar_semaforo.clicked.connect(self.widget_semaforo.reiniciar)
        layout_central.addWidget(reiniciar_semaforo)

        contenedor.setLayout(layout_central)
        self.setCentralWidget(contenedor)


app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()