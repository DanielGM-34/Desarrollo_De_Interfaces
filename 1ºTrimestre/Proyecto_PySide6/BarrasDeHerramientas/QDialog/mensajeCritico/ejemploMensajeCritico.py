# Daniel García Méndez 2ºDAM

import sys
import platform
from PySide6.QtCore import Qt, QLibraryInfo, QTranslator
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit,
    QPushButton, QDialog, QVBoxLayout, QDialogButtonBox,QMessageBox
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con ventana emergente")

        boton = QPushButton("Haz click para ver el mensaje crítico.")
        boton.clicked.connect(self.mostrar_dialogo)

        self.setCentralWidget(boton)

    def mostrar_dialogo(self):
        boton_pulsado=QMessageBox.critical(
            self,
            "Ejemplo de cuadro de diálogo e mensaje crítico",
            "Ha ocurrido un error al realizar la acción",
            buttons=QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.NoToAll
            | QMessageBox.StandardButton.Ignore,
            defaultButton=QMessageBox.StandardButton.Discard
        )

        if boton_pulsado == QMessageBox.StandardButton.Discard:
            print("Descartado")
        
        elif boton_pulsado == QMessageBox.StandardButton.NoAll:
            print("No a todo")
        else:
            print("Ignorar.")


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


