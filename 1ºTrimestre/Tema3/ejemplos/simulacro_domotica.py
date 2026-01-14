import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QComboBox, QTabWidget, QSlider, QToolBar, 
    QGroupBox, QGridLayout, QPushButton, QMessageBox
)
from PySide6.QtGui import QAction, QPainter, QColor, QPen, QBrush, QFont, QPolygon
from PySide6.QtCore import Qt, QPoint

# ==============================================================================
# TEMA 3: WIDGET PINTADO (VELOCÍMETRO / GAUGE)
# ==============================================================================
class GaugeConsumo(QWidget):
    """
    Dibuja un semicírculo con una aguja que indica el consumo en Watts.
    """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 200)
        self._valor = 0 # 0 a 100%
        self._max_watts = 5000 # 5000W es el 100%

    def set_consumo(self, porcentaje):
        """Recibe un valor de 0 a 100"""
        self._valor = max(0, min(100, porcentaje))
        self.update() # ¡Obligatorio para repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones
        ancho = self.width()
        alto = self.height()
        # El radio será un poco menos de la mitad del ancho
        radio = min(ancho / 2, alto) - 20
        centro_x = ancho // 2
        centro_y = alto - 20 # La base del semicírculo está abajo

        # 1. Dibujar Arco de Fondo (Gris)
        painter.setPen(QPen(QColor("#444"), 15))
        # drawArc usa 16avos de grado. 
        # Empezamos en 0 (derecha) y vamos hasta 180 (izquierda) -> 180 * 16
        rect_arco = QRect(centro_x - radio, centro_y - radio, radio * 2, radio * 2)
        painter.drawArc(rect_arco, 0 * 16, 180 * 16)

        # 2. Dibujar Arco de Valor (Color dinámico)
        if self._valor < 50:
            color = QColor("#2ecc71") # Verde
        elif self._valor < 80:
            color = QColor("#f1c40f") # Amarillo
        else:
            color = QColor("#e74c3c") # Rojo alerta

        painter.setPen(QPen(color, 15))
        # Ángulo: De 180 (izq) restamos valor. 
        # Qt mide ángulos antihorario: 0 es las 3, 90 las 12, 180 las 9.
        span_angle = -int((self._valor / 100) * 180 * 16)
        painter.drawArc(rect_arco, 180 * 16, span_angle)

        # 3. Dibujar la Aguja (Matemáticas básicas)
        # Convertimos valor (0-100) a ángulo en radianes para usar sen/cos
        # 0% = PI radianes (izquierda), 100% = 0 radianes (derecha)
        angulo_rad = math.pi * (1 - self._valor / 100)
        
        punto_punta_x = centro_x + int(math.cos(angulo_rad) * (radio - 20))
        punto_punta_y = centro_y - int(math.sin(angulo_rad) * (radio - 20))
        
        painter.setPen(QPen(QColor("white"), 3))
        painter.drawLine(centro_x, centro_y, punto_punta_x, punto_punta_y)

        # 4. Texto Central
        painter.setPen(color)
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        watts = int(self._max_watts * (self._valor / 100))
        painter.drawText(self.rect(), Qt.AlignCenter | Qt.AlignBottom, f"{watts} W")

        painter.end()

# ==============================================================================
# VENTANA PRINCIPAL
# ==============================================================================
class SmartHomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EcoHome Manager v4.0")
        self.resize(700, 500)

        # --- TOOLBAR ---
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Acción Apagar Todo
        self.accion_apagar = QAction("⚠️ APAGADO EMERGENCIA", self)
        self.accion_apagar.triggered.connect(self.apagar_todo)
        
        # Botón estilizado en la toolbar
        btn_fake = QPushButton("⚠️ APAGAR TODO")
        btn_fake.setObjectName("btnApagar") # ID Rojo
        btn_fake.clicked.connect(self.apagar_todo)
        toolbar.addWidget(btn_fake)

        # --- PESTAÑAS ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_control = QWidget()
        self.tab_energy = QWidget()

        self.tabs.addTab(self.tab_control, "🏠 Control Estancias")
        self.tabs.addTab(self.tab_energy, "⚡ Monitor Energía")

        self.setup_control_tab()
        self.setup_energy_tab()

    def setup_control_tab(self):
        layout = QVBoxLayout()

        # Selector de Habitación
        layout.addWidget(QLabel("Selecciona Estancia:"))
        self.combo_room = QComboBox()
        self.combo_room.addItems(["Salón Principal", "Dormitorio Master", "Cocina", "Garaje"])
        self.combo_room.currentTextChanged.connect(self.cambiar_estancia)
        layout.addWidget(self.combo_room)

        # Grupo de Dispositivos (Grid Layout)
        grupo = QGroupBox("Dispositivos Conectados")
        grid = QGridLayout()

        # Switches (Checkboxes estilizados)
        self.sw_luz_techo = QCheckBox("Luz de Techo")
        self.sw_luz_mesa = QCheckBox("Lámpara Mesa")
        self.sw_tv = QCheckBox("Smart TV")
        self.sw_ac = QCheckBox("Aire Acondicionado")

        # Conectar señales para recalcular consumo
        self.sw_luz_techo.toggled.connect(self.calcular_consumo)
        self.sw_luz_mesa.toggled.connect(self.calcular_consumo)
        self.sw_tv.toggled.connect(self.calcular_consumo)
        self.sw_ac.toggled.connect(self.calcular_consumo)

        grid.addWidget(self.sw_luz_techo, 0, 0)
        grid.addWidget(self.sw_luz_mesa, 0, 1)
        grid.addWidget(self.sw_tv, 1, 0)
        grid.addWidget(self.sw_ac, 1, 1)
        grupo.setLayout(grid)
        layout.addWidget(grupo)

        # Regulador de Intensidad (La Bombilla)
        grupo_dimmer = QGroupBox("Ambiente (Dimmer)")
        vbox_dim = QVBoxLayout()
        
        # La bombilla es un Label redondo
        self.lbl_bombilla = QLabel("💡")
        self.lbl_bombilla.setObjectName("lblBombilla")
        self.lbl_bombilla.setFixedSize(100, 100)
        self.lbl_bombilla.setAlignment(Qt.AlignCenter)
        self.lbl_bombilla.setStyleSheet("font-size: 40px; color: #333; background-color: #222;") # Apagada

        self.slider_luz = QSlider(Qt.Horizontal)
        self.slider_luz.setRange(0, 100)
        self.slider_luz.valueChanged.connect(self.actualizar_bombilla)

        vbox_dim.addWidget(self.lbl_bombilla, alignment=Qt.AlignCenter)
        vbox_dim.addWidget(self.slider_luz)
        grupo_dimmer.setLayout(vbox_dim)
        
        layout.addWidget(grupo_dimmer)
        self.tab_control.setLayout(layout)

    def setup_energy_tab(self):
        layout = QVBoxLayout()
        
        self.gauge = GaugeConsumo() # Nuestro widget pintado
        
        # Slider de simulación extra
        self.slider_simulacion = QSlider(Qt.Horizontal)
        self.slider_simulacion.setRange(0, 100)
        self.slider_simulacion.setValue(0)
        self.slider_simulacion.valueChanged.connect(self.simulacion_manual)

        layout.addWidget(QLabel("Consumo en Tiempo Real:"))
        layout.addWidget(self.gauge, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Simular Carga Externa (Coche Eléctrico, Horno...):"))
        layout.addWidget(self.slider_simulacion)
        
        self.tab_energy.setLayout(layout)

    # --- LÓGICA ---

    def cambiar_estancia(self, nombre):
        # Simplemente reseteamos controles al cambiar de habitación para el efecto demo
        self.sw_luz_techo.setChecked(False)
        self.sw_tv.setChecked(False)
        self.slider_luz.setValue(0)
        self.statusBar().showMessage(f"Controlando: {nombre}")

    def actualizar_bombilla(self, valor):
        # Cambiamos el color de fondo del label según el slider
        # De negro (#000) a Amarillo (#FFD700)
        # Interpolación simple:
        intensidad = int(255 * (valor / 100))
        color_hex = f"rgba(255, 215, 0, {valor/100})" # Amarillo con transparencia alpha
        
        # Actualizamos estilo solo de este widget
        self.lbl_bombilla.setStyleSheet(f"""
            QLabel#lblBombilla {{
                background-color: {color_hex};
                border-radius: 50px;
                border: 4px solid #555;
                font-size: 40px;
                color: { 'black' if valor > 50 else '#555' };
            }}
        """)
        
        # También afecta al consumo
        self.calcular_consumo()

    def calcular_consumo(self):
        # Sumamos valores arbitrarios
        total = 0
        if self.sw_luz_techo.isChecked(): total += 10
        if self.sw_luz_mesa.isChecked(): total += 5
        if self.sw_tv.isChecked(): total += 15
        if self.sw_ac.isChecked(): total += 40
        
        # Añadimos lo de la bombilla regulable (0 a 10)
        total += int(self.slider_luz.value() / 10)
        
        # Añadimos la simulación de la otra pestaña
        total += self.slider_simulacion.value()

        # Actualizamos el gauge
        self.gauge.set_consumo(total)

    def simulacion_manual(self, valor):
        # Al mover el slider de la pestaña 2, recalculamos todo
        self.calcular_consumo()

    def apagar_todo(self):
        self.sw_luz_techo.setChecked(False)
        self.sw_luz_mesa.setChecked(False)
        self.sw_tv.setChecked(False)
        self.sw_ac.setChecked(False)
        self.slider_luz.setValue(0)
        self.slider_simulacion.setValue(0)
        QMessageBox.critical(self, "Sistema", "Apagado de emergencia ejecutado.\nConsumo: 0W")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Carga de estilos UTF-8
    try:
        from PySide6.QtCore import QFile, QTextStream
        file = QFile("estilos_domotica.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            app.setStyleSheet(stream.readAll())
    except Exception as e:
        print(f"Error estilos: {e}")

    ventana = SmartHomeApp()
    ventana.show()
    sys.exit(app.exec())