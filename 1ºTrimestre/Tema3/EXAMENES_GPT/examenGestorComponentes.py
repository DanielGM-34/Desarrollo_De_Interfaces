from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtGui import QPainter, QColor, QPalette
from PySide6.QtCore import Signal
import sys

# --- Widget derivado 1 ---
class AreaTextoLimitada(QTextEdit):
    longitudCambiada = Signal(int)
    limiteSuperado = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.maximo = 200
        self.textChanged.connect(self._comprobar)

    def _comprobar(self):
        longitud = len(self.toPlainText())
        self.longitudCambiada.emit(longitud)
        self.limiteSuperado.emit(longitud > self.maximo)

        paleta = self.palette()
        if longitud <= int(0.8 * self.maximo):
            paleta.setColor(QPalette.Base, QColor("white"))
        elif longitud <= self.maximo:
            paleta.setColor(QPalette.Base, QColor("yellow"))
        else:
            paleta.setColor(QPalette.Base, QColor("red"))
        self.setPalette(paleta)

# --- Widget derivado 2 ---
class EtiquetaContadorCaracteres(QLabel):
    def actualizar(self, longitud, maximo=200):
        self.setText(f"Caracteres: {longitud}/{maximo}")
        paleta = self.palette()
        if longitud <= int(0.8 * maximo):
            paleta.setColor(QPalette.WindowText, QColor("black"))
        elif longitud <= maximo:
            paleta.setColor(QPalette.WindowText, QColor("orange"))
        else:
            paleta.setColor(QPalette.WindowText, QColor("red"))
        self.setPalette(paleta)

# --- Widget derivado 3 ---
class BotonLimpiarAviso(QPushButton):
    textoLimpiado = Signal()

    def __init__(self, area, parent=None):
        super().__init__("Limpiar texto", parent)
        self.area = area
        self.clicked.connect(self._limpiar)

    def _limpiar(self):
        self.area.clear()
        paleta = self.palette()
        paleta.setColor(QPalette.Button, QColor("lightgreen"))
        self.setPalette(paleta)
        self.textoLimpiado.emit()

# --- Componente propio ---
class PanelSemaforo(QWidget):
    def __init__(self):
        super().__init__()
        self.__estado_actual = "rojo"
        self.boton = QPushButton("Cambiar")
        self.boton.clicked.connect(self._cambiar)

        layout = QVBoxLayout(self)
        layout.addWidget(self.boton)

    def estado(self): 
        return self.__estado_actual

    def reiniciar(self): 
        self.__estado_actual = "rojo"
        self.update()

    def _cambiar(self):
        ciclo = ["rojo","amarillo","verde"]
        i = ciclo.index(self.__estado_actual)
        self.__estado_actual = ciclo[(i+1)%3]
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for i,c in enumerate(["rojo","amarillo","verde"]):
            color = QColor(c) if self.__estado_actual==c else QColor("gray")
            p.setBrush(color)
            p.drawEllipse(50,30+i*60,40,40)

# --- Ventana principal ---
class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Componentes")
        layout = QVBoxLayout(self)

        self.contador = EtiquetaContadorCaracteres()
        self.texto = AreaTextoLimitada()
        self.boton = BotonLimpiarAviso(self.texto)
        self.semaforo = PanelSemaforo()

        layout.addWidget(self.contador)
        layout.addWidget(self.texto)
        layout.addWidget(self.boton)
        layout.addWidget(self.semaforo)

        # Conexiones sin lambda
        self.texto.longitudCambiada.connect(self._actualizarContador)
        self.boton.textoLimpiado.connect(self._mensajeTextoLimpiado)

    def _actualizarContador(self, longitud):
        self.contador.actualizar(longitud)

    def _mensajeTextoLimpiado(self):
        self.contador.setText("Texto limpiado")

# --- Main ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("EXAMENES_GPT/estilos.qss") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("No se encontró estilos.qss, se ejecuta sin estilos externos.")
    ventana = Ventana()
    ventana.show()
    app.exec()
