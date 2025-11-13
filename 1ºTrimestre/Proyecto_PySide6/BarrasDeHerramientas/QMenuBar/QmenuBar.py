from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

from PySide6.QtGui import QAction, QKeySequence

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = self.menuBar().addMenu("&Archivo")

        accion = QAction("Imprimir", self)


        accion.setShortcut(QKeySequence("Ctrl + P"))

        accion.triggered.connect(self.imprimir_por_consola)
        
        self.setWindowTitle("Menú de herramientas")
        menu.addAction(accion)

    
    
    def imprimir_por_consola(self):
        print("Imprimir por consola con el atajo CTRL+P")

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()