import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox
from PySide6.QtGui import QPainter, QColor, QPalette
from PySide6.QtCore import Signal, Qt

# --- CampoNombre derivado ---
class CampoNombre(QLineEdit):
    nombre_valido = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._validar)
    def _validar(self, texto):
        pal = QPalette(self.palette())
        if len(texto) >= 3:
            pal.setColor(QPalette.Base, QColor("#d4efdf"))
            self.nombre_valido.emit(texto)
        else:
            pal.setColor(QPalette.Base, QColor("#f5b7b1"))
        self.setPalette(pal)

# --- CampoEmail derivado ---
class CampoEmail(QLineEdit):
    email_valido = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._validar)
    def _validar(self, texto):
        pal = QPalette(self.palette())
        if "@" in texto and "." in texto:
            pal.setColor(QPalette.Base, QColor("#d4efdf"))
            self.email_valido.emit(texto)
        else:
            pal.setColor(QPalette.Base, QColor("#f5b7b1"))
        self.setPalette(pal)

# --- BotonRegistrar derivado ---
class BotonRegistrar(QPushButton):
    registro_completado = Signal(bool)
    def __init__(self, parent=None):
        super().__init__("Registrar", parent)
        self.clicked.connect(self._registrar)
    def _registrar(self):
        # La lógica se implementa en la ventana principal
        pass

# --- IndicadorProgreso nuevo ---
class IndicadorProgreso(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 30)
        self._progreso = 0
    def setProgreso(self, valor: int):
        self._progreso = valor
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor("red")
        if self._progreso == 1: color = QColor("yellow")
        elif self._progreso >= 2: color = QColor("green")
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self._progreso * 70, 30)

# --- Ventana principal ---
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario de Registro Inteligente")

        self.label_titulo = QLabel("Registro de Usuario")
        self.campo_nombre = CampoNombre()
        self.campo_email = CampoEmail() 
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["Alumno", "Profesor", "Invitado"])
        self.check_terminos = QCheckBox("Aceptar términos")
        self.boton_registrar = BotonRegistrar()
        self.indicador = IndicadorProgreso()
        self.label_estado = QLabel("Estado: pendiente")

        layout = QVBoxLayout()
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.campo_nombre)
        layout.addWidget(self.campo_email)
        layout.addWidget(self.combo_rol)
        layout.addWidget(self.check_terminos)
        layout.addWidget(self.boton_registrar)
        layout.addWidget(self.indicador)
        layout.addWidget(self.label_estado)
        self.setLayout(layout)

        # Conexiones
        self.campo_nombre.nombre_valido.connect(lambda _: self._actualizar_progreso())
        self.campo_email.email_valido.connect(lambda _: self._actualizar_progreso())
        self.boton_registrar.clicked.connect(self._registrar)

    def _actualizar_progreso(self):
        progreso = 0
        if len(self.campo_nombre.text()) >= 3: progreso += 1
        if "@" in self.campo_email.text() and "." in self.campo_email.text(): progreso += 1
        if self.check_terminos.isChecked(): progreso += 1
        self.indicador.setProgreso(progreso)

    def _registrar(self):
        valido = len(self.campo_nombre.text()) >= 3 and "@" in self.campo_email.text() and "." in self.campo_email.text() and self.check_terminos.isChecked()
        self.label_estado.setText("Registro completado" if valido else "Error en el registro")
        self.boton_registrar.registro_completado.emit(valido)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("EXAMENES_GPT/dani.qss", "r") as f:
        app.setStyleSheet(f.read())
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
