import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton
)


class BotonPrimario(QPushButton):
    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setProperty("tipo", "primario")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login con estilos QSS")

        # --- Widgets ---
        label_usuario = QLabel("Usuario:")
        self.input_usuario = QLineEdit()

        label_password = QLabel("Contraseña:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        boton_aceptar = BotonPrimario("Aceptar")
        boton_cancelar = QPushButton("Cancelar")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(boton_aceptar)
        layout.addWidget(boton_cancelar)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Estilo Fusion para que QSS sea más consistente
    app.setStyle("Fusion")

    # Cargar estilos desde fichero .qss
    with open("APUNTES/estilos.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    ventana = MainWindow()
    ventana.show()

    sys.exit(app.exec())
