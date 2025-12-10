import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QCheckBox
)
from PySide6.QtGui import QPainter, QColor, QPalette
from PySide6.QtCore import Signal, Qt


# --- CampoTitulo derivado ---
class CampoTitulo(QLineEdit):
    titulo_valido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Introduce título (mín. 5 caracteres)")
        self.textChanged.connect(self._validar)

    def _validar(self, texto):
        pal = QPalette(self.palette())
        if len(texto) >= 5:
            pal.setColor(QPalette.Base, QColor("#d4efdf"))  # verde suave
            self.titulo_valido.emit(texto)
        else:
            pal.setColor(QPalette.Base, QColor("#f5b7b1"))  # rojo suave
        self.setPalette(pal)


# --- CampoDescripcion derivado ---
class CampoDescripcion(QTextEdit):
    descripcion_valida = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Introduce descripción (máx. 200 caracteres)")
        self.textChanged.connect(self._validar)

    def _validar(self):
        texto = self.toPlainText()
        pal = QPalette(self.palette())
        if len(texto) > 200:
            pal.setColor(QPalette.Base, QColor("#f5b7b1"))  # rojo
            self.descripcion_valida.emit(False)
        elif len(texto) > 150:
            pal.setColor(QPalette.Base, QColor("#fcf3cf"))  # amarillo
            self.descripcion_valida.emit(True)
        else:
            pal.setColor(QPalette.Base, QColor("#ffffff"))  # blanco
            self.descripcion_valida.emit(True)
        self.setPalette(pal)


# --- BotonGuardar derivado ---
class BotonGuardar(QPushButton):
    actividad_guardada = Signal(dict)

    def __init__(self, parent=None):
        super().__init__("Guardar actividad", parent)
        self.clicked.connect(self._guardar)

    def _guardar(self):
        # Este método se sobreescribe en la ventana principal
        # Aquí no dejamos vacío, sino que emitimos un diccionario básico
        datos = {"titulo": "", "descripcion": "", "categoria": ""}
        self.actividad_guardada.emit(datos)


# --- PanelIndicadores nuevo ---
class PanelIndicadores(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 80)
        self._titulo_ok = False
        self._desc_ok = False
        self._terminos_ok = False

    def actualizar_estado(self, titulo_ok, desc_ok, terminos_ok):
        self._titulo_ok = titulo_ok
        self._desc_ok = desc_ok
        self._terminos_ok = terminos_ok
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dibujar tres barras horizontales sin usar enumerate
        # Barra 1: título
        color_titulo = QColor("green") if self._titulo_ok else QColor("red")
        painter.setBrush(color_titulo)
        painter.setPen(Qt.NoPen)
        painter.drawRect(10, 10, 200, 20)

        # Barra 2: descripción
        color_desc = QColor("green") if self._desc_ok else QColor("red")
        painter.setBrush(color_desc)
        painter.drawRect(10, 35, 200, 20)

        # Barra 3: términos
        color_terminos = QColor("green") if self._terminos_ok else QColor("red")
        painter.setBrush(color_terminos)
        painter.drawRect(10, 60, 200, 20)


# --- Ventana principal ---
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Actividades")

        self.label_titulo = QLabel("Formulario de Actividad")
        self.campo_titulo = CampoTitulo()
        self.campo_desc = CampoDescripcion()
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["Trabajo", "Estudio", "Ocio"])
        self.check_terminos = QCheckBox("Aceptar términos")
        self.boton_guardar = BotonGuardar()
        self.panel = PanelIndicadores()
        self.label_estado = QLabel("Estado: pendiente")

        layout = QVBoxLayout()
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.campo_titulo)
        layout.addWidget(self.campo_desc)
        layout.addWidget(self.combo_categoria)
        layout.addWidget(self.check_terminos)
        layout.addWidget(self.boton_guardar)
        layout.addWidget(self.panel)
        layout.addWidget(self.label_estado)
        self.setLayout(layout)

        # Conexiones
        self.campo_titulo.titulo_valido.connect(self._on_titulo_valido)
        self.campo_desc.descripcion_valida.connect(self._on_desc_valida)
        self.check_terminos.stateChanged.connect(self._on_terminos_cambiados)
        self.boton_guardar.clicked.connect(self._guardar)

    # --- Métodos de conexión ---
    def _on_titulo_valido(self, texto):
        self._actualizar_panel()

    def _on_desc_valida(self, valido):
        self._actualizar_panel()

    def _on_terminos_cambiados(self, estado):
        self._actualizar_panel()

    def _actualizar_panel(self):
        titulo_ok = len(self.campo_titulo.text()) >= 5
        desc_ok = len(self.campo_desc.toPlainText()) <= 200
        terminos_ok = self.check_terminos.isChecked()
        self.panel.actualizar_estado(titulo_ok, desc_ok, terminos_ok)

    def _guardar(self):
        titulo_ok = len(self.campo_titulo.text()) >= 5
        desc_ok = len(self.campo_desc.toPlainText()) <= 200
        terminos_ok = self.check_terminos.isChecked()

        if titulo_ok and desc_ok and terminos_ok:
            datos = {
                "titulo": self.campo_titulo.text(),
                "descripcion": self.campo_desc.toPlainText(),
                "categoria": self.combo_categoria.currentText()
            }
            self.label_estado.setText("Actividad guardada correctamente")
            self.boton_guardar.actividad_guardada.emit(datos)
        else:
            self.label_estado.setText("Error: revisa los campos")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("EXAMENES_GPT/p.qss", "r") as f:
        app.setStyleSheet(f.read())
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec() 
