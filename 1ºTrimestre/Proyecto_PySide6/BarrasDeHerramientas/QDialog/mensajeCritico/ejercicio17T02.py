# Daniel García Méndez 2ºDAM

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QMessageBox, QMainWindow
)


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")

        # Campo usuario
        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Usuario")

        # Campo contraseña
        self.campo_password = QLineEdit()
        self.campo_password.setPlaceholderText("Contraseña")
        self.campo_password.setEchoMode(QLineEdit.EchoMode.Password)
        

        # Botón validar
        self.boton_validar = QPushButton("Validar")
        self.boton_validar.clicked.connect(self.validar)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Introduce tus credenciales"))
        layout.addWidget(self.campo_usuario)
        layout.addWidget(self.campo_password)
        layout.addWidget(self.boton_validar)

        self.setLayout(layout)

    def validar(self):
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()

        if usuario == "admin" and password == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario o la contraseña son incorrectos")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana principal")

        # Contenido principal
        etiqueta = QLabel("Ventana principal", self)
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(etiqueta)


app = QApplication(sys.argv)

# Mostrar diálogo de login
login = LoginDialog()
if login.exec() == QDialog.DialogCode.Accepted:
    ventana = VentanaPrincipal()
    ventana.showMaximized()
    sys.exit(app.exec())
else:
    sys.exit(0)
