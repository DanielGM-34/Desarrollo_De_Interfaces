# Daniel García Méndez 2ºDAM

import sys
import platform
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QDockWidget, QTextEdit
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejercicio - Componentes flotantes.")

        #  BARRA DE ESTADO 
        barra_estado = self.statusBar()
        barra_estado.addPermanentWidget(QLabel(platform.system()))
        barra_estado.showMessage("Listo. Paneles creados correctamente.", 3000)

        #  COMPONENTE FLOTANTE (DOCK)
        # Panel 1: Fijo
        dock1_panel1 = QDockWidget("Panel 1", self)
        dock1_panel1.setWidget(QTextEdit("Panel de notas"))
        dock1_panel1.setMinimumWidth(100)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock1_panel1)
        dock1_panel1.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Panel 2: Flotante
        dock2_panel2 = QDockWidget("Panel 2", self)
        dock2_panel2.setWidget(QLabel("Panel de estado"))
        dock2_panel2.setMinimumWidth(100)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock2_panel2)
        dock2_panel2.setFeatures( QDockWidget.DockWidgetFeature.DockWidgetMovable|QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        # Panel 3: Flotante y cerrable
        dock3_panel3 = QDockWidget("Panel 3", self)
        dock3_panel3.setWidget(QLabel("Panel de ayuda"))
        dock3_panel3.setMinimumWidth(100)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock3_panel3)
        dock3_panel3.setFeatures( QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                                 QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                 QDockWidget.DockWidgetFeature.DockWidgetClosable)
        # COMPONENTE CENTRAL
        self.setCentralWidget(QLabel("Área principal de la aplicación"))

        # BARRA DE HERRAMIENTAS 
        barra_herramientas = QToolBar("Barra de herramientas")
        self.addToolBar(barra_herramientas)

        accion_imprimir = QAction(QIcon(), "Imprimir por consola", self)
        accion_imprimir.setShortcut(QKeySequence("Ctrl+I"))
        accion_imprimir.triggered.connect(self.imprimir_por_consola)

        barra_herramientas.addAction(accion_imprimir)

    def imprimir_por_consola(self):
        print("Acción lanzada desde el menú, el atajo o la barra de herramientas.")

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()