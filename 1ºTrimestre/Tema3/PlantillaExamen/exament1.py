import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, Signal

class PanelTermometro(QWidget):
    estadoCambiado = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__estado_actual = "frio"

        # --- Botón interno ---
        self.boton = QPushButton("Subir temperatura")
        self.boton.clicked.connect(self._cambiar_estado)

        # --- Layout principal ---
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addStretch()
        layout.addWidget(self.boton)

        self.setFixedSize(150, 300)

    def _cambiar_estado(self):
        estados = ["frio", "templado", "caliente"]
        i = estados.index(self.__estado_actual)
        self.__estado_actual = estados[(i + 1) % len(estados)]
        self.estadoCambiado.emit(self.__estado_actual)
        self.update()

    def estado(self):
        return self.__estado_actual

    def reiniciar(self):
        self.__estado_actual = "frio"
        self.estadoCambiado.emit(self.__estado_actual)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Color según estado
        color = {
            "frio": QColor("#3498db"),
            "templado": QColor("#f1c40f"),
            "caliente": QColor("#e74c3c")
        }[self.__estado_actual]

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)

        # Dibujar rectángulo del termómetro
        painter.drawRect(55, 20, 40, 180)

        # Dibujar círculo en la base
        painter.drawEllipse(45, 180, 60, 60)


# --- Ventana principal ---
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Termómetro")

        self.termometro = PanelTermometro()
        self.label_estado = QLabel("Estado actual: frío")

        # Conectar señal personalizada
        self.termometro.estadoCambiado.connect(self._actualizar_label)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.termometro)
        layout.addWidget(self.label_estado)
        self.setLayout(layout)

    def _actualizar_label(self, estado):
        self.label_estado.setText(f"Estado actual: {estado}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar estilos desde archivo externo
    # Cargar estilos desde archivo externo
with open("PlantillaExamen/dani_garcia_estilos_T3.qss", "r") as f:
    app.setStyleSheet(f.read())


    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
