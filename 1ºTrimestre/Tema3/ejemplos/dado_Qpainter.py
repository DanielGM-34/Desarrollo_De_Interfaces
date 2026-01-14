import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QTimer, QRect

# ==============================================================================
# 1. WIDGET PERSONALIZADO: DADO DIBUJADO A MANO
# ==============================================================================
class DadoVisual(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200) # Tamaño cuadrado
        self.numero_actual = 1        # Estado inicial (Caras del 1 al 6)
        
        # Colores para dibujar
        self.color_dado = QColor("#fdfefe") # Blanco hueso
        self.color_puntos = QColor("#e74c3c") # Rojo
        self.color_borde = QColor("#2c3e50")  # Azul oscuro

    def set_numero(self, n):
        """Cambia el estado y fuerza el repintado"""
        if 1 <= n <= 6:
            self.numero_actual = n
            self.update() # ¡Llama a paintEvent!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Suavizar círculos

        # --- 1. DIBUJAR EL CUERPO DEL DADO ---
        rect = self.rect().adjusted(10, 10, -10, -10) # Dejamos margen
        
        painter.setPen(QPen(self.color_borde, 4)) # Borde grueso
        painter.setBrush(QBrush(self.color_dado)) # Relleno blanco
        painter.drawRoundedRect(rect, 20, 20)     # Cuadrado con bordes redondeados

        # --- 2. DIBUJAR LOS PUNTOS (Lógica Geométrica) ---
        painter.setBrush(QBrush(self.color_puntos))
        painter.setPen(Qt.NoPen) # Los puntos no tienen borde

        # Calculamos posiciones relativas al tamaño del widget
        w = self.width()
        h = self.height()
        
        # Coordenadas base (Centro, Izquierda, Derecha, Arriba, Abajo)
        cx, cy = w // 2, h // 2           # Centro absoluto
        izq = w // 4
        der = w * 3 // 4
        arr = h // 4
        abj = h * 3 // 4
        
        radio = 15 # Tamaño del punto

        # Lista de coordenadas donde dibujar según el número
        puntos_a_dibujar = []

        if self.numero_actual == 1:
            puntos_a_dibujar = [(cx, cy)]
            
        elif self.numero_actual == 2:
            puntos_a_dibujar = [(izq, arr), (der, abj)]
            
        elif self.numero_actual == 3:
            puntos_a_dibujar = [(izq, arr), (cx, cy), (der, abj)]
            
        elif self.numero_actual == 4:
            puntos_a_dibujar = [(izq, arr), (der, arr), 
                                (izq, abj), (der, abj)]
                                
        elif self.numero_actual == 5:
            puntos_a_dibujar = [(izq, arr), (der, arr), 
                                (cx, cy), 
                                (izq, abj), (der, abj)]
                                
        elif self.numero_actual == 6:
            puntos_a_dibujar = [(izq, arr), (der, arr), 
                                (izq, cy),  (der, cy), 
                                (izq, abj), (der, abj)]

        # Dibujamos los círculos en las coordenadas calculadas
        for x, y in puntos_a_dibujar:
            painter.drawEllipse(QPoint(x, y), radio, radio)

        painter.end()

# Necesitamos importar QPoint para dibujar los círculos
from PySide6.QtCore import QPoint

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaExamen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulacro: Dado Digital")
        self.resize(300, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Widget propio
        self.dado = DadoVisual()
        
        # Etiqueta texto
        self.lbl_info = QLabel("Pulsa para lanzar")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setFont(QFont("Arial", 14))

        # Botones
        self.btn_manual = QPushButton("🎲 Lanzar (Manual)")
        self.btn_manual.clicked.connect(self.accion_manual)

        self.btn_auto = QPushButton("🔄 Modo Automático (Barajar)")
        self.btn_auto.setCheckable(True)
        self.btn_auto.clicked.connect(self.accion_auto)

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(150) # Rápido para efecto de "barajar"
        self.timer.timeout.connect(self.evento_timer)

        layout.addWidget(self.dado)
        layout.addWidget(self.lbl_info)
        layout.addSpacing(20)
        layout.addWidget(self.btn_manual)
        layout.addWidget(self.btn_auto)

    def accion_manual(self):
        # Paramos el automático si estaba puesto
        if self.timer.isActive():
            self.timer.stop()
            self.btn_auto.setChecked(False)
            self.btn_auto.setText("🔄 Modo Automático")

        nuevo_num = random.randint(1, 6)
        self.dado.set_numero(nuevo_num)
        self.lbl_info.setText(f"Resultado: {nuevo_num}")

    def accion_auto(self):
        if self.btn_auto.isChecked():
            self.timer.start()
            self.btn_auto.setText("⏹ Detener")
            self.btn_manual.setEnabled(False) # Bloqueamos manual mientras gira
            self.lbl_info.setText("Barajando...")
        else:
            self.timer.stop()
            self.btn_auto.setText("🔄 Modo Automático")
            self.btn_manual.setEnabled(True)
            # Resultado final al parar
            num_final = random.randint(1, 6)
            self.dado.set_numero(num_final)
            self.lbl_info.setText(f"¡Ha salido un {num_final}!")

    def evento_timer(self):
        # Cambia el número rápidamente para animar
        num = random.randint(1, 6)
        self.dado.set_numero(num)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaExamen()
    ventana.show()
    sys.exit(app.exec())