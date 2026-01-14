import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QTimer, QPoint

# ==============================================================================
# 1. WIDGET PERSONALIZADO: CÍRCULO QUE LATE
# ==============================================================================
class CirculoLatido(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        
        # VARIABLES DE ESTADO
        self.radio = 20          # Tamaño inicial
        self.creciendo = True    # ¿Se está haciendo grande o pequeño?
        
        # Configuración
        self.radio_min = 20
        self.radio_max = 100
        self.velocidad = 2       # Cuánto cambia por cada tic del reloj

    def paso_animacion(self):
        """Lógica matemática: Aumentar o disminuir el radio"""
        
        if self.creciendo:
            self.radio += self.velocidad
            # Si tocamos el techo, cambiamos de dirección
            if self.radio >= self.radio_max:
                self.creciendo = False
        else:
            self.radio -= self.velocidad
            # Si tocamos el suelo, cambiamos de dirección
            if self.radio <= self.radio_min:
                self.creciendo = True
        
        # ¡FUNDAMENTAL! Pedir repintado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Bordes suaves

        # 1. Fondo Negro (Para que destaque)
        painter.fillRect(self.rect(), QColor("#111"))

        # 2. Calcular el Centro exacto del widget
        # (Da igual si estiras la ventana, siempre estará en medio)
        centro_x = self.width() // 2
        centro_y = self.height() // 2
        centro = QPoint(centro_x, centro_y)

        # 3. Configurar Pincel (Rojo Corazón)
        color = QColor("#e74c3c")
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen) # Sin borde negro

        # 4. Dibujar el Círculo con el radio actual
        # drawEllipse(centro, radio_x, radio_y)
        painter.drawEllipse(centro, self.radio, self.radio)

        painter.end()

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaPulse(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulacro: Animación Básica")
        self.resize(350, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- Nuestro Widget ---
        self.latido = CirculoLatido()
        
        # --- Timer (El motor de la animación) ---
        self.timer = QTimer()
        self.timer.setInterval(20) # 20ms = Muy fluido (50 FPS aprox)
        # Conectamos el timer directamente a la función lógica del widget
        self.timer.timeout.connect(self.latido.paso_animacion)

        # --- Botón ---
        self.btn_accion = QPushButton("💓 Activar Latido")
        self.btn_accion.setCheckable(True) # Se queda pulsado
        self.btn_accion.setStyleSheet("font-size: 16px; padding: 10px;")
        self.btn_accion.clicked.connect(self.controlar_timer)

        layout.addWidget(self.latido)
        layout.addWidget(self.btn_accion)

    def controlar_timer(self):
        if self.btn_accion.isChecked():
            self.timer.start()
            self.btn_accion.setText("⏹ Detener")
        else:
            self.timer.stop()
            self.btn_accion.setText("💓 Activar Latido")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPulse()
    ventana.show()
    sys.exit(app.exec())