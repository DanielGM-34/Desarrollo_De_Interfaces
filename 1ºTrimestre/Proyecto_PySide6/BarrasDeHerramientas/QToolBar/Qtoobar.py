import os
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana con menú y barra de herramientas")

        # --- MENÚ ---
        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Menú")

        # Ruta del icono
        ruta_icono = os.path.join(os.path.dirname(__file__), "xrp.png")

        # Acción con icono, texto y descripción
        accion = QAction(QIcon(ruta_icono), "Imprimir por consola", self)
        accion.setWhatsThis("Imprime un texto por consola al pulsar el botón o atajo") # Define un texto de ayuda que aparece si el usuario activa el modo What’s This? de Qt (atajo Shift + F1).
        accion.setShortcut(QKeySequence("Ctrl+P"))
        accion.triggered.connect(self.imprimir_por_consola)
        menu.addAction(accion)

        # --- BARRA DE HERRAMIENTAS ---
        barra_herramientas = QToolBar("Barra principal")
        barra_herramientas.addAction(accion)  # Añadimos la misma acción
        self.addToolBar(barra_herramientas)

    def imprimir_por_consola(self):
        print("Acción lanzada desde el menú, la barra de herramientas o el atajo.")

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()