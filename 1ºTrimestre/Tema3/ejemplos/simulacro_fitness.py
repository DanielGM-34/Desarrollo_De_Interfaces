import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QRadioButton, QGroupBox, QSpinBox, 
    QButtonGroup, QMessageBox
)
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRect

# ==============================================================================
# PARTE 1: WIDGET PINTADO (ANILLO DE PROGRESO)
# ==============================================================================
class AnilloProgreso(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 250)
        self.pasos_actuales = 0
        self.meta = 10000 # Meta por defecto
        
    def actualizar_datos(self, pasos, meta):
        self.pasos_actuales = pasos
        self.meta = meta
        self.update() # ¡Repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones y Geometría
        w = self.width()
        h = self.height()
        margen = 20
        rect = QRect(margen, margen, w - 2*margen, h - 2*margen)

        # 1. DIBUJAR FONDO DEL ANILLO (Gris claro)
        pen_fondo = QPen(QColor("#dfe6e9"), 15) # Grosor 15
        pen_fondo.setCapStyle(Qt.RoundCap)      # Bordes redondeados
        painter.setPen(pen_fondo)
        painter.drawEllipse(rect) # Dibuja el círculo completo gris

        # 2. CALCULAR ÁNGULO DE PROGRESO
        # Evitamos dividir por 0
        if self.meta > 0:
            porcentaje = min(1.0, self.pasos_actuales / self.meta)
        else:
            porcentaje = 0
            
        # Qt usa 16avos de grado. Círculo completo = 360 * 16 = 5760
        angulo_span = int(-porcentaje * 360 * 16) # Negativo = sentido horario
        angulo_inicio = 90 * 16 # Empezar arriba (las 12)

        # 3. ELEGIR COLOR (Lógica visual)
        if self.pasos_actuales >= self.meta:
            color_anillo = QColor("#fdcb6e") # Oro (Meta conseguida)
        else:
            color_anillo = QColor("#6c5ce7") # Morado (En progreso)

        # 4. DIBUJAR ARCO DE PROGRESO
        pen_progreso = QPen(color_anillo, 15)
        pen_progreso.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_progreso)
        painter.drawArc(rect, angulo_inicio, angulo_span)

        # 5. TEXTO CENTRAL
        painter.setPen(QColor("#2d3436"))
        painter.setFont(QFont("Arial", 28, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, str(self.pasos_actuales))
        
        # Subtítulo pequeño
        painter.setFont(QFont("Arial", 12))
        rect_sub = QRect(rect.x(), rect.y() + 40, rect.width(), rect.height())
        painter.drawText(rect_sub, Qt.AlignCenter, "PASOS")

        painter.end()

# ==============================================================================
# PARTE 2: VENTANA PRINCIPAL
# ==============================================================================
class FitnessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Entrenador Personal")
        self.resize(600, 400)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_main = QHBoxLayout(widget_central)

        # ---------------- COLUMNA IZQUIERDA (CONTROLES) ----------------
        layout_controles = QVBoxLayout()

        # Grupo 1: Meta
        grupo_meta = QGroupBox("1. Tu Objetivo Diario")
        vbox_meta = QVBoxLayout()
        self.spin_meta = QSpinBox()
        self.spin_meta.setRange(100, 50000)
        self.spin_meta.setSingleStep(500)
        self.spin_meta.setValue(5000)
        self.spin_meta.valueChanged.connect(self.actualizar_ui) # Si cambias meta, repinta
        
        vbox_meta.addWidget(QLabel("Pasos a conseguir:"))
        vbox_meta.addWidget(self.spin_meta)
        grupo_meta.setLayout(vbox_meta)

        # Grupo 2: Actividad
        grupo_act = QGroupBox("2. Registrar Actividad")
        vbox_act = QVBoxLayout()
        
        self.rad_paseo = QRadioButton("Paseo (+100 pasos)")
        self.rad_carrera = QRadioButton("Carrera (+500 pasos)")
        self.rad_bici = QRadioButton("Bicicleta (+200 pasos)")
        self.rad_carrera.setChecked(True)

        vbox_act.addWidget(self.rad_paseo)
        vbox_act.addWidget(self.rad_carrera)
        vbox_act.addWidget(self.rad_bici)
        grupo_act.setLayout(vbox_act)

        # Botones
        self.btn_sumar = QPushButton("¡AÑADIR ACTIVIDAD!")
        self.btn_sumar.setObjectName("btnAndar") # ID para CSS Verde
        self.btn_sumar.clicked.connect(self.sumar_pasos)

        self.btn_reset = QPushButton("Empezar de cero")
        self.btn_reset.setObjectName("btnReset") # ID para CSS Gris
        self.btn_reset.clicked.connect(self.resetear)

        layout_controles.addWidget(grupo_meta)
        layout_controles.addWidget(grupo_act)
        layout_controles.addStretch()
        layout_controles.addWidget(self.btn_sumar)
        layout_controles.addWidget(self.btn_reset)

        # ---------------- COLUMNA DERECHA (VISUAL) ----------------
        layout_visual = QVBoxLayout()
        
        self.anillo = AnilloProgreso() # Instancia de nuestro widget
        
        layout_visual.addWidget(QLabel("Tu Progreso Hoy:"))
        layout_visual.addWidget(self.anillo, 1) # El 1 hace que se expanda

        # Añadir al layout principal
        layout_main.addLayout(layout_controles, 1)
        layout_main.addLayout(layout_visual, 2) # El anillo ocupa más espacio

        # Estado inicial
        self.total_pasos = 0
        self.actualizar_ui()

    # --- LÓGICA ---

    def sumar_pasos(self):
        # Miramos qué radio button está marcado
        if self.rad_paseo.isChecked():
            suma = 100
        elif self.rad_carrera.isChecked():
            suma = 500
        else:
            suma = 200
            
        self.total_pasos += suma
        self.actualizar_ui()
        
        # Bonus: Mensaje si llegas a la meta exacta o la superas por primera vez
        meta = self.spin_meta.value()
        if self.total_pasos >= meta and (self.total_pasos - suma) < meta:
             QMessageBox.information(self, "¡Felicidades!", "¡Has alcanzado tu objetivo diario! 🥇")

    def resetear(self):
        self.total_pasos = 0
        self.actualizar_ui()

    def actualizar_ui(self):
        # Mandamos los datos al widget pintado para que se actualice
        meta_actual = self.spin_meta.value()
        self.anillo.actualizar_datos(self.total_pasos, meta_actual)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_fitness.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except:
        print("⚠️ Crea el archivo estilos_fitness.qss")

    ventana = FitnessApp()
    ventana.show()
    sys.exit(app.exec())