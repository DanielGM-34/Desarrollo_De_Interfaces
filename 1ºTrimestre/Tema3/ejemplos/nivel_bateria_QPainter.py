import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QSlider, QPushButton
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRect, QTimer

# ==============================================================================
# 1. WIDGET BATERÍA (PINTADO)
# ==============================================================================
class BateriaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 150)
        self.nivel = 50 # Porcentaje inicial (0-100)

    def set_nivel(self, valor):
        # Limitamos para que no se salga del rango
        self.nivel = max(0, min(100, valor))
        self.update() # ¡Repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones del widget
        w = self.width()
        h = self.height()

        # 1. Definir área de la batería (dejando margen)
        margen = 20
        # El cuerpo ocupa casi todo el ancho menos un poco para la punta
        rect_cuerpo = QRect(margen, margen, w - 2*margen - 20, h - 2*margen)
        
        # 2. Dibujar el CONTORNO (Cuerpo)
        pen_grueso = QPen(Qt.black, 4)
        painter.setPen(pen_grueso)
        painter.setBrush(Qt.NoBrush) # Hueco por dentro
        painter.drawRect(rect_cuerpo)

        # 3. Dibujar el POLO POSITIVO (La punta a la derecha)
        # Se coloca pegado al lado derecho del cuerpo
        rect_punta = QRect(rect_cuerpo.right(), rect_cuerpo.center().y() - 15, 15, 30)
        painter.setBrush(QBrush(Qt.black)) # Relleno negro sólido
        painter.drawRect(rect_punta)

        # 4. Dibujar la CARGA (El relleno)
        # Lógica de Color
        if self.nivel <= 20:
            color = QColor("#e74c3c") # Rojo (Crítico)
        elif self.nivel <= 50:
            color = QColor("#f39c12") # Naranja (Medio)
        else:
            color = QColor("#2ecc71") # Verde (Bien)

        painter.setPen(Qt.NoPen) # Sin borde para el líquido
        painter.setBrush(QBrush(color))

        # Calcular ancho según porcentaje
        # Ancho máximo disponible = ancho del cuerpo - un poquito de margen interno (4px)
        ancho_maximo = rect_cuerpo.width() - 4
        ancho_actual = int((self.nivel / 100) * ancho_maximo)

        # Dibujar rectángulo de carga (con un pequeño margen de 2px dentro del cuerpo)
        if self.nivel > 0:
            painter.drawRect(
                rect_cuerpo.x() + 2, 
                rect_cuerpo.y() + 2, 
                ancho_actual, 
                rect_cuerpo.height() - 4
            )

        # 5. Texto opcional en el centro
        painter.setPen(Qt.black)
        painter.drawText(rect_cuerpo, Qt.AlignCenter, f"{self.nivel}%")

        painter.end()

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaBateria(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor de Batería")
        self.resize(400, 300)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Widget Batería
        self.bateria = BateriaWidget()
        
        # Controles
        self.lbl_info = QLabel("Usa el slider para probar:")
        self.lbl_info.setAlignment(Qt.AlignCenter)

        # Slider Manual
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.actualizar_manual)

        # Botón Animación
        self.btn_cargar = QPushButton("⚡ Simular Carga")
        self.btn_cargar.clicked.connect(self.iniciar_carga)

        # Timer para la animación
        self.timer = QTimer()
        self.timer.setInterval(50) # Rápido
        self.timer.timeout.connect(self.animacion_carga)

        layout.addWidget(self.bateria)
        layout.addWidget(self.lbl_info)
        layout.addWidget(self.slider)
        layout.addWidget(self.btn_cargar)

    def actualizar_manual(self, valor):
        # Si movemos el slider, paramos la animación automática
        self.timer.stop()
        self.bateria.set_nivel(valor)
        self.btn_cargar.setText("⚡ Simular Carga")

    def iniciar_carga(self):
        self.nivel_temp = 0 # Empezamos de 0
        self.timer.start()
        self.btn_cargar.setText("Cargando...")
        self.btn_cargar.setEnabled(False) # Desactivar botón mientras carga

    def animacion_carga(self):
        self.nivel_temp += 1
        self.bateria.set_nivel(self.nivel_temp)
        self.slider.setValue(self.nivel_temp) # Sincronizar slider

        if self.nivel_temp >= 100:
            self.timer.stop()
            self.btn_cargar.setText("¡Carga Completa!")
            self.btn_cargar.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBateria()
    ventana.show()
    sys.exit(app.exec())