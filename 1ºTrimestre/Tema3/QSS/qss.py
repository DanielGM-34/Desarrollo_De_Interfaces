from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo de QSS")

        # --- Widgets ---
        self.label = QLabel("Introduce tu nombre:")
        self.input_nombre = QLineEdit()
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_cancelar = QPushButton("Cancelar")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.boton_aceptar)
        layout.addWidget(self.boton_cancelar)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        # --- Hoja de estilos QSS aplicada a la ventana ---
        estilos = """
        /* Fondo general de la ventana */
        QMainWindow {
            background-color: #f5f5f5;
        }

        /* Estilo para la etiqueta */
        QLabel {
            font-size: 16px;
            color: #2c3e50;
        }

        /* Estilo para la caja de texto */
        QLineEdit {
            background-color: white;
            border: 2px solid #3498db;
            border-radius: 5px;
            padding: 4px;
            font-size: 14px;
        }

        /* Estilo general de los botones */
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        }

        /* Cambio de color al pasar el ratón por encima del botón */
        QPushButton:hover {
            background-color: #2980b9;
        }

        /* Cambio de color cuando el botón está pulsado */
        QPushButton:pressed {
            background-color: #1f5f8b;
        }
        """

        self.setStyleSheet(estilos)


app = QApplication([])
app.setStyle("Fusion")

ventana = MainWindow()
ventana.show()
app.exec()
