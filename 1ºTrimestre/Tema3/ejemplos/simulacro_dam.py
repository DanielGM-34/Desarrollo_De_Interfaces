import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QComboBox, QSpinBox, QTabWidget, QToolBar, QMessageBox, 
    QFormLayout, QTextEdit, QGridLayout
)
from PySide6.QtGui import QAction, QPainter, QColor, QPen, QBrush, QFont
from PySide6.QtCore import Qt, Signal, QRect

# ==============================================================================
# TEMA 3: INPUT VALIDADO (Nombre Proyecto)
# ==============================================================================
class InputNombreProyecto(QLineEdit):
    validacion_cambiada = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Ej: mi-api-rest (Solo minúsculas y guiones)")
        self.textChanged.connect(self._validar)
        self.setProperty("error", "false")

    def _validar(self, texto):
        # Regla: Sin espacios y longitud > 2
        if " " in texto or len(texto) < 3:
            es_valido = False
            self.setProperty("error", "true")
        else:
            es_valido = True
            self.setProperty("error", "false")
        
        self.style().unpolish(self)
        self.style().polish(self)
        self.validacion_cambiada.emit(es_valido)

# ==============================================================================
# TEMA 3: BLOC DE NOTAS CON LÍMITE (Estilo Dinámico)
# ==============================================================================
class LimitTextEdit(QTextEdit):
    """
    Editor de texto que cambia de color si superas el límite de caracteres.
    """
    LIMITE = 100

    def __init__(self):
        super().__init__()
        self.setPlaceholderText(f"Escribe comandos extra (Máx {self.LIMITE} chars)...")
        self.textChanged.connect(self._check_limit)
        self.setProperty("limite", "ok")

    def _check_limit(self):
        texto = self.toPlainText()
        cantidad = len(texto)
        
        if cantidad > self.LIMITE:
            self.setProperty("limite", "excedido")
        else:
            self.setProperty("limite", "ok")
            
        # Refrescar estilo
        self.style().unpolish(self)
        self.style().polish(self)

# ==============================================================================
# TEMA 3: MONITOR GRÁFICO (QPainter)
# ==============================================================================
class MonitorRecursos(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(180, 180)
        self._cpu = 10
        self._ram = 20

    def set_valores(self, cpu, ram):
        self._cpu = cpu
        self._ram = ram
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRect(10, 10, self.width()-20, self.height()-20)
        
        # 1. Fondo
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#e1e4e8")))
        painter.drawEllipse(rect)

        # 2. Arco CPU (Azul)
        start_angle = 90 * 16
        span_cpu = int((-self._cpu / 100.0) * 360 * 16)
        painter.setBrush(QBrush(QColor("#0366d6")))
        painter.drawPie(rect, start_angle, span_cpu)

        # 3. Arco RAM (Morado) - Empieza donde acaba CPU
        start_ram = start_angle + span_cpu
        span_ram = int((-self._ram / 100.0) * 360 * 16)
        painter.setBrush(QBrush(QColor("#6f42c1")))
        painter.drawPie(rect, start_ram, span_ram)

        # 4. Texto Central
        painter.setPen(QColor("#333"))
        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        info = f"CPU: {self._cpu}%\nRAM: {self._ram}%"
        painter.drawText(rect, Qt.AlignCenter, info)
        
        painter.end()

# ==============================================================================
# TEMA 2: VENTANA PRINCIPAL
# ==============================================================================
class DevSuiteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevSuite Pro - Scaffolding Tool")
        self.resize(850, 600)

        # Barra de Menú y Toolbar
        self.setup_bars()

        # Widget Central y Layout Principal
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_main = QHBoxLayout(widget_central)

        # ---------------- COLUMNA IZQUIERDA (TABS) ----------------
        self.tabs = QTabWidget()
        layout_main.addWidget(self.tabs, 2) # Factor expansión 2

        # --- TAB 1: GENERAL ---
        self.tab_general = QWidget()
        self.setup_tab_general()
        self.tabs.addTab(self.tab_general, "General")

        # --- TAB 2: GIT CONFIG ---
        self.tab_git = QWidget()
        self.setup_tab_git()
        self.tabs.addTab(self.tab_git, "Git Control")

        # --- TAB 3: DOCKER ---
        self.tab_docker = QWidget()
        self.setup_tab_docker()
        self.tabs.addTab(self.tab_docker, "Docker Env")

        # ---------------- COLUMNA DERECHA (MONITOR Y ACCIONES) ----------------
        layout_right = QVBoxLayout()
        
        grupo_monitor = QGroupBox("Recursos Estimados")
        layout_mon = QVBoxLayout()
        self.monitor = MonitorRecursos()
        layout_mon.addWidget(self.monitor)
        grupo_monitor.setLayout(layout_mon)
        
        layout_right.addWidget(grupo_monitor)
        
        # Botones
        self.btn_limpiar = QPushButton("Restaurar")
        self.btn_limpiar.setObjectName("btnLimpiar")
        self.btn_limpiar.clicked.connect(self.reset_all)

        self.btn_generar = QPushButton("🚀 GENERAR BUILD")
        self.btn_generar.setObjectName("btnGenerar")
        self.btn_generar.setEnabled(False)
        self.btn_generar.clicked.connect(self.generar_build)

        layout_right.addStretch()
        layout_right.addWidget(self.btn_limpiar)
        layout_right.addWidget(self.btn_generar)

        layout_main.addLayout(layout_right, 1) # Factor expansión 1

    # ------------------ CONFIGURACIÓN DE TABS ------------------

    def setup_tab_general(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.input_nombre = InputNombreProyecto()
        self.input_nombre.validacion_cambiada.connect(self.validar_global)
        
        self.combo_stack = QComboBox()
        self.combo_stack.addItems(["Python / Django", "Java / Spring", "NodeJS / Express"])
        self.combo_stack.currentIndexChanged.connect(self.actualizar_recursos)

        form.addRow("Nombre Proyecto:", self.input_nombre)
        form.addRow("Tech Stack:", self.combo_stack)
        
        grupo_tipo = QGroupBox("Tipo de Aplicación")
        h_layout = QHBoxLayout()
        self.r_monolito = QRadioButton("Monolito")
        self.r_micro = QRadioButton("Microservicios")
        self.r_serverless = QRadioButton("Serverless")
        self.r_monolito.setChecked(True)
        # Conectar para actualizar gráfica
        self.r_monolito.toggled.connect(self.actualizar_recursos)
        self.r_micro.toggled.connect(self.actualizar_recursos)
        
        h_layout.addWidget(self.r_monolito)
        h_layout.addWidget(self.r_micro)
        h_layout.addWidget(self.r_serverless)
        grupo_tipo.setLayout(h_layout)

        layout.addLayout(form)
        layout.addWidget(grupo_tipo)
        layout.addStretch()
        self.tab_general.setLayout(layout)

    def setup_tab_git(self):
        layout = QVBoxLayout()
        
        self.chk_init_git = QCheckBox("Inicializar Repositorio Git")
        self.chk_init_git.setChecked(True)
        self.chk_init_git.stateChanged.connect(self.toggle_git_inputs)

        form = QFormLayout()
        self.input_branch = QLineEdit("main")
        self.input_remote = QLineEdit()
        self.input_remote.setPlaceholderText("https://github.com/usuario/repo.git")
        
        form.addRow("Rama Principal:", self.input_branch)
        form.addRow("Remote URL:", self.input_remote)

        layout.addWidget(self.chk_init_git)
        layout.addLayout(form)
        layout.addStretch()
        self.tab_git.setLayout(layout)

    def setup_tab_docker(self):
        layout = QVBoxLayout()
        
        self.chk_docker = QCheckBox("Habilitar Dockerización")
        self.chk_docker.stateChanged.connect(self.actualizar_recursos) # Sube recursos si se activa

        form = QFormLayout()
        self.combo_base = QComboBox()
        self.combo_base.addItems(["python:3.9-slim", "node:16-alpine", "openjdk:17"])
        
        self.spin_port = QSpinBox()
        self.spin_port.setRange(80, 9999)
        self.spin_port.setValue(8000)

        form.addRow("Imagen Base:", self.combo_base)
        form.addRow("Puerto Expuesto:", self.spin_port)

        # Aquí usamos nuestro componente personalizado con QSS
        lbl_info = QLabel("Comandos Extra (Dockerfile):")
        self.txt_dockerfile = LimitTextEdit()
        
        layout.addWidget(self.chk_docker)
        layout.addLayout(form)
        layout.addWidget(lbl_info)
        layout.addWidget(self.txt_dockerfile)
        self.tab_docker.setLayout(layout)

    def setup_bars(self):
        menu = self.menuBar()
        m_file = menu.addMenu("Archivo")
        a_reset = QAction("Nuevo Proyecto", self)
        a_reset.triggered.connect(self.reset_all)
        m_file.addAction(a_reset)

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Acciones rápidas para cambiar de Tab
        a_tab1 = QAction("General", self)
        a_tab1.triggered.connect(lambda: self.tabs.setCurrentIndex(0))
        
        a_tab2 = QAction("Git Config", self)
        a_tab2.triggered.connect(lambda: self.tabs.setCurrentIndex(1))

        toolbar.addAction(a_tab1)
        toolbar.addAction(a_tab2)

    # ------------------ LÓGICA Y SLOTS ------------------

    def toggle_git_inputs(self):
        estado = self.chk_init_git.isChecked()
        self.input_branch.setEnabled(estado)
        self.input_remote.setEnabled(estado)

    def validar_global(self, nombre_valido):
        # Solo activamos si el nombre es válido
        if nombre_valido:
            self.btn_generar.setEnabled(True)
            self.btn_generar.setText("🚀 GENERAR BUILD")
        else:
            self.btn_generar.setEnabled(False)
            self.btn_generar.setText("Nombre Inválido")

    def actualizar_recursos(self):
        # Lógica falsa para calcular consumo
        cpu = 10
        ram = 10
        
        if self.r_micro.isChecked(): 
            cpu += 40
            ram += 30
        
        if self.chk_docker.isChecked():
            cpu += 20
            ram += 40
            
        if "Java" in self.combo_stack.currentText():
            ram += 20

        # Enviamos datos al widget pintado
        self.monitor.set_valores(min(cpu, 100), min(ram, 100))

    def reset_all(self):
        self.input_nombre.clear()
        self.tabs.setCurrentIndex(0)
        self.chk_docker.setChecked(False)
        self.r_monolito.setChecked(True)
        self.txt_dockerfile.clear()
        print(">> Sistema reseteado")

    def generar_build(self):
        # Recogida de datos de todas las pestañas
        data = {
            "nombre": self.input_nombre.text(),
            "git": self.chk_init_git.isChecked(),
            "docker": self.chk_docker.isChecked(),
            "docker_cmds": self.txt_dockerfile.toPlainText()
        }
        
        print("\n[BUILD STARTED] ------------------")
        print(f"Project: {data['nombre']}")
        print(f"Git Init: {data['git']}")
        print(f"Dockerize: {data['docker']}")
        if data['docker']:
            print(f"Dockerfile append: {len(data['docker_cmds'])} chars")
        print("----------------------------------\n")
        
        QMessageBox.information(self, "Build Complete", "Estructura generada en ./dist")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_dev.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo estilos_pro.qss")

    window = DevSuiteWindow()
    window.show()
    sys.exit(app.exec())