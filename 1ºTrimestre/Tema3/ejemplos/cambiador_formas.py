import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt

# ==============================================================================
# WIDGET PERSONALIZADO
# ==============================================================================
class FiguraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        
        # VARIABLE DE ESTADO (Booleana: True o False)
        self.es_circulo = True 

    def cambiar_forma(self):
        # Alternamos el valor: True -> False -> True...
        self.es_circulo = not self.es_circulo
        
        # ¡OBLIGATORIO! Pedir repintado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Definir el área de dibujo (un cuadrado en el centro con margen)
        margen = 40
        rect = self.rect().adjusted(margen, margen, -margen, -margen)

        # 2. Configurar borde común
        painter.setPen(QPen(Qt.black, 3))

        # 3. LÓGICA DE DIBUJO (IF / ELSE)
        if self.es_circulo:
            # Estado A: Círculo Azul
            painter.setBrush(QBrush(QColor("#3498db"))) # Azul
            painter.drawEllipse(rect)
        else:
            # Estado B: Cuadrado Naranja
            painter.setBrush(QBrush(QColor("#e67e22"))) # Naranja
            painter.drawRect(rect)

        painter.end()

# ==============================================================================
# VENTANA PRINCIPAL
# ==============================================================================
class VentanaFormas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Círculo vs Cuadrado")
        self.resize(300, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 1. Nuestro widget pintado
        self.figura = FiguraWidget()
        layout.addWidget(self.figura)

        # 2. Botón
        self.boton = QPushButton("CAMBIAR FORMA")
        self.boton.clicked.connect(self.accion_cambiar)
        layout.addWidget(self.boton)

    def accion_cambiar(self):
        # Llamamos al método del widget
        self.figura.cambiar_forma()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFormas()
    ventana.show()
    sys.exit(app.exec())