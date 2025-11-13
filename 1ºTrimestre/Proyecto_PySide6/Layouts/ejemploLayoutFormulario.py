from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QPushButton,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout vertical")
        
        # Creamos un objeto layout formulario
        layout_form = QFormLayout()
        componente_principal = QWidget()
        componente_principal.setLayout(layout_form)
        self.setCentralWidget(componente_principal)

        # Añadimos los widgets al formulario
        layout_form.addRow(QLabel("Texto:"), QLineEdit())
        layout_form.addRow(QLabel("Entero:"), QSpinBox())
        layout_form.addRow(QLabel("Decimal:"), QDoubleSpinBox())

        combo = QComboBox()
        combo.addItems(["Sevilla", "Huelva", "Córdoba", "Almería"])
        layout_form.addRow(QLabel("Ciudad:"), combo)


app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()
