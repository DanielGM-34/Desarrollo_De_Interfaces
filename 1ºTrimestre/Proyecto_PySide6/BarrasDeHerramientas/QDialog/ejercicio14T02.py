# Daniel García Méndez 2ºDAM

import platform
from PySide6.QtCore import Qt, QLibraryInfo, QTranslator
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit,
    QPushButton, QDialog, QVBoxLayout, QDialogButtonBox
)


class DialogoPersonalizado(QDialog):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setWindowTitle("Diálogo personalizado.")

        # Crear botones 
        botones = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No |QDialogButtonBox.StandardButton.Help
        caja = QDialogButtonBox(botones)

        # Guardar referencias a cada botón
        self.boton_si = caja.button(QDialogButtonBox.StandardButton.Yes)
        self.boton_no = caja.button(QDialogButtonBox.StandardButton.No)
        self.boton_ayuda = caja.button(QDialogButtonBox.StandardButton.Help)

        self.boton_si.clicked.connect(self.pulsar_yes)
        self.boton_no.clicked.connect(self.pulsar_no)
        self.boton_ayuda.clicked.connect(self.pulsar_help)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Selecciona el modo de operación que quieres activar:"))
        layout.addWidget(caja)
        self.setLayout(layout)

    def pulsar_yes(self):
        self.boton_pulsado = "Yes"
        self.accept()

    def pulsar_no(self):
        self.boton_pulsado = "No"
        self.accept()

    def pulsar_help(self):
        self.boton_pulsado = "Help"
        self.reject()


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selección de modo de operación")

        boton = QPushButton("Elegir modo")
        boton.clicked.connect(self.mostrar_dialogo)
        self.setCentralWidget(boton)

    def mostrar_dialogo(self):
        print("Click recibido, se mostrará el diálogo personalizado.")
        dialogo = DialogoPersonalizado(self)
        dialogo.setWindowTitle("Ventana de diálogo.")

        resultado = dialogo.exec()
        if resultado == QDialog.DialogCode.Accepted:
            if dialogo.boton_pulsado == "Yes":
                print("Modo A activado")
            elif dialogo.boton_pulsado == "No":
                print("Modo B activado")
        else:
            print("Se ha solicitado ayuda")


def cargar_traductor(app):
    traductor = QTranslator(app)
    ruta = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    traductor.load("qt_es", ruta)
    app.installTranslator(traductor)


app = QApplication([])
cargar_traductor(app)
ventana = VentanaPrincipal()
ventana.show()
app.exec()
