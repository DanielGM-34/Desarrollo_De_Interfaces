import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QRadioButton, QGroupBox, QCheckBox, 
    QGridLayout, QButtonGroup, QMessageBox
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPolygon
from PySide6.QtCore import Qt, QPoint, QRect

# ==============================================================================
# PARTE 1: WIDGET PINTADO (LA TAZA)
# ==============================================================================
class TazaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 300)
        
        # Estado interno
        self.color_cafe = QColor("#3e2723") # Por defecto negro (Espresso)
        self.nivel_llenado = 0.3            # Por defecto pequeño (0.3, 0.6, 0.9)
        self.tiene_hielo = False

    def configurar(self, tipo_cafe, tamano, hielo):
        """Recibe strings y configura el dibujo"""
        
        # 1. Color según tipo
        if tipo_cafe == "Espresso":
            self.color_cafe = QColor("#1b0000") # Casi negro
        elif tipo_cafe == "Americano":
            self.color_cafe = QColor("#3e2723") # Marrón oscuro
        elif tipo_cafe == "Latte":
            self.color_cafe = QColor("#d7ccc8") # Beige muy claro
        elif tipo_cafe == "Capuchino":
            self.color_cafe = QColor("#8d6e63") # Marrón medio

        # 2. Nivel según tamaño
        if tamano == "S": self.nivel_llenado = 0.4
        elif tamano == "M": self.nivel_llenado = 0.65
        elif tamano == "L": self.nivel_llenado = 0.9

        self.tiene_hielo = hielo
        self.update() # ¡PINTAR!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        
        # Coordenadas base para la taza (centrada abajo)
        base_y = h - 50
        ancho_base = 100
        ancho_boca = 160
        altura_taza = 180
        centro_x = w // 2

        # 1. Definir la forma de la taza (Trapezoide invertido)
        # 4 Puntos: Esquina inf izq, inf der, sup der, sup izq
        p1 = QPoint(centro_x - ancho_base // 2, base_y)
        p2 = QPoint(centro_x + ancho_base // 2, base_y)
        p3 = QPoint(centro_x + ancho_boca // 2, base_y - altura_taza)
        p4 = QPoint(centro_x - ancho_boca // 2, base_y - altura_taza)
        
        poligono_taza = QPolygon([p1, p2, p3, p4])

        # 2. Dibujar el líquido (Truco: Recortar)
        # Calculamos la altura del líquido
        altura_liq = int(altura_taza * self.nivel_llenado)
        y_liq = base_y - altura_liq
        
        # Pintamos primero el líquido "flotando" (un rectangulo simple detrás)
        # Para hacerlo bien con la forma inclinada es complejo, 
        # así que pintaremos la taza rellena del color del café hasta cierto punto.
        
        # Vamos a simplificar: Pintamos la taza blanca entera
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawPolygon(poligono_taza)
        
        # Ahora pintamos el café DENTRO (usando clip sería lo ideal, pero haremos un trapecio más pequeño)
        # Calculamos el ancho de la superficie del líquido por geometría (interpolación)
        ratio = self.nivel_llenado
        ancho_liq_boca = ancho_base + (ancho_boca - ancho_base) * ratio
        
        # Puntos del líquido
        l1 = QPoint(centro_x - ancho_base // 2 + 5, base_y - 5) # +5 margen interno
        l2 = QPoint(centro_x + ancho_base // 2 - 5, base_y - 5)
        l3 = QPoint(int(centro_x + ancho_liq_boca // 2) - 5, y_liq)
        l4 = QPoint(int(centro_x - ancho_liq_boca // 2) + 5, y_liq)
        
        poligono_cafe = QPolygon([l1, l2, l3, l4])
        painter.setBrush(QBrush(self.color_cafe))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(poligono_cafe)

        # 3. Dibujar Hielos (Cuadraditos azules) si hace falta
        if self.tiene_hielo:
            painter.setBrush(QBrush(QColor("#e3f2fd"))) # Azul hielo
            painter.setPen(QPen(QColor("#90caf9"), 1))
            # Dibujamos 3 cubitos flotando
            tam_hielo = 20
            painter.drawRect(centro_x - 10, y_liq + 10, tam_hielo, tam_hielo)
            painter.drawRect(centro_x - 30, y_liq + 25, tam_hielo, tam_hielo)
            painter.drawRect(centro_x + 15, y_liq + 15, tam_hielo, tam_hielo)

        # 4. Asa de la taza (Arco a la derecha)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.black, 3))
        # drawArc(rect, start, span)
        painter.drawArc(centro_x + ancho_boca//2 - 20, base_y - altura_taza + 30, 60, 80, 270*16, 180*16)

        painter.end()

# ==============================================================================
# PARTE 2: VENTANA PRINCIPAL
# ==============================================================================
class CoffeeMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barista Pro v1.0")
        self.resize(700, 500)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # LAYOUT PRINCIPAL (Horizontal: Controles IZQ | Dibujo DER)
        layout_main = QHBoxLayout(widget_central)

        # ---------------- COLUMNA IZQUIERDA (CONTROLES) ----------------
        layout_izq = QVBoxLayout()

        # 1. GRUPO TIPO DE CAFÉ (Vertical)
        grupo_tipo = QGroupBox("1. Selecciona Café")
        vbox_tipo = QVBoxLayout()
        
        self.r_espresso = QRadioButton("Espresso")
        self.r_americano = QRadioButton("Americano")
        self.r_latte = QRadioButton("Latte")
        self.r_capu = QRadioButton("Capuchino")
        self.r_espresso.setChecked(True)

        # Conectar todos a la función de actualizar
        self.r_espresso.toggled.connect(self.actualizar_taza)
        self.r_americano.toggled.connect(self.actualizar_taza)
        self.r_latte.toggled.connect(self.actualizar_taza)
        self.r_capu.toggled.connect(self.actualizar_taza)

        vbox_tipo.addWidget(self.r_espresso)
        vbox_tipo.addWidget(self.r_americano)
        vbox_tipo.addWidget(self.r_latte)
        vbox_tipo.addWidget(self.r_capu)
        grupo_tipo.setLayout(vbox_tipo)
        
        layout_izq.addWidget(grupo_tipo)

        # 2. GRUPO TAMAÑO (Horizontal)
        grupo_tam = QGroupBox("2. Tamaño")
        hbox_tam = QHBoxLayout()
        
        self.r_s = QRadioButton("S")
        self.r_m = QRadioButton("M")
        self.r_l = QRadioButton("L")
        self.r_s.setChecked(True)

        self.r_s.toggled.connect(self.actualizar_taza)
        self.r_m.toggled.connect(self.actualizar_taza)
        self.r_l.toggled.connect(self.actualizar_taza)

        hbox_tam.addWidget(self.r_s)
        hbox_tam.addWidget(self.r_m)
        hbox_tam.addWidget(self.r_l)
        grupo_tam.setLayout(hbox_tam)

        layout_izq.addWidget(grupo_tam)

        # 3. GRUPO EXTRAS (Grid Layout / Cuadrícula)
        grupo_extra = QGroupBox("3. Extras")
        grid_extra = QGridLayout()

        self.chk_azucar = QCheckBox("Azúcar")
        self.chk_sacarina = QCheckBox("Sacarina")
        self.chk_hielo = QCheckBox("Con Hielo ❄️")
        self.chk_choco = QCheckBox("Cacao")
        
        # Conectamos el hielo para pintar los cubitos
        self.chk_hielo.stateChanged.connect(self.actualizar_taza)
        # Los otros solo afectan al precio (si quisieramos calcularlo)
        self.chk_azucar.stateChanged.connect(self.calcular_precio)
        self.chk_choco.stateChanged.connect(self.calcular_precio)

        grid_extra.addWidget(self.chk_azucar, 0, 0)
        grid_extra.addWidget(self.chk_sacarina, 0, 1)
        grid_extra.addWidget(self.chk_hielo, 1, 0)
        grid_extra.addWidget(self.chk_choco, 1, 1)
        grupo_extra.setLayout(grid_extra)

        layout_izq.addWidget(grupo_extra)
        
        # Precio
        self.lbl_precio = QLabel("1.20 €")
        self.lbl_precio.setObjectName("lblPrecio")
        self.lbl_precio.setAlignment(Qt.AlignCenter)
        layout_izq.addSpacing(10)
        layout_izq.addWidget(self.lbl_precio)

        layout_main.addLayout(layout_izq, 1) # 40% ancho

        # ---------------- COLUMNA DERECHA (VISUAL Y ACCIÓN) ----------------
        layout_der = QVBoxLayout()

        # Widget Pintado
        self.taza = TazaWidget()
        layout_der.addWidget(self.taza, 1) # Ocupa todo el espacio posible

        # Botón Gigante
        self.btn_servir = QPushButton("☕ SERVIR CAFÉ")
        self.btn_servir.setObjectName("btnServir")
        self.btn_servir.clicked.connect(self.servir)
        layout_der.addWidget(self.btn_servir)

        layout_main.addLayout(layout_der, 2) # 60% ancho

        # Inicializar
        self.actualizar_taza()

    # --- LÓGICA ---

    def actualizar_taza(self):
        # 1. Detectar tipo
        tipo = "Espresso"
        if self.r_americano.isChecked(): tipo = "Americano"
        elif self.r_latte.isChecked(): tipo = "Latte"
        elif self.r_capu.isChecked(): tipo = "Capuchino"

        # 2. Detectar tamaño
        tam = "S"
        if self.r_m.isChecked(): tam = "M"
        elif self.r_l.isChecked(): tam = "L"

        # 3. Detectar hielo
        hielo = self.chk_hielo.isChecked()

        # Mandar datos al widget para que pinte
        self.taza.configurar(tipo, tam, hielo)
        self.calcular_precio()

    def calcular_precio(self):
        base = 1.20
        if self.r_m.isChecked(): base += 0.50
        if self.r_l.isChecked(): base += 1.00
        
        if self.r_latte.isChecked() or self.r_capu.isChecked(): base += 0.30
        
        if self.chk_choco.isChecked(): base += 0.20
        
        self.lbl_precio.setText(f"{base:.2f} €")

    def servir(self):
        QMessageBox.information(self, "Listo", "¡Tu café está listo! ☕\nCuidado que quema.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_cafe.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except:
        print("⚠️ Crea el archivo estilos_cafe.qss")

    ventana = CoffeeMaker()
    ventana.show()
    sys.exit(app.exec())