import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QTabWidget,
    QSlider, QMessageBox, QColorDialog, QToolBar, QFormLayout
)
from PySide6.QtGui import QAction, QPainter, QColor, QPen, QFont, QBrush, QIcon
from PySide6.QtCore import Qt, Signal, QRect

# ==============================================================================
# TEMA 3: WIDGET DERIVADO (Validación + QSS Dinámico)
# ==============================================================================
class InputCodigo(QLineEdit):
    # Señal personalizada: avisa si el código es válido
    validacion_cambiada = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Clave (Empieza por 'CMD-')")
        self.setObjectName("InputComando") # ID para el CSS
        self.textChanged.connect(self._validar_interno)

    def _validar_interno(self, texto):
        # Debe empezar por CMD- y tener algo más
        es_valido = texto.startswith("CMD-") and len(texto) > 4
        
        # PROPIEDAD DINÁMICA: Cambia el estilo en el QSS
        self.setProperty("valido", "true" if es_valido else "false")
        
        # Refrescar estilo (OBLIGATORIO al cambiar propiedad dinámica)
        self.style().unpolish(self)
        self.style().polish(self)
        
        # Emitir señal
        self.validacion_cambiada.emit(es_valido)

# ==============================================================================
# TEMA 3: WIDGET PINTADO A MANO (QPainter)
# ==============================================================================
class MedidorCircular(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self._valor = 0 
        self._color_barra = QColor("#27ae60") # Verde por defecto

    def set_valor(self, valor):
        self._valor = valor
        self.update() # Llama a paintEvent

    def set_color(self, color):
        self._color_barra = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones
        rect = self.rect().adjusted(20, 20, -20, -20)

        # 1. Fondo
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#222")))
        painter.drawEllipse(rect)

        # 2. Arco de carga (Matemáticas básicas de dibujo)
        angulo_inicio = -90 * 16
        angulo_extension = int(-(self._valor * 3.6) * 16)

        pen = QPen(self._color_barra)
        pen.setWidth(15)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, angulo_inicio, angulo_extension)

        # 3. Texto
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self._valor}%")
        painter.end()

# ==============================================================================
# TEMA 2: VENTANA PRINCIPAL (Estructura y Layouts)
# ==============================================================================
class VentanaStarPy(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StarPy Control - EXAMEN FINAL")
        self.resize(600, 500)

        # --- BARRA DE HERRAMIENTAS SUPERIOR ---
        toolbar = QToolBar("Herramientas")
        # Esto impide que el usuario mueva la barra (opcional)
        toolbar.setMovable(False) 
        self.addToolBar(toolbar)
        
        # Acción 1: Cambiar Color
        accion_color = QAction("🎨 Color Reactor", self)
        accion_color.triggered.connect(self.cambiar_color)
        toolbar.addAction(accion_color)

        # Acción 2: Salir
        accion_salir = QAction("🚪 Salir", self)
        accion_salir.triggered.connect(self.close)
        toolbar.addAction(accion_salir)

        # --- PESTAÑAS ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.pestana_control = QWidget()
        self.pestana_reactor = QWidget()

        self.tabs.addTab(self.pestana_control, "Mando Manual")
        self.tabs.addTab(self.pestana_reactor, "Reactor")

        self.setup_tab_control()
        self.setup_tab_reactor()

    def setup_tab_control(self):
        layout = QVBoxLayout()

        # Input Personalizado
        self.input_codigo = InputCodigo()
        self.input_codigo.validacion_cambiada.connect(self.validar_boton_ejecutar)

        # Checkboxes
        self.check_1 = QCheckBox("Activar Propulsores")
        self.check_2 = QCheckBox("Desactivar Gravedad")

        # --- BOTONES DE ACCIÓN (Enviar y Borrar) ---
        layout_botones = QHBoxLayout()

        # Botón BORRAR (Rojo)
        self.btn_borrar = QPushButton("BORRAR DATOS")
        # IMPORTANTE: ID para que el CSS sepa que este es el ROJO
        self.btn_borrar.setObjectName("btnBorrar") 
        self.btn_borrar.clicked.connect(self.accion_borrar)

        # Botón EJECUTAR (Verde)
        self.btn_ejecutar = QPushButton("EJECUTAR ORDEN")
        # IMPORTANTE: ID para que el CSS sepa que este es el VERDE
        self.btn_ejecutar.setObjectName("btnEjecutar")
        self.btn_ejecutar.setEnabled(False) # Empieza desactivado
        self.btn_ejecutar.clicked.connect(self.accion_ejecutar)

        layout_botones.addWidget(self.btn_borrar)
        layout_botones.addWidget(self.btn_ejecutar)

        # Añadir al layout principal
        layout.addWidget(QLabel("SISTEMA DE CONTROL DE NAVE"))
        layout.addSpacing(10)
        
        # Form Layout para que quede alineado
        form = QFormLayout()
        form.addRow("Código Seguridad:", self.input_codigo)
        layout.addLayout(form)
        
        layout.addWidget(self.check_1)
        layout.addWidget(self.check_2)
        layout.addStretch() # Empuja todo hacia arriba
        layout.addLayout(layout_botones) # Botones abajo del todo

        self.pestana_control.setLayout(layout)

    def setup_tab_reactor(self):
        layout = QVBoxLayout()
        self.medidor = MedidorCircular()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.medidor.set_valor)

        layout.addWidget(QLabel("Nivel de Energía del Núcleo:"))
        layout.addWidget(self.medidor, alignment=Qt.AlignCenter)
        layout.addWidget(self.slider)
        self.pestana_reactor.setLayout(layout)

    # --- LÓGICA (SLOTS) ---

    def validar_boton_ejecutar(self, es_valido):
        """Activa el botón verde solo si el código es correcto"""
        self.btn_ejecutar.setEnabled(es_valido)
        if es_valido:
            self.btn_ejecutar.setText("¡EJECUTAR AHORA!")
        else:
            self.btn_ejecutar.setText("Código Inválido...")

    def accion_borrar(self):
        """Limpia el formulario"""
        self.input_codigo.clear()
        self.check_1.setChecked(False)
        self.check_2.setChecked(False)
        print("Formulario reseteado.")

    def accion_ejecutar(self):
        """Muestra un mensaje de éxito"""
        QMessageBox.information(self, "Éxito", "Comando enviado a la nave.")

    def cambiar_color(self):
        """Abre diálogo para cambiar el color del reactor"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.medidor.set_color(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga del QSS con codificación correcta
    try:
        with open("estilos_starpy.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo estilos_starpy.qss primero")

    ventana = VentanaStarPy()
    ventana.show()
    sys.exit(app.exec())