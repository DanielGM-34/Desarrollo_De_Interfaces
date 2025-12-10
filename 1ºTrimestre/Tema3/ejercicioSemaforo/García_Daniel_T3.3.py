# Daniel García Méndez 2ºDAM

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel
)
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRect, Qt, QTimer


class Semaforo(QWidget):
    # Lista de colores del semáforo
    colores = ["rojo", "amarillo", "verde"]

    def __init__(self, parent=None):
        super().__init__(parent)

        # Estado inicial
        self.__estado_actual = self.colores[0]

        # Tamaño fijo del semáforo
        self.setFixedSize(120, 380)

        # Botón para cambiar color
        self.__boton_cambiar = QPushButton("Cambiar", self)
        self.__boton_cambiar.clicked.connect(self.__cambiar_estado)

        # Temporizador automático (1 segundo)
        self.__timer = QTimer(self)
        self.__timer.setInterval(1000)
        self.__timer.timeout.connect(self.__cambiar_estado)
        self.__timer.start()

        # Layout principal
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.__boton_cambiar, alignment=Qt.AlignCenter)

    # Métodos públicos para devolver el color y reiniciar el color.
    def estado(self):
        return self.__estado_actual

    def reiniciar(self):
        self.__estado_actual = self.colores[0]
        self.update()

    # Método para cambiar el color
    def __cambiar_estado(self):
        indice_actual = self.colores.index(self.__estado_actual)
        indice_siguiente = (indice_actual + 1) % len(self.colores)
        self.__estado_actual = self.colores[indice_siguiente]
        self.update()

    # Dibujo del semáforo
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Cuerpo del semáforo
        cuerpo_ancho = 90
        cuerpo_x = (self.width() - cuerpo_ancho) // 2
        cuerpo_y = 10
        cuerpo_alto = 250
        cuerpo_rect = QRect(cuerpo_x, cuerpo_y, cuerpo_ancho, cuerpo_alto)

        painter.setBrush(QColor("#272626"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(cuerpo_rect)

        # Definiciones de las luces
        luz_diametro = 60
        luz_radio = luz_diametro // 2
        centro_x = cuerpo_x + (cuerpo_ancho // 2)

        luces = [
            (cuerpo_y + 40, QColor("red"), "rojo"),
            (cuerpo_y + 125, QColor("yellow"), "amarillo"),
            (cuerpo_y + 210, QColor("green"), "verde")
        ]

        color_apagado = QColor("#5c5c5c")
        painter.setPen(QPen(QColor("#7f8c8d"), 1))

        for centro_y, color_luz, nombre_estado in luces:
            luz_x = centro_x - luz_radio
            luz_y = centro_y - luz_radio

            if nombre_estado == self.__estado_actual:
                painter.setBrush(color_luz)
            else:
                painter.setBrush(color_apagado)

            painter.drawEllipse(luz_x, luz_y, luz_diametro, luz_diametro)

        painter.end()


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Semáforo Automático Adaptado")
        self.resize(300, 450)

        # Instancia del semáforo
        self.semaforo = Semaforo()

        # Etiqueta para mostrar estado actual
        self.label_estado = QLabel(f"Estado: {self.semaforo.estado()}")
        self.label_estado.setAlignment(Qt.AlignCenter)

        # Botón para reiniciar
        self.boton_reiniciar = QPushButton("Reiniciar (Volver a Rojo)")
        self.boton_reiniciar.clicked.connect(self.__reiniciar_semaforo)

        # Layout central
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.semaforo, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_estado)
        layout.addWidget(self.boton_reiniciar)

        self.setCentralWidget(central_widget)

        # Conexiones para actualizar la etiqueta externa
        self.semaforo._Semaforo__timer.timeout.connect(self.__actualizar_interfaz_externa)
        self.semaforo._Semaforo__boton_cambiar.clicked.connect(self.__actualizar_interfaz_externa)

    def __actualizar_interfaz_externa(self):
        self.label_estado.setText(f"Estado: {self.semaforo.estado()}")

    def __reiniciar_semaforo(self):
        self.semaforo.reiniciar()
        self.__actualizar_interfaz_externa()


app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()
