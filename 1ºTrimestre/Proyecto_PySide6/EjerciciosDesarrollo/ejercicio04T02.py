# Daniel García Méndez 2ºDAM

import os
import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

basedir = os.path.dirname(__file__)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Mi aplicación")

        widget = QLabel("Helloo")
        widget.setPixmap(QPixmap(os.path.join(basedir, "gato.jpg")))

        widget.setScaledContents(True)
        self.setCentralWidget(widget)

app=QApplication(sys.argv)
windows = VentanaPrincipal()
windows.show()
# Directorio padre que tiene todas las carpetas
print("Carpeta de trabajo actual: ", os.getcwd())

# Directorio de trabajo actual 
print("Ruta del archivo actual: ", basedir )
app.exec()

