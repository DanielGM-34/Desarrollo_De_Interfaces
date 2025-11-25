# Daniel García Méndez 2ºDAM



import sys
import platform
from PySide6.QtCore import Qt, QLibraryInfo, QTranslator
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit,
    QPushButton, QDialog, QVBoxLayout, QDialogButtonBox,QMessageBox
)

from PySide6.QtWidgets import QMessageBox

# Ejemplos de acceso con punto:
QMessageBox.StandardButton.Ok
QMessageBox.StandardButton.Open
QMessageBox.StandardButton.Save
QMessageBox.StandardButton.Cancel
QMessageBox.StandardButton.Close
QMessageBox.StandardButton.Discard
QMessageBox.StandardButton.Apply
QMessageBox.StandardButton.Reset
QMessageBox.StandardButton.RestoreDefaults
QMessageBox.StandardButton.Help
QMessageBox.StandardButton.SaveAll
QMessageBox.StandardButton.Yes
QMessageBox.StandardButton.YesToAll
QMessageBox.StandardButton.No
QMessageBox.StandardButton.NoToAll
QMessageBox.StandardButton.Abort
QMessageBox.StandardButton.Retry
QMessageBox.StandardButton.Ignore


class OtraVentanita(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("La otra ventanita")

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con ventana emergente")

        boton = QPushButton("Gestionar tarea")
        boton.clicked.connect(self.mostrar_dialogo)

        self.setCentralWidget(boton)

    def mostrar_dialogo(self):
        boton_pulsado=QMessageBox.question(
            self,
            "Acción sobre la tarea",
            "¿Qué quieres hacer con la tarea seleccionada?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Ignore,
            defaultButton=QMessageBox.StandardButton.Ignore
        )

        if boton_pulsado == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Resultado",
                "La tarea se ha completado."
            )

        elif boton_pulsado == QMessageBox.StandardButton.No:
              QMessageBox.information(
                self,
                "Resultado",
                "La tarea se ha pospuesto para más tarde."
            )

        
  
        else:
            QMessageBox.information(
                self,
                "Resultado",
                "La tarea se mantiene sin cambios."
            )


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


