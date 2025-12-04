import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Signal


class AreaTextoLimitada(QTextEdit):
    longitudCambiada = Signal(int)
    limiteSuperado = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._max_caracteres = 200
        self.setPlaceholderText("Escribe tu nota...")
        self.textChanged.connect(self._cuando_cambia_texto)
        self._actualizar_color_fondo(0)

    def obtenerMaxCaracteres(self):
        return self._max_caracteres

    def _cuando_cambia_texto(self):
        texto = self.toPlainText()
        longitud = len(texto)
        self.longitudCambiada.emit(longitud)
        superado = longitud > self._max_caracteres
        self.limiteSuperado.emit(superado)
        self._actualizar_color_fondo(longitud)

    def _actualizar_color_fondo(self, longitud):
        pal = self.palette()
        if self._max_caracteres == 0:
            ratio = 0
        else:
            ratio = float(longitud) / float(self._max_caracteres)

        if ratio < 0.8:
            color = QColor(230, 240, 250)
        elif ratio <= 1.0:
            color = QColor(255, 250, 200)
        else:
            color = QColor(255, 210, 220)

        pal.setColor(QPalette.ColorRole.Base, color)
        self.setPalette(pal)


class EtiquetaContadorCaracteres(QLabel):
    def __init__(self, maxCaracteresTextEditClase, parent=None):
        super().__init__(parent)
        self._max_caracteres = maxCaracteresTextEditClase
        self.actualizarContador(0)

    def actualizarContador(self, longitud_actual):
        self.setText("Caracteres : " + str(longitud_actual) + " / " + str(self._max_caracteres))
        self.cambiaColorDeTexto(longitud_actual)

    def cambiaColorDeTexto(self, longitud_actual):
        paletaDeColores = self.palette()
        if self._max_caracteres == 0:
            ratio = 0
        else:
            ratio = (longitud_actual) / (self._max_caracteres)
        if ratio < 0.8:
            color = QColor("black")
        elif ratio <= 1.0:
            color = QColor(255, 140, 0)
        else:
            color = QColor("red")

        paletaDeColores.setColor(QPalette.ColorRole.WindowText, color)
        self.setPalette(paletaDeColores)


class BotonLimpiarAviso(QPushButton):
    textoLimpiado = Signal()

    def __init__(self, area_texto, parent=None):
        super().__init__(parent)
        self._area_texto = area_texto
        self.setText("Limpiar texto")
        self._color_normal = QColor(220, 220, 220)
        self._color_ok = QColor(200, 255, 200)
        self._aplicar_color(self._color_normal)
        self.clicked.connect(self.texto_limpiado)

    def _aplicar_color(self, color):
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Button, color)
        self.setPalette(pal)

    def texto_limpiado(self):
        self._area_texto.clear()
        self._aplicar_color(self._color_ok)
        self.textoLimpiado.emit()

    def restablecerApariencia(self):
        self._aplicar_color(self._color_normal)


class EditorNotasConAvisos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de notas con avisos")
 
        self.area_texto = AreaTextoLimitada()
        self.etiqueta_contador = EtiquetaContadorCaracteres(self.area_texto.obtenerMaxCaracteres())
        self.boton_limpiar = BotonLimpiarAviso(self.area_texto)
        self.etiqueta_mensaje = QLabel("Escribe, como te pases los colores cambiarán.")

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta_contador)
        layout.addWidget(self.area_texto)
        layout.addWidget(self.boton_limpiar)
        layout.addWidget(self.etiqueta_mensaje)
        self.setLayout(layout) 

        self.area_texto.longitudCambiada.connect(self.etiqueta_contador.actualizarContador)
        self.area_texto.limiteSuperado.connect(self._gestionarLimiteSuperado)
        self.boton_limpiar.textoLimpiado.connect(self._mostrarMensajeLimpieza)

    def _gestionarLimiteSuperado(self, superado):
        if not superado:
            self.boton_limpiar.restablecerApariencia()

    def _mostrarMensajeLimpieza(self):
        self.etiqueta_mensaje.setText("Texto limpiado mediante el botón.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = EditorNotasConAvisos()
    ventana.resize(500, 400)
    ventana.show()
    sys.exit(app.exec())
