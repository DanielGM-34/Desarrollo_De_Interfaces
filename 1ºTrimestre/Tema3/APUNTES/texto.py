from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QCheckBox, QRadioButton, QComboBox, QListWidget, QTableWidget,
    QTableWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QDateEdit, QTimeEdit
)
import sys
from PySide6.QtCore import Signal


class CampoTexto(QLineEdit):
    texto_valido = Signal(str)
    texto_invalido = Signal(str)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Escribe solo letras...")
        self.textChanged.connect(self._validar)

    def _validar(self, texto):
        if texto.isalpha():
            self.texto_valido.emit(texto)
        else:
            self.texto_invalido.emit(texto)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = CampoTexto()
    ventana.show()

    # Conectar señales para ver resultados en consola
    ventana.texto_valido.connect(lambda t: print("Texto válido:", t))
    ventana.texto_invalido.connect(lambda t: print("Texto inválido:", t))

    sys.exit(app.exec())
