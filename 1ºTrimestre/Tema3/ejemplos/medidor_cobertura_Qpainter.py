import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QTimer, QRect

# ==============================================================================
# 1. WIDGET PERSONALIZADO MULTICOLOR
# ==============================================================================
class MonitorSenal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 150)
        self.nivel_actual = 0 
        
        # 🔴 CAMBIO 1: Definimos una lista de colores en lugar de uno solo
        # Indice 0 no se usa (o es gris), 1=Rojo, 2=Naranja, 3=Amarillo, 4=Verde
        self.paleta_colores = [
            QColor("#bdc3c7"), # 0 (Base/Vacío)
            QColor("#e74c3c"), # 1 Rojo
            QColor("#e67e22"), # 2 Naranja
            QColor("#f1c40f"), # 3 Amarillo
            QColor("#2ecc71")  # 4 Verde
        ]
        
        self.color_inactivo = QColor("#ecf0f1") # Gris muy clarito para lo apagado

    def set_nivel(self, nivel):
        if nivel > 4: 
            self.nivel_actual = 0
        else:
            self.nivel_actual = nivel
        self.update() # Forzar repintado

    def get_nivel(self):
        return self.nivel_actual

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Borde negro para que se definan bien las barras
        painter.setPen(QPen(Qt.black, 1))

        ancho_widget = self.width()
        alto_widget = self.height()
        
        ancho_barra = int(ancho_widget / 5)
        espacio = int(ancho_barra / 4)

        for i in range(1, 5): 
            
            # 🔴 CAMBIO 2: Lógica de color dinámica
            # Si la barra 'i' debe estar encendida (es menor o igual al nivel actual)
            if i <= self.nivel_actual:
                # Usamos el color correspondiente a esa posición 'i'
                color_a_usar = self.paleta_colores[i]
                painter.setBrush(QBrush(color_a_usar))
            else:
                # Si no, color apagado
                painter.setBrush(QBrush(self.color_inactivo))

            # Geometría (Igual que antes)
            altura_barra = int((i / 4) * alto_widget * 0.8)
            x = (i - 1) * (ancho_barra + espacio) + 20
            y = alto_widget - altura_barra - 10 

            painter.drawRect(x, y, ancho_barra, altura_barra)

        painter.end()

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaExamen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulacro: Señal Multicolor")
        self.resize(450, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.monitor = MonitorSenal()
        
        self.lbl_info = QLabel("Estado: Sin Señal")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        # --- BOTONERA ---
        layout_botones = QHBoxLayout()
        
        self.btn_manual = QPushButton("📡 Buscar (+1)")
        self.btn_manual.clicked.connect(self.accion_manual)
        
        self.btn_auto = QPushButton("🔄 Auto")
        self.btn_auto.setCheckable(True)
        self.btn_auto.clicked.connect(self.accion_auto)

        # 🔴 CAMBIO 3: Nuevo Botón Reset
        self.btn_reset = QPushButton("🗑️ Reset")
        self.btn_reset.setStyleSheet("background-color: #ffcccc; color: red;") # Un poco de estilo rápido
        self.btn_reset.clicked.connect(self.accion_reset)

        layout_botones.addWidget(self.btn_manual)
        layout_botones.addWidget(self.btn_auto)
        layout_botones.addWidget(self.btn_reset)

        self.timer = QTimer()
        self.timer.setInterval(400) # Un poco más rápido
        self.timer.timeout.connect(self.evento_timer)

        layout.addWidget(self.lbl_info)
        layout.addWidget(self.monitor)
        layout.addLayout(layout_botones)

    # --- SLOTS ---

    def accion_manual(self):
        # Si tocamos manual, paramos el automático por seguridad
        if self.timer.isActive():
            self.btn_auto.setChecked(False)
            self.accion_auto()

        nivel = self.monitor.get_nivel()
        self.monitor.set_nivel(nivel + 1)
        self.actualizar_texto()

    def accion_auto(self):
        if self.btn_auto.isChecked():
            self.timer.start()
            self.btn_auto.setText("⏹ Stop")
            self.btn_manual.setEnabled(False)
            self.btn_reset.setEnabled(False) # Bloqueamos reset en auto
        else:
            self.timer.stop()
            self.btn_auto.setText("🔄 Auto")
            self.btn_manual.setEnabled(True)
            self.btn_reset.setEnabled(True)

    # 🔴 CAMBIO 4: Lógica del Reset
    def accion_reset(self):
        self.monitor.set_nivel(0)
        self.actualizar_texto()
        print("Sistema reseteado a 0")

    def evento_timer(self):
        nivel = self.monitor.get_nivel()
        self.monitor.set_nivel(nivel + 1)
        self.actualizar_texto()

    def actualizar_texto(self):
        mensajes = ["Sin Señal ❌", "Débil 🔴", "Media 🟠", "Buena 🟡", "Excelente 🟢"]
        idx = self.monitor.get_nivel()
        self.lbl_info.setText(f"{mensajes[idx]}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaExamen()
    ventana.show()
    sys.exit(app.exec())