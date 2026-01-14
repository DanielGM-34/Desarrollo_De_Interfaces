from PySide6.QtWidgets import QLineEdit, QWidget, QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout
from PySide6.QtGui import QPalette, QColor, QPainter, QFont, QPen, QRegularExpressionValidator
from PySide6.QtCore import Signal, QRect, Qt, QRegularExpression

# -------------------------------
# CampoNombreAula (QLineEdit derivado)
# -------------------------------
class CampoNombreAula(QLineEdit):
    validity_changed = Signal(bool)  # Señal personalizada

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Introduce el nombre del aula (mínimo 3 caracteres)")
        self._es_valido = False
        self.textChanged.connect(self._validar_y_actualizar_paleta)
        self._validar_y_actualizar_paleta()

    def es_valido(self):
        return self._es_valido

    def _validar(self, texto):
        return len(texto.strip()) >= 3

    def _validar_y_actualizar_paleta(self, *args):
        texto = self.text()
        es_valido_nuevo = self._validar(texto)
        self._es_valido = es_valido_nuevo

        paleta = self.palette()
        if texto == "":
            self.setStyleSheet("background-color: #FFFFFF;")        
        elif es_valido_nuevo:
            self.setStyleSheet("background-color: #DFF5DD;")        
        else:
            self.setStyleSheet("background-color: #F8D7DA;")
        self.setPalette(paleta)
        self.validity_changed.emit(es_valido_nuevo)


# -------------------------------
# IndicadorEstadoAula (QWidget con paintEvent)
# -------------------------------
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import QRect, Qt

class IndicadorEstadoAula(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._estado = "Preparando"

        # Colores configurables por estado
        self._color_correcto = "#48C78E"    # verde
        self._color_preparando = "#FFDD57"  # amarillo
        self._color_incidencia = "#F14668"  # rojo

    def set_estado(self, estado):
        self._estado = estado
        self.update()
    def _color_por_estado(self):
        color = "#CCCCCC"  # valor por defecto

        if self._estado == "Correcto":
            color = self._color_correcto
        elif self._estado == "Preparando":
            color = self._color_preparando
        elif self._estado == "Incidencia":
            color = self._color_incidencia

        return QColor(color)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height()) - 20
        x = (rect.width() - size) // 2
        y = (rect.height() - size) // 2
        circle_rect = QRect(x, y, size, size)

        color = self._color_por_estado()
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(color)
        painter.drawEllipse(circle_rect)

        painter.setPen(Qt.white if self._estado != "Preparando" else Qt.black)
        font = QFont()
        font.setPointSize(max(10, size // 10))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(circle_rect, Qt.AlignCenter, self._estado)



# -------------------------------
# DialogoConfiguracionAvanzada (QDialog modal)
# -------------------------------
from PySide6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QComboBox

class DialogoConfiguracionAvanzada(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración avanzada del aula")
        self.setModal(True)

        # Lista de colores disponibles (nombre → código hex)
        self.colores = {
            "Verde": "#48C78E",
            "Amarillo": "#FFDD57",
            "Rojo": "#F14668",
            "Azul": "#2D89EF",
            "Gris": "#CCCCCC",
            "Naranja": "#FFA500",
            "Morado": "#800080",
            "Rosa": "#FFC0CB",
            "Negro": "#000000",
            "Blanco": "#FFFFFF"
        }

        # Combos para cada estado
        self.cmb_correcto = QComboBox(self)
        self.cmb_correcto.addItems(self.colores.keys())

        self.cmb_preparando = QComboBox(self)
        self.cmb_preparando.addItems(self.colores.keys())

        self.cmb_incidencia = QComboBox(self)
        self.cmb_incidencia.addItems(self.colores.keys())

        # Layout del formulario
        form = QFormLayout()
        form.addRow("Color Correcto:", self.cmb_correcto)
        form.addRow("Color Preparando:", self.cmb_preparando)
        form.addRow("Color Incidencia:", self.cmb_incidencia)

        # Botones estándar
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(botones)
        self.setLayout(layout)

    def establecer_colores(self, correcto, preparando, incidencia):
        self.cmb_correcto.setCurrentText(self._nombre_por_hex(correcto))
        self.cmb_preparando.setCurrentText(self._nombre_por_hex(preparando))
        self.cmb_incidencia.setCurrentText(self._nombre_por_hex(incidencia))
        return  # solo un return, nada más

    def obtener_colores(self):
        return (
            self.colores[self.cmb_correcto.currentText()],
            self.colores[self.cmb_preparando.currentText()],
            self.colores[self.cmb_incidencia.currentText()]
        )

    def _nombre_por_hex(self, hex_color):
        nombre_encontrado = "Gris"  # valor por defecto

        # recorrer con items() pero sin return dentro
        for nombre, valor in self.colores.items():
            if valor.lower() == hex_color.lower():
                nombre_encontrado = nombre

        return nombre_encontrado
