import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QRadioButton, QCheckBox, 
    QTextEdit, QGroupBox, QButtonGroup
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QTimer, QRect

# ==============================================================================
# PARTE 1: WIDGET PINTADO A MANO (Progreso Circular)
# ==============================================================================
class ProgresoCircular(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.porcentaje = 0 # 0 a 100

    def set_progreso(self, valor):
        self.porcentaje = valor
        self.update() # Forzar repintado

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        rect = QRect(10, 10, w-20, h-20) # Margen de 10px

        # 1. Círculo de Fondo (Gris claro, la pista)
        painter.setPen(QPen(QColor("#e0e0e0"), 15)) # Borde muy grueso (15px)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(rect)

        # 2. Arco de Progreso (Color dinámico)
        # Cambiamos color según avance: Rojo -> Naranja -> Verde
        if self.porcentaje < 30:
            color = QColor("#e74c3c") # Rojo
        elif self.porcentaje < 70:
            color = QColor("#f39c12") # Naranja
        else:
            color = QColor("#2ecc71") # Verde

        pen_progreso = QPen(color, 15)
        pen_progreso.setCapStyle(Qt.RoundCap) # Bordes del arco redondeados
        painter.setPen(pen_progreso)

        # Matemáticas: 360 grados * 16 (Qt usa 1/16 de grado)
        # Angulo start: 90 (Arriba) -> 90 * 16
        # Angulo span: negativo (horario) -> porcentaje * 3.6 * 16
        span = int(-self.porcentaje * 3.6 * 16)
        painter.drawArc(rect, 90 * 16, span)

        # 3. Texto en el centro
        painter.setPen(QColor("#2c3e50"))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self.porcentaje}%")

        painter.end()

# ==============================================================================
# PARTE 2: VENTANA PRINCIPAL (Lógica + QSS)
# ==============================================================================
class TurboDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TurboDownloader v1.0")
        self.resize(700, 500)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        
        # --- LAYOUT PRINCIPAL (Horizontal: Izq Configuración | Der Visual) ---
        layout_main = QHBoxLayout(central)

        # ==================== COLUMNA IZQUIERDA ====================
        col_izq = QVBoxLayout()

        # 1. Input URL
        lbl_url = QLabel("URL del Archivo:")
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://ejemplo.com/archivo.zip")
        col_izq.addWidget(lbl_url)
        col_izq.addWidget(self.input_url)

        # 2. Grupo Prioridad (RadioButtons)
        group_prio = QGroupBox("Velocidad de Descarga")
        layout_prio = QVBoxLayout()
        
        self.radio_alta = QRadioButton("Alta (Premium)")
        self.radio_media = QRadioButton("Media (Estándar)")
        self.radio_baja = QRadioButton("Baja (Gratis)")
        self.radio_media.setChecked(True) # Por defecto

        layout_prio.addWidget(self.radio_alta)
        layout_prio.addWidget(self.radio_media)
        layout_prio.addWidget(self.radio_baja)
        group_prio.setLayout(layout_prio)
        col_izq.addWidget(group_prio)

        # 3. Opciones (CheckBoxes)
        self.check_shutdown = QCheckBox("Apagar PC al finalizar")
        self.check_antivirus = QCheckBox("Escanear virus")
        col_izq.addWidget(self.check_shutdown)
        col_izq.addWidget(self.check_antivirus)

        # 4. Log / Bloc de notas
        col_izq.addWidget(QLabel("Registro de Eventos:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True) # Solo lectura para que sea un log
        self.log_text.setText("> Esperando orden...")
        col_izq.addWidget(self.log_text)

        layout_main.addLayout(col_izq, 1) # Proporción 1

        # ==================== COLUMNA DERECHA ====================
        col_der = QVBoxLayout()

        # 1. Widget Pintado
        self.visor_progreso = ProgresoCircular()
        col_der.addWidget(self.visor_progreso, 1, alignment=Qt.AlignCenter)

        # 2. Botonera (Horizontal)
        layout_btns = QHBoxLayout()
        
        self.btn_iniciar = QPushButton("INICIAR")
        self.btn_iniciar.setObjectName("btnIniciar") # ID para QSS Verde
        self.btn_iniciar.clicked.connect(self.iniciar_descarga)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("btnCancelar") # ID para QSS Rojo
        self.btn_cancelar.clicked.connect(self.cancelar_descarga)
        self.btn_cancelar.setEnabled(False)

        layout_btns.addWidget(self.btn_iniciar)
        layout_btns.addWidget(self.btn_cancelar)
        col_der.addLayout(layout_btns)

        # Botón extra para limpiar log
        self.btn_limpiar = QPushButton("Limpiar Log")
        self.btn_limpiar.setObjectName("btnLimpiar") # ID para QSS Azul
        self.btn_limpiar.clicked.connect(self.limpiar_log)
        col_der.addWidget(self.btn_limpiar)

        layout_main.addLayout(col_der, 1) # Proporción 1

        # --- TIMER (Motor de la simulación) ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso)
        self.progreso_actual = 0

    # ==================== LÓGICA ====================

    def log(self, mensaje):
        """Helper para escribir en el bloc de notas"""
        self.log_text.append(f"> {mensaje}")

    def iniciar_descarga(self):
        url = self.input_url.text()
        if not url:
            self.log("ERROR: URL vacía.")
            return

        self.log(f"Conectando a {url}...")
        self.btn_iniciar.setEnabled(False)
        self.btn_cancelar.setEnabled(True)
        self.input_url.setEnabled(False) # Bloquear input
        
        self.progreso_actual = 0
        self.visor_progreso.set_progreso(0)

        # Definir velocidad según RadioButton
        if self.radio_alta.isChecked():
            velocidad = 50 # Muy rápido (ms)
            self.log("Modo: ALTA VELOCIDAD")
        elif self.radio_media.isChecked():
            velocidad = 100
            self.log("Modo: Velocidad Estándar")
        else:
            velocidad = 200 # Lento
            self.log("Modo: Velocidad Baja")

        self.timer.start(velocidad)

    def cancelar_descarga(self):
        self.timer.stop()
        self.log("!!! Descarga CANCELADA por usuario.")
        self.reset_ui()

    def actualizar_progreso(self):
        self.progreso_actual += 1
        self.visor_progreso.set_progreso(self.progreso_actual)

        # Eventos a mitad de descarga (Lógica condicional)
        if self.progreso_actual == 50 and self.check_antivirus.isChecked():
            self.log("Escaneando virus en 50%... OK")
        
        if self.progreso_actual >= 100:
            self.timer.stop()
            self.log("DESCARGA COMPLETADA EXITOSAMENTE.")
            if self.check_shutdown.isChecked():
                self.log("Apagando sistema en 3, 2, 1... (Simulado)")
            self.reset_ui()

    def reset_ui(self):
        self.btn_iniciar.setEnabled(True)
        self.btn_cancelar.setEnabled(False)
        self.input_url.setEnabled(True)

    def limpiar_log(self):
        self.log_text.clear()
        self.log_text.setText("> Sistema listo.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga de estilos
    try:
        with open("estilo_descarga.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print("Crea el fichero 'estilo_descarga.qss'")

    ventana = TurboDownloader()
    ventana.show()
    sys.exit(app.exec())