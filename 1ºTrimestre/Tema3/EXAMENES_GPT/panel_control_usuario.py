from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Signal
import sys

# --- Widget derivado 1 ---
class CampoUsuario(QLineEdit):
    entradaInvalida = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._validar)

    def _validar(self):
        texto = self.text()
        if any(ch.isdigit() for ch in texto):
            self.entradaInvalida.emit("No se permiten números")

# --- Widget derivado 2 ---
class EtiquetaAviso(QLabel):
    def mostrarAviso(self, mensaje):
        self.setText(mensaje)
        self.setStyleSheet("color: red;")

    def limpiarAviso(self):
        self.setText("")
        self.setStyleSheet("color: black;")

# --- Widget derivado 3 ---
class BotonConfirmar(QPushButton):
    confirmado = Signal()

    def __init__(self, parent=None):
        super().__init__("Confirmar", parent)
        self.clicked.connect(self._emitir)

    def _emitir(self):
        self.confirmado.emit()

# --- Componente propio ---
class PanelProgreso(QWidget):
    def __init__(self):
        super().__init__()
        self.__porcentaje = 0

    def setPorcentaje(self, valor):
        self.__porcentaje = max(0, min(100, valor))
        self.update()

    def reset(self):
        self.__porcentaje = 0
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(10,10,-10,-10)

        # Fondo gris
        pen = QPen(QColor("gray"), 10)
        p.setPen(pen)
        p.drawArc(rect, 0, 16*360)

        # Progreso verde
        pen.setColor(QColor("green"))
        p.setPen(pen)
        p.drawArc(rect, 90*16, -16*360*self.__porcentaje/100)

# --- Ventana principal ---
class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Control de Usuario")
        layout = QVBoxLayout(self)

        self.aviso = EtiquetaAviso()
        self.campo = CampoUsuario()
        self.boton = BotonConfirmar()
        self.progreso = PanelProgreso()

        layout.addWidget(self.aviso)
        layout.addWidget(self.campo)
        layout.addWidget(self.boton)
        layout.addWidget(self.progreso)

        # Conexiones
        self.campo.entradaInvalida.connect(self._mostrarError)
        self.boton.confirmado.connect(self._aumentarProgreso)

    def _mostrarError(self, mensaje):
        self.aviso.mostrarAviso(mensaje)

    def _aumentarProgreso(self):
        self.aviso.limpiarAviso()
        nuevo = self.progreso._PanelProgreso__porcentaje + 20
        self.progreso.setPorcentaje(nuevo)

# --- Main ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("EXAMENES_GPT/estilos_control_usuario.qss") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("No se encontró panel_estilos.qss")
    ventana = Ventana()
    ventana.resize(300,300)
    ventana.show()
    app.exec()
