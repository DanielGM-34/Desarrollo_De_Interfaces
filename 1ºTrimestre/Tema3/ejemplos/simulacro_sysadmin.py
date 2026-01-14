import sys
import random
# IMPORTACIONES COMPLETAS (incluyendo QGridLayout que falló antes)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QComboBox, QSpinBox, QTabWidget, QToolBar, QMessageBox, 
    QFormLayout, QListWidget, QListWidgetItem, QProgressBar, QSlider, QGridLayout
)
from PySide6.QtGui import QAction, QPainter, QColor, QPen, QBrush, QFont, QIcon
from PySide6.QtCore import Qt, Signal, QRect

# ==============================================================================
# TEMA 3: INPUT DERIVADO (Validación IP con colores)
# ==============================================================================
class IpAddressInput(QLineEdit):
    estado_cambiado = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Ej: 192.168.1.10")
        self.textChanged.connect(self._validar_ip)
        self.setProperty("estado", "neutro")

    def _validar_ip(self, texto):
        es_valida = False
        partes = texto.split('.')
        if len(partes) == 4:
            todas_ok = True
            for p in partes:
                if not p.isdigit() or not (0 <= int(p) <= 255):
                    todas_ok = False
                    break
            if todas_ok:
                es_valida = True

        # Cambio de propiedad dinámica para el CSS
        if es_valida:
            self.setProperty("estado", "ok")
        else:
            self.setProperty("estado", "error")
            
        # Refresco visual
        self.style().unpolish(self)
        self.style().polish(self)
        
        self.estado_cambiado.emit(es_valida)

# ==============================================================================
# TEMA 3: WIDGET PINTADO A MANO (Monitor Gráfico Colorido)
# ==============================================================================
class ColorfulMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 150)
        self.valores = [10, 20, 30, 40, 20, 10, 50, 60]

    def add_data(self, valor):
        self.valores.pop(0)
        self.valores.append(valor)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fondo blanco con borde grueso
        painter.setPen(QPen(QColor("#2d3436"), 3))
        painter.setBrush(QBrush(QColor("white")))
        painter.drawRoundedRect(self.rect().adjusted(2,2,-2,-2), 10, 10)
        
        w = self.width()
        h = self.height()
        bar_width = (w - 20) / len(self.valores)

        # Dibujar Barras
        for i, val in enumerate(self.valores):
            # Altura proporcional
            bar_h = (val / 100) * (h - 20)
            x = int(10 + i * bar_width)
            y = int(h - 10 - bar_h)
            
            # COLOR DINÁMICO: Verde si es bajo, Rojo si es alto
            if val < 40:
                color = QColor("#00b894") # Verde
            elif val < 75:
                color = QColor("#fdcb6e") # Amarillo
            else:
                color = QColor("#d63031") # Rojo
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor("#2d3436"), 2)) # Borde negro estilo cartoon
            
            # Dejamos un margen entre barras
            rect_barra = QRect(x, y, int(bar_width - 4), int(bar_h))
            painter.drawRoundedRect(rect_barra, 4, 4)

        painter.end()

# ==============================================================================
# TEMA 2: VENTANA PRINCIPAL
# ==============================================================================
class SuperAdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperAdmin Dashboard v5.0 - COLORFUL EDITION")
        self.resize(900, 650)
        
        # ID para CSS (Fondo general)
        widget_central = QWidget()
        widget_central.setObjectName("Central")
        self.setCentralWidget(widget_central)
        
        main_layout = QVBoxLayout(widget_central)

        # --- TABS ---
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Crear pestañas
        self.tab_conn = QWidget()
        self.setup_tab_conn()
        self.tabs.addTab(self.tab_conn, "🌍 Conexión")

        self.tab_serv = QWidget()
        self.setup_tab_serv()
        self.tabs.addTab(self.tab_serv, "⚙️ Servicios")

        self.tab_mon = QWidget()
        self.setup_tab_mon()
        self.tabs.addTab(self.tab_mon, "📊 Monitor")

        # Barra estado
        self.statusBar().showMessage("Sistema listo.")

    # ------------------ PESTAÑA 1: CONEXIÓN ------------------
    def setup_tab_conn(self):
        layout = QHBoxLayout()
        
        # Panel Izquierdo: Datos
        grupo_datos = QGroupBox("Datos del Servidor")
        form = QFormLayout()
        
        self.input_ip = IpAddressInput() # Input con colores
        self.input_ip.estado_cambiado.connect(self.validar_ip)
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("root")
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["SSH Seguro", "FTP Clásico", "RDP Windows"])

        form.addRow("Dirección IP:", self.input_ip)
        form.addRow("Usuario:", self.input_user)
        form.addRow("Protocolo:", self.combo_tipo)
        grupo_datos.setLayout(form)

        # Panel Derecho: Acciones
        grupo_acciones = QGroupBox("Control de Sesión")
        vbox = QVBoxLayout()
        
        self.chk_vpn = QCheckBox("Forzar VPN")
        self.chk_log = QCheckBox("Guardar Log")
        self.chk_vpn.setChecked(True)

        self.btn_conectar = QPushButton("CONECTAR")
        self.btn_conectar.setObjectName("btnAzul") # Color Azul
        self.btn_conectar.setEnabled(False) # Espera a la IP
        self.btn_conectar.clicked.connect(self.conectar)

        self.btn_abortar = QPushButton("CANCELAR")
        self.btn_abortar.setObjectName("btnRojo") # Color Rojo
        self.btn_abortar.clicked.connect(self.close)

        vbox.addWidget(self.chk_vpn)
        vbox.addWidget(self.chk_log)
        vbox.addSpacing(20)
        vbox.addWidget(self.btn_conectar)
        vbox.addWidget(self.btn_abortar)
        grupo_acciones.setLayout(vbox)

        layout.addWidget(grupo_datos, 2)
        layout.addWidget(grupo_acciones, 1)
        self.tab_conn.setLayout(layout)

    # ------------------ PESTAÑA 2: SERVICIOS ------------------
    def setup_tab_serv(self):
        layout = QVBoxLayout()
        
        grupo_lista = QGroupBox("Servicios Activos")
        vbox = QVBoxLayout()
        
        self.lista = QListWidget()
        items = ["Apache Server", "MySQL Database", "Docker Daemon", "Firewall UFW", "Redis Cache"]
        for i in items:
            item = QListWidgetItem(i)
            item.setCheckState(Qt.Checked)
            self.lista.addItem(item)
            
        vbox.addWidget(self.lista)
        
        # Botones de control
        hbox_btns = QHBoxLayout()
        btn_start = QPushButton("INICIAR SELECCIONADO")
        btn_start.setObjectName("btnVerde") # Color Verde
        btn_start.clicked.connect(lambda: QMessageBox.information(self, "Info", "Servicio Iniciado"))

        btn_stop = QPushButton("DETENER SERVICIO")
        btn_stop.setObjectName("btnRojo") # Color Rojo
        btn_stop.clicked.connect(lambda: QMessageBox.warning(self, "Aviso", "Servicio Detenido"))

        hbox_btns.addWidget(btn_start)
        hbox_btns.addWidget(btn_stop)
        
        vbox.addLayout(hbox_btns)
        grupo_lista.setLayout(vbox)
        layout.addWidget(grupo_lista)
        self.tab_serv.setLayout(layout)

    # ------------------ PESTAÑA 3: MONITOR ------------------
    def setup_tab_mon(self):
        layout = QVBoxLayout()
        
        grupo_mon = QGroupBox("Tráfico de Red (Tiempo Real)")
        vbox = QVBoxLayout()
        
        self.monitor = ColorfulMonitor() # Widget pintado
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(20)
        self.slider.valueChanged.connect(self.actualizar_grafico)

        self.progress = QProgressBar()
        self.progress.setValue(20)

        vbox.addWidget(self.monitor)
        vbox.addSpacing(15)
        vbox.addWidget(QLabel("Simular Carga de Red:"))
        vbox.addWidget(self.slider)
        vbox.addSpacing(10)
        vbox.addWidget(QLabel("Uso de CPU Global:"))
        vbox.addWidget(self.progress)
        
        grupo_mon.setLayout(vbox)
        layout.addWidget(grupo_mon)
        self.tab_mon.setLayout(layout)

    # ------------------ LÓGICA ------------------

    def validar_ip(self, es_valida):
        """Activa el botón solo si la IP es correcta y cambia estilos"""
        self.btn_conectar.setEnabled(es_valida)
        if es_valida:
            self.btn_conectar.setText("CONECTAR AHORA")
        else:
            self.btn_conectar.setText("IP INVÁLIDA")

    def conectar(self):
        ip = self.input_ip.text()
        QMessageBox.information(self, "Conectado", f"Estableciendo túnel seguro a {ip}...")
        self.tabs.setCurrentIndex(1) # Pasa a la pestaña 2

    def actualizar_grafico(self, valor):
        """Actualiza tanto el gráfico pintado como la barra de progreso"""
        self.monitor.add_data(valor)
        self.progress.setValue(valor)
        
        # Cambiar color de la barra de progreso por código (opcional, el CSS ya hace cosas)
        # Pero aquí actualizamos texto del label si quisiéramos

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_syadmin.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo estilos_colorfull.qss")

    ventana = SuperAdminPanel()
    ventana.show()
    sys.exit(app.exec())