import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel
)
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QPolygon, QLinearGradient
)
from PySide6.QtCore import Qt, QPoint, QRect

# ==============================================================================
# 1. WIDGET PINTADO: FORMAS GEOMÉTRICAS
# ==============================================================================
class VisorFormas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.forma_actual = "cuadrado" # Opciones: cuadrado, triangulo, rombo

    def cambiar_forma(self):
        """Alterna entre las 3 formas cíclicamente"""
        if self.forma_actual == "cuadrado":
            self.forma_actual = "triangulo"
        elif self.forma_actual == "triangulo":
            self.forma_actual = "rombo"
        else:
            self.forma_actual = "cuadrado"
        
        self.update() # ¡Repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        rect = self.rect().adjusted(20, 20, -20, -20) # Margen de seguridad

        # --- 1. CREAR UN DEGRADADO (Gradient) ---
        # Se define desde (0,0) hasta (w,h) -> Diagonal
        gradiente = QLinearGradient(0, 0, w, h)
        gradiente.setColorAt(0.0, QColor("#ff9a9e"))  # Color inicio (Rosa)
        gradiente.setColorAt(1.0, QColor("#fecfef"))  # Color final (Lila suave)
        # Puedes añadir más paradas:
        # gradiente.setColorAt(0.5, QColor("white"))

        # --- 2. CONFIGURAR PINCEL Y BROCHA ---
        painter.setBrush(QBrush(gradiente)) # Relleno con degradado
        
        pluma = QPen(QColor("#555"), 4)     # Color gris, grosor 4
        pluma.setStyle(Qt.DashLine)         # Línea Discontinua (- - -)
        painter.setPen(pluma)

        # --- 3. DIBUJAR LA FORMA ELEGIDA ---
        
        if self.forma_actual == "cuadrado":
            # Rectángulo simple
            painter.drawRect(rect)

        elif self.forma_actual == "triangulo":
            # Para un triángulo necesitamos 3 puntos:
            # 1. Arriba centro
            p1 = QPoint(w // 2, 20) 
            # 2. Abajo izquierda
            p2 = QPoint(20, h - 20)
            # 3. Abajo derecha
            p3 = QPoint(w - 20, h - 20)
            
            # Creamos el polígono con esos puntos
            triangulo = QPolygon([p1, p2, p3])
            painter.drawPolygon(triangulo)

        elif self.forma_actual == "rombo":
            # Para un rombo necesitamos 4 puntos (centros de cada lado):
            p1 = QPoint(w // 2, 20)      # Arriba
            p2 = QPoint(w - 20, h // 2)  # Derecha
            p3 = QPoint(w // 2, h - 20)  # Abajo
            p4 = QPoint(20, h // 2)      # Izquierda
            
            rombo = QPolygon([p1, p2, p3, p4])
            painter.drawPolygon(rombo)

        painter.end()

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaGeometria(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formas y Degradados")
        self.resize(350, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Widget personalizado
        self.visor = VisorFormas()
        
        # Etiqueta
        self.lbl_info = QLabel("Forma: Cuadrado")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Botón
        self.btn_cambiar = QPushButton("Cambiar Forma")
        self.btn_cambiar.setStyleSheet("padding: 10px; background-color: #ddd;")
        self.btn_cambiar.clicked.connect(self.accion_cambiar)

        layout.addWidget(self.lbl_info)
        layout.addWidget(self.visor)
        layout.addWidget(self.btn_cambiar)

    def accion_cambiar(self):
        self.visor.cambiar_forma()
        # Actualizamos el texto según el estado interno del widget
        texto = self.visor.forma_actual.capitalize()
        self.lbl_info.setText(f"Forma: {texto}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGeometria()
    ventana.show()
    sys.exit(app.exec())