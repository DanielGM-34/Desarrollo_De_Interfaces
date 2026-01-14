import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QCheckBox, QRadioButton, QComboBox, QListWidget, QTableWidget,
    QTableWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QDateEdit, QTimeEdit
)
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRect, Qt
from PySide6.QtCore import Signal

# --- Botón contador con señal personalizada ---

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

class BotonAgregarIncidencia(QPushButton):
    contador_actualizado = Signal(int)
    def __init__(self):
        super().__init__("Añadir incidencia")
        self.__contador = 0
        self.clicked.connect(self._incrementar)

    def _incrementar(self):
        self.__contador += 1
        self.contador_actualizado.emit(self.__contador)

    def __numVeces(self):
        return self.__contador
    
    def reiniciar(self):
        self.__contador = 0


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
        main_layout = QVBoxLayout()
        self.contenedor = QWidget ()
        self.circuloAviso = IndicadorSimple()
        self.etiquetaAviso= QLabel("Incidencias abiertas")
        self.painterCirculo = QPainter(self.circuloAviso)
        self.setMinimumSize(60,400)

        main_layout.addWidget(self.circuloAviso)
        
        # Botón agregar incidencia
        self.boton = BotonAgregarIncidencia()
        # Boton reset incidencia
        self.boton_reset = QPushButton("Reset")
        
        self.boton.contador_actualizado.connect(self.actualizar_etiqueta)
        self.boton_reset.clicked.connect(self.__reiniciar_contador)


        main_layout.addWidget(self.etiquetaAviso)
        main_layout.addWidget(self.boton)

        main_layout.addWidget(self.boton_reset)

        self.contenedor.setLayout(main_layout)
        self.setCentralWidget(self.contenedor)

    def __reiniciar_contador(self): 
        self.boton.reiniciar()
        self.etiquetaAviso.setText("Incidencias abiertas: " + str(0))
        self.circuloAviso.setTexto("OK")

    def actualizar_etiqueta(self,valor):
        self.etiquetaAviso.setText("Incidencias abiertas: " + str(valor))

        if(valor<=3):
            self.circuloAviso.setTexto("OK")

        elif(valor==4 and valor<=7 ):
            self.circuloAviso.setTexto("AVISO")

        elif(valor >7):
            self.circuloAviso.setTexto("ERROR")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("EXAMEN_HOY/Garcia_Daniel_Ext3.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())