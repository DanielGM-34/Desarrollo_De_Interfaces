import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt

# ==============================================================================
# PARTE 1: EL WIDGET PINTADO A MANO (QPainter)
# Este componente NO se estiliza con QSS, se dibuja con código.
# ==============================================================================
class VumetroWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 150)
        self.volumen = 5 # Nivel inicial (0 a 10)

    def set_volumen(self, valor):
        # Limitamos entre 0 y 10
        self.volumen = max(0, min(10, valor))
        self.update() # ¡Repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        
        # Calculamos el ancho de cada barrita (dejando un hueco de 5px)
        # Queremos 10 barras
        ancho_barra = (w / 10) - 5 

        for i in range(10): # 0 a 9
            # 1. ¿De qué color es esta barra?
            # Las primeras 6 verdes, luego 2 amarillas, ultimas 2 rojas
            if i < 6:
                color = QColor("#00ff00") # Verde
            elif i < 8:
                color = QColor("#ffff00") # Amarillo
            else:
                color = QColor("#ff0000") # Rojo

            # 2. ¿Está encendida o apagada?
            # Si el índice 'i' es menor que el volumen actual, pintamos con color.
            # Si no, pintamos gris oscuro (apagado).
            if i < self.volumen:
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(color.lighter(), 2)) # Borde brillante
            else:
                painter.setBrush(QBrush(QColor("#444"))) # Gris apagado
                painter.setPen(Qt.NoPen)

            # 3. Dibujar el rectángulo
            # x = posición i * espacio que ocupa cada una
            x = int(i * (w / 10)) 
            
            # Altura: Hacemos que crezcan un poco de izq a derecha o fijas
            # Vamos a hacerlas fijas de alto para simplificar, pero con margen
            painter.drawRoundedRect(x, 10, int(ancho_barra), h - 20, 5, 5)

        painter.end()

# ==============================================================================
# PARTE 2: LA VENTANA PRINCIPAL (QSS + Estructura)
# ==============================================================================
class AudioControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Master Audio Control")
        self.resize(500, 300)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 1. Título (Estilizado por QSS genérico de QLabel)
        self.lbl_info = QLabel(f"VOLUMEN: 50%")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_info)

        # 2. NUESTRO WIDGET PINTADO (Aquí entra el QPainter)
        self.vumetro = VumetroWidget()
        layout.addWidget(self.vumetro)

        # 3. CONTROLES (Aquí entra el QSS de botones)
        hbox = QHBoxLayout()
        
        btn_menos = QPushButton("-")
        btn_menos.setObjectName("btnBajar") # ID para que salga ROSA
        btn_menos.setFixedSize(50, 50)      # Tamaño fijo para que sea redondo
        btn_menos.clicked.connect(self.bajar_volumen)

        btn_mas = QPushButton("+")
        btn_mas.setObjectName("btnSubir")   # ID para que salga AZUL
        btn_mas.setFixedSize(50, 50)
        btn_mas.clicked.connect(self.subir_volumen)

        hbox.addStretch()
        hbox.addWidget(btn_menos)
        hbox.addSpacing(20)
        hbox.addWidget(btn_mas)
        hbox.addStretch()

        layout.addLayout(hbox)

    def subir_volumen(self):
        nuevo_vol = self.vumetro.volumen + 1
        self.vumetro.set_volumen(nuevo_vol)
        self.lbl_info.setText(f"VOLUMEN: {nuevo_vol * 10}%")

    def bajar_volumen(self):
        nuevo_vol = self.vumetro.volumen - 1
        self.vumetro.set_volumen(nuevo_vol)
        self.lbl_info.setText(f"VOLUMEN: {nuevo_vol * 10}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga del QSS (Estética de la carcasa)
    try:
        with open("estilo_hibrido.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print("Crea el fichero 'estilo_hibrido.qss' para ver los colores neón.")

    ventana = AudioControl()
    ventana.show()
    sys.exit(app.exec())