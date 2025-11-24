import os
import platform
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana con menú, barra de herramientas y componente flotante")

        # --- MENÚ Y ACCIÓN ---
        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Menú")

        ruta_icono = os.path.join(os.path.dirname(__file__), "console-log-icon.png")
        accion = QAction(QIcon(ruta_icono), "Imprimir por consola", self)
        accion.setStatusTip("Imprimir por consola")
        accion.setShortcut(QKeySequence("Ctrl+P"))
        accion.triggered.connect(self.imprimir_por_consola)
        menu.addAction(accion)

        # --- BARRA DE HERRAMIENTAS ---
        barra_herramientas = QToolBar("Barra principal")
        barra_herramientas.addAction(accion)
        self.addToolBar(barra_herramientas)

        # --- BARRA DE ESTADO ---
        barra_estado = self.statusBar()
        barra_estado.addPermanentWidget(QLabel(platform.system()))
        barra_estado.showMessage("Listo. Esperando acción...", 3000)

        # --- COMPONENTE FLOTANTE (DOCK) ---
        dock1 = QDockWidget("Componente base 1", self)
        dock1.setWidget(QTextEdit(""))
        dock1.setMinimumWidth(50)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock1)

        # --- COMPONENTE CENTRAL ---
        self.setCentralWidget(QLabel("Componente principal"))

    def imprimir_por_consola(self):
        print("Acción lanzada desde el menú, el atajo o la barra de herramientas.")

if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()