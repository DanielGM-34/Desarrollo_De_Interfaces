import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox,
    QPushButton, QLineEdit, QRadioButton, QComboBox, QLabel
)
from PySide6.QtCore import Qt

class GimnasioForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario Gimnasio")
        self.setMinimumSize(800,600)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta título
        label = QLabel("Formulario de Inscripción")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # QLineEdit (nombre)
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Introduce tu nombre")
        layout.addWidget(self.nombre_input)

        # QLineEdit (DNI)
        self.dni_input = QLineEdit()
        self.dni_input.setPlaceholderText("Introduce tu DNI")
        layout.addWidget(self.dni_input)

        # QLineEdit (Teléfono)
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Introduce tu teléfono")
        layout.addWidget(self.telefono_input)

        # QLineEdit (Dirección)
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Introduce tu dirección")
        layout.addWidget(self.direccion_input)

        # QCheckBox (aceptar términos)
        self.terminos_checkbox = QCheckBox("Acepto los términos y condiciones")
        layout.addWidget(self.terminos_checkbox)

        # QRadioButton (tipo de membresía)
        etiquetaMem = QLabel("selecciona tu tipo de membresía:")

        self.radio_basico = QRadioButton("Membresía Básica")
        self.radio_premium = QRadioButton("Membresía Premium")
        layout.addWidget(etiquetaMem)
        layout.addWidget(self.radio_basico)
        layout.addWidget(self.radio_premium)

        # QComboBox (selección de actividad)
        self.actividad_combo = QComboBox()
        etiquetaAct = QLabel("selecciona una actividad:")
        self.actividad_combo.setPlaceholderText("Selecciona una actividad")
        self.actividad_combo.addItems(["Yoga", "Crossfit", "Boxeo", "Spinning"])
        layout.addWidget(etiquetaAct)
        layout.addWidget(self.actividad_combo)

        # QPushButton (enviar)
        self.enviar_btn = QPushButton("Enviar")
        layout.addWidget(self.enviar_btn)

        self.setLayout(layout)

        # Cargar estilos externos
        self.cargar_estilos()

    def cargar_estilos(self):
        try:
            with open("García_Daniel_estilos_T3.1.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error cargando estilos:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GimnasioForm()
    ventana.show()
    sys.exit(app.exec())
