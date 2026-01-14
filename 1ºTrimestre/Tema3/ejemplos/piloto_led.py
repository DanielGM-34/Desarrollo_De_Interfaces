import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt

# ==============================================================================
# WIDGET PERSONALIZADO: LA LUZ
# ==============================================================================
class PilotoLed(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        
        # VARIABLE DE ESTADO (Lo único que necesitas controlar)
        self.encendido = False 

    def cambiar_estado(self):
        # Invertimos el valor: Si es True pasa a False, y viceversa
        self.encendido = not self.encendido
        
        # ¡OBLIGATORIO! Avisar a Qt para que borre y pinte de nuevo
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Para que el círculo se vea suave

        # 1. Elegir el color según el estado
        if self.encendido:
            color_relleno = QColor("red")      # Rojo brillante
            color_borde = QColor("#ffcccc")    # Borde clarito (brillo)
        else:
            color_relleno = QColor("#555555")  # Gris apagado
            color_borde = QColor("#333333")    # Borde oscuro

        # 2. Configurar el pincel
        painter.setBrush(QBrush(color_relleno))
        
        # Hacemos el borde grueso (ancho 5) para que se vea bien
        pluma = QPen(color_borde, 5)
        painter.setPen(pluma)

        # 3. Dibujar el círculo en el centro
        ancho = self.width()
        alto = self.height()
        
        # Calculamos el centro
        centro_x = ancho // 2
        centro_y = alto // 2
        radio = 50 # Tamaño fijo, fácil

        # drawEllipse(centro_x, centro_y, radio_x, radio_y)
        # OJO: drawEllipse con centro pide (Point, rx, ry) o (x, y, w, h) de la caja
        # La forma más fácil si te lías con coordenadas es usar la caja:
        
        # Caja centrada de 100x100 (radio 50)
        painter.drawEllipse(centro_x - 50, centro_y - 50, 100, 100)

        painter.end()

# ==============================================================================
# VENTANA PRINCIPAL
# ==============================================================================
class VentanaExamen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejercicio Simple: LED")
        self.resize(300, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 1. Añadimos nuestro widget pintado
        self.led = PilotoLed()
        layout.addWidget(self.led)

        # 2. Añadimos el botón de control
        self.boton = QPushButton("ENCENDER / APAGAR")
        self.boton.clicked.connect(self.accion_boton)
        layout.addWidget(self.boton)

    def accion_boton(self):
        # Llamamos al método del widget para que cambie su variable interna
        self.led.cambiar_estado()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaExamen()
    ventana.show()
    sys.exit(app.exec())