# Daniel García Méndez 2ºDAM

import sys
import platform
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit, QPushButton,QDialog
)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con diálogos.")

        boton = QPushButton("Haz clicl para mostrar el diálogo.")
        boton.clicked.connect(self.mostrar_dialogo)
        self.setCentralWidget(boton)

    def mostrar_dialogo(self):
        print("Click recibido, se mostrará el diálogo.")
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Ventana de diálogo.")
        dialogo.exec()

        
app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()