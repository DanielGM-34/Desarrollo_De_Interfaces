import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QSpinBox, QMessageBox
)
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPolygon
from PySide6.QtCore import Qt, QTimer, QPoint

# ==============================================================================
# TEMA 3: WIDGET PINTADO A MANO (Gráfica de Líneas)
# ==============================================================================
class GraficaLineal(QWidget):
    """
    Dibuja un historial de datos (lista de números 0-100) uniendo puntos.
    SIN QSS: Todo el color de la línea se define aquí con Python.
    """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 200)
        # Lista para guardar los últimos 20 valores de CPU
        # Empezamos con ceros
        self.datos = [0] * 20 
        
    def agregar_valor(self, valor):
        """Añade un dato nuevo y borra el más antiguo (efecto desplazamiento)"""
        self.datos.pop(0) # Eliminar el primero (izquierda)
        self.datos.append(valor) # Añadir al final (derecha)
        self.update() # ¡Repintar!

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Dibujar Fondo (Negro rejilla)
        painter.fillRect(self.rect(), QColor("#050505"))
        
        # 2. Dibujar Rejilla (Grid) - Manualmente con bucles
        ancho = self.width()
        alto = self.height()
        
        # Pincel para la rejilla (Verde muy oscuro y fino)
        pen_grid = QPen(QColor("#003300"))
        pen_grid.setStyle(Qt.DotLine) # Línea punteada
        painter.setPen(pen_grid)

        # Líneas verticales cada 40px
        for x in range(0, ancho, 40):
            painter.drawLine(x, 0, x, alto)
        # Líneas horizontales cada 40px
        for y in range(0, alto, 40):
            painter.drawLine(0, y, ancho, y)

        # 3. Dibujar la Gráfica de Datos
        # Calculamos el paso horizontal (espacio entre puntos)
        paso_x = ancho / (len(self.datos) - 1)
        
        # Preparamos los puntos para dibujar
        puntos_grafica = []
        
        # Color dinámico de la línea (Esto es lo que pedías sin QSS)
        valor_actual = self.datos[-1] # El último valor
        if valor_actual > 80:
            color_linea = QColor("#ff0000") # Rojo (Peligro)
        elif valor_actual > 50:
            color_linea = QColor("#ffff00") # Amarillo (Warning)
        else:
            color_linea = QColor("#00ff41") # Verde (OK)

        # Configuramos el pincel de la gráfica (Gordo)
        pen_grafica = QPen(color_linea)
        pen_grafica.setWidth(3)
        painter.setPen(pen_grafica)

        for i, valor in enumerate(self.datos):
            x = int(i * paso_x)
            # Invertimos Y porque 0 está arriba. 
            # Si valor es 100, queremos y=0. Si valor es 0, queremos y=alto.
            y = int(alto - (valor / 100 * alto))
            puntos_grafica.append(QPoint(x, y))

        # Dibujamos la polilínea (une todos los puntos)
        painter.drawPolyline(puntos_grafica)
        
        # 4. Texto del valor actual en la esquina
        painter.setPen(color_linea) # Usamos el mismo color que la línea
        painter.drawText(10, 20, f"CPU: {valor_actual}%")

        painter.end()

# ==============================================================================
# TEMA 2: VENTANA PRINCIPAL
# ==============================================================================
class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SYS_MONITOR_v9.0")
        self.resize(800, 600)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_main = QVBoxLayout(central)

        # --- PESTAÑAS ---
        self.tabs = QTabWidget()
        layout_main.addWidget(self.tabs)

        # Pestaña 1: Gráfica en tiempo real
        self.tab_dashboard = QWidget()
        self.setup_tab_dashboard()
        self.tabs.addTab(self.tab_dashboard, "DASHBOARD")

        # Pestaña 2: Tabla de Procesos (Historial)
        self.tab_procesos = QWidget()
        self.setup_tab_procesos()
        self.tabs.addTab(self.tab_procesos, "PROCESS_LIST")

        # --- TEMPORIZADOR (Simula la CPU) ---
        self.timer = QTimer()
        self.timer.setInterval(500) # Medio segundo
        self.timer.timeout.connect(self.actualizar_sistema)
        self.timer.start()

    def setup_tab_dashboard(self):
        layout = QVBoxLayout()

        # 1. Nuestra gráfica personalizada
        self.grafica = GraficaLineal()
        
        # 2. Panel de Control
        grupo_control = QGroupBox("CONTROL_PANEL")
        hbox = QHBoxLayout()

        self.btn_pause = QPushButton("PAUSE MONITOR")
        self.btn_pause.setCheckable(True)
        self.btn_pause.clicked.connect(self.toggle_timer)

        self.btn_stress = QPushButton("⚠️ STRESS TEST")
        self.btn_stress.setObjectName("btnStress") # ID para ponerlo rojo en QSS
        self.btn_stress.pressed.connect(self.iniciar_stress) # Al pulsar sube
        self.btn_stress.released.connect(self.parar_stress)  # Al soltar baja

        self.spin_base = QSpinBox()
        self.spin_base.setRange(0, 50)
        self.spin_base.setValue(10)
        self.spin_base.setPrefix("Base Load: ")

        hbox.addWidget(self.btn_pause)
        hbox.addWidget(self.spin_base)
        hbox.addStretch()
        hbox.addWidget(self.btn_stress)
        grupo_control.setLayout(hbox)

        layout.addWidget(QLabel("CPU_USAGE_HISTORY:"))
        layout.addWidget(self.grafica, 1) # El 1 es para que se expanda
        layout.addWidget(grupo_control)
        
        self.tab_dashboard.setLayout(layout)

    def setup_tab_procesos(self):
        layout = QVBoxLayout()
        
        # Tabla estándar de Qt
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["PID", "NOMBRE", "USO %"])
        # Hacemos que la tabla ocupe todo el ancho
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabla)
        
        btn_limpiar = QPushButton("CLEAR LOGS")
        btn_limpiar.clicked.connect(lambda: self.tabla.setRowCount(0))
        layout.addWidget(btn_limpiar)

        self.tab_procesos.setLayout(layout)

    # --- LÓGICA ---

    def toggle_timer(self):
        if self.btn_pause.isChecked():
            self.timer.stop()
            self.btn_pause.setText("RESUME MONITOR")
        else:
            self.timer.start()
            self.btn_pause.setText("PAUSE MONITOR")

    def iniciar_stress(self):
        # Variable bandera para simular carga alta
        self.stress_mode = True

    def parar_stress(self):
        self.stress_mode = False

    def actualizar_sistema(self):
        # 1. Calcular valor simulado
        base = self.spin_base.value()
        
        # Si estamos apretando el botón de estrés, subimos a 90-100
        if hasattr(self, 'stress_mode') and self.stress_mode:
            valor = random.randint(90, 100)
        else:
            # Si no, valor base + ruido aleatorio
            valor = base + random.randint(0, 20)
            valor = min(100, valor)

        # 2. Mandar datos a la gráfica (Widget pintado)
        self.grafica.agregar_valor(valor)

        # 3. Añadir fila a la tabla (Widget estándar)
        # Solo añadimos si el valor es alto para no llenar la tabla
        if valor > 50:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # Datos falsos
            pid = str(random.randint(1000, 9999))
            nombre = random.choice(["chrome.exe", "python.exe", "docker_engine", "kernel_task"])
            
            self.tabla.setItem(row, 0, QTableWidgetItem(pid))
            self.tabla.setItem(row, 1, QTableWidgetItem(nombre))
            item_valor = QTableWidgetItem(f"{valor}%")
            
            # Colorear texto de la tabla si es crítico (Usando métodos de Qt, no CSS)
            if valor > 80:
                item_valor.setForeground(QBrush(Qt.red))
            
            self.tabla.setItem(row, 2, item_valor)
            self.tabla.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_matrix.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo estilos_matrix.qss")

    ventana = SystemMonitor()
    ventana.show()
    sys.exit(app.exec())