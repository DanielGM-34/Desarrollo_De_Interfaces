import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QTimer, QRect

# ==============================================================================
# 1. WIDGET PERSONALIZADO: TANQUE
# ==============================================================================
class TanqueWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(250, 300)
        self.nivel_actual = 50.0  # Porcentaje 0.0 a 100.0 (Float para suavidad)
        
    def set_nivel(self, nuevo_nivel):
        # Limitamos entre 0 y 100
        self.nivel_actual = max(0.0, min(100.0, nuevo_nivel))
        self.update() # ¡Repintar!

    def get_nivel(self):
        return self.nivel_actual

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones
        w = self.width()
        h = self.height()
        
        # Márgenes para que no se corte el borde
        margen = 20
        rect_tanque = QRect(margen, margen, w - 2*margen, h - 2*margen)

        # --- 1. DIBUJAR EL LÍQUIDO ---
        
        # Calcular altura del líquido en píxeles
        # Regla de tres: 100% -> altura total del tanque
        altura_liquido = (self.nivel_actual / 100) * rect_tanque.height()
        
        # Coordenada Y del líquido (recordad: 0 está arriba)
        # Y_inicio = (Y_abajo_tanque) - altura_liquido
        y_liquido = (rect_tanque.y() + rect_tanque.height()) - altura_liquido
        
        # Elegir color según nivel (Lógica visual)
        if self.nivel_actual < 20:
            color_liq = QColor("#e74c3c") # Rojo (Alerta vacío)
        elif self.nivel_actual > 80:
            color_liq = QColor("#2ecc71") # Verde (Casi lleno)
        else:
            color_liq = QColor("#3498db") # Azul (Normal)

        painter.setPen(Qt.NoPen) # Sin borde para el agua
        painter.setBrush(QBrush(color_liq))
        
        # Dibujamos el rectángulo del agua
        # (x, y, ancho, alto)
        painter.drawRect(
            rect_tanque.x() + 2,      # Un poco metido para no tapar el borde
            int(y_liquido),           # Convertir float a int
            rect_tanque.width() - 4,  # Un poco menos ancho
            int(altura_liquido)
        )

        # --- 2. DIBUJAR EL CONTENEDOR (CRISTAL) ---
        pen_borde = QPen(Qt.black, 3)
        painter.setPen(pen_borde)
        painter.setBrush(Qt.NoBrush) # Hueco por dentro
        painter.drawRect(rect_tanque)

        # --- 3. DIBUJAR LA REGLA DE MEDICIÓN (EL RETO) ---
        # Vamos a dibujar 10 rayitas al lado derecho
        painter.setPen(QPen(Qt.gray, 2))
        
        # x de la regla = borde derecho del tanque
        x_regla = rect_tanque.right()
        
        for i in range(11): # 0 a 10 (0%, 10%, ... 100%)
            # Calculamos la Y de cada rayita
            y_pos = rect_tanque.bottom() - (i * (rect_tanque.height() / 10))
            
            # Rayas largas en 0, 50 y 100, cortas en el resto
            if i % 5 == 0:
                longitud = 15
                # Texto de porcentaje
                painter.drawText(x_regla + 20, int(y_pos) + 5, f"{i*10}%")
            else:
                longitud = 8
            
            # Dibujar la línea
            painter.drawLine(x_regla, int(y_pos), x_regla + longitud, int(y_pos))

        painter.end()

# ==============================================================================
# 2. VENTANA PRINCIPAL (LÓGICA DE SIMULACIÓN)
# ==============================================================================
class VentanaFabrica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Tanque v1.0")
        self.resize(400, 500)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout = QVBoxLayout(widget_central)

        # Widget Tanque
        self.tanque = TanqueWidget()
        
        # Etiqueta digital
        self.lbl_litros = QLabel("Nivel: 500L / 1000L")
        self.lbl_litros.setAlignment(Qt.AlignCenter)
        self.lbl_litros.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Botonera
        layout_btns = QHBoxLayout()
        
        # Usamos botones "Checkable" para simular válvulas abiertas/cerradas
        self.btn_llenar = QPushButton("🚰 Abrir Entrada")
        self.btn_llenar.setCheckable(True)
        self.btn_llenar.clicked.connect(self.control_valvulas)
        
        self.btn_vaciar = QPushButton("🚽 Abrir Salida")
        self.btn_vaciar.setCheckable(True)
        self.btn_vaciar.clicked.connect(self.control_valvulas)

        layout_btns.addWidget(self.btn_llenar)
        layout_btns.addWidget(self.btn_vaciar)

        # Timer para la física (simular el paso del tiempo)
        self.timer = QTimer()
        self.timer.setInterval(50) # 50ms (rápido para que se vea fluido)
        self.timer.timeout.connect(self.simular_fisica)
        self.timer.start() # El timer siempre corre, pero solo hace algo si hay válvulas abiertas

        layout.addWidget(self.tanque)
        layout.addWidget(self.lbl_litros)
        layout.addLayout(layout_btns)

    def control_valvulas(self):
        """Lógica para que no estén las dos abiertas a la vez (opcional)"""
        sender = self.sender()
        if sender == self.btn_llenar and self.btn_llenar.isChecked():
            self.btn_vaciar.setChecked(False) # Cierra la otra
            self.btn_llenar.setStyleSheet("background-color: #a0f0a0;") # Verde visual
            self.btn_vaciar.setStyleSheet("")
            
        elif sender == self.btn_vaciar and self.btn_vaciar.isChecked():
            self.btn_llenar.setChecked(False)
            self.btn_vaciar.setStyleSheet("background-color: #f0a0a0;") # Rojo visual
            self.btn_llenar.setStyleSheet("")
            
        else:
            # Si desmarcamos, quitamos colores
            sender.setStyleSheet("")

    def simular_fisica(self):
        """Se ejecuta cada 50ms"""
        nivel = self.tanque.get_nivel()
        cambio = 0
        
        if self.btn_llenar.isChecked():
            cambio = 0.5 # Sube 0.5% cada 50ms
        elif self.btn_vaciar.isChecked():
            cambio = -0.8 # Vacía más rápido de lo que llena (física real jeje)
            
        if cambio != 0:
            nuevo_nivel = nivel + cambio
            self.tanque.set_nivel(nuevo_nivel)
            
            # Actualizar etiqueta (Suponemos tanque de 1000 Litros)
            litros = int(nuevo_nivel * 10) # 100% * 10 = 1000
            self.lbl_litros.setText(f"Nivel: {litros}L / 1000L")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFabrica()
    ventana.show()
    sys.exit(app.exec())