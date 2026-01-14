import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QTimer, QRect

# ==============================================================================
# 1. WIDGET SEMÁFORO (PINTADO)
# ==============================================================================
class SemaforoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 300) # Formato vertical
        
        # ESTADO: False = ROJO (Parar), True = VERDE (Andar)
        self.esta_verde = False 

    def alternar(self):
        """Cambia el estado al contrario del que tiene"""
        self.esta_verde = not self.esta_verde
        self.update() # ¡Obligatorio para que se vea el cambio!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # 1. DIBUJAR LA CAJA (Fondo negro)
        rect_caja = self.rect().adjusted(10, 10, -10, -10)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(QColor("#2c3e50"))) # Gris oscuro chulo
        painter.drawRoundedRect(rect_caja, 20, 20) # Bordes redondeados

        # 2. DEFINIR COLORES SEGÚN ESTADO
        # Colores apagados (base)
        color_rojo = QColor("#550000") # Rojo oscuro (apagado)
        color_verde = QColor("#003300") # Verde oscuro (apagado)

        # Colores encendidos (según el estado)
        if self.esta_verde:
            # Si está verde, encendemos el de abajo
            color_verde = QColor("#2ecc71") # Verde neón
        else:
            # Si no está verde (es rojo), encendemos el de arriba
            color_rojo = QColor("#e74c3c") # Rojo neón

        # 3. DIBUJAR LAS LUCES (Círculos)
        # Calculamos centro horizontal y posiciones verticales
        cx = w // 2
        cy_arriba = h // 4       # Luz Roja
        cy_abajo = h * 3 // 4    # Luz Verde
        radio = 40

        painter.setPen(Qt.NoPen) # Sin borde en las luces

        # Luz Roja (Arriba)
        painter.setBrush(QBrush(color_rojo))
        painter.drawEllipse(QPoint(cx, cy_arriba), radio, radio)

        # Luz Verde (Abajo)
        painter.setBrush(QBrush(color_verde))
        painter.drawEllipse(QPoint(cx, cy_abajo), radio, radio)

        painter.end()

# Necesario para usar QPoint
from PySide6.QtCore import QPoint

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaPeaton(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cruce de Peatones")
        self.resize(300, 500)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout = QVBoxLayout(widget_central)

        # --- INSTANCIAR NUESTRO WIDGET ---
        self.semaforo = SemaforoWidget()
        
        # Etiqueta de texto
        self.lbl_info = QLabel("Estado: ESPERE (Rojo)")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 18px; font-weight: bold; color: red;")

        # --- BOTONERA ---
        btn_manual = QPushButton("Pulsar Botón (Manual)")
        btn_manual.clicked.connect(self.accion_manual)

        self.btn_auto = QPushButton("Modo Automático")
        self.btn_auto.setCheckable(True)
        self.btn_auto.clicked.connect(self.accion_auto)

        # --- TIMER ---
        self.timer = QTimer()
        self.timer.setInterval(1000) # 1 segundo
        self.timer.timeout.connect(self.evento_timer)

        # Añadir al layout
        layout.addWidget(self.semaforo)
        layout.addWidget(self.lbl_info)
        layout.addSpacing(20)
        layout.addWidget(btn_manual)
        layout.addWidget(self.btn_auto)

    # --- LÓGICA ---

    def accion_manual(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_auto.setChecked(False)
        
        # Llamamos al método del widget para cambiar la luz
        self.semaforo.alternar()
        self.actualizar_etiqueta()

    def accion_auto(self):
        if self.btn_auto.isChecked():
            self.timer.start()
        else:
            self.timer.stop()

    def evento_timer(self):
        self.semaforo.alternar()
        self.actualizar_etiqueta()

    def actualizar_etiqueta(self):
        # Preguntamos al widget cómo está
        if self.semaforo.esta_verde:
            self.lbl_info.setText("Estado: ADELANTE (Verde)")
            self.lbl_info.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
        else:
            self.lbl_info.setText("Estado: ESPERE (Rojo)")
            self.lbl_info.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPeaton()
    ventana.show()
    sys.exit(app.exec())