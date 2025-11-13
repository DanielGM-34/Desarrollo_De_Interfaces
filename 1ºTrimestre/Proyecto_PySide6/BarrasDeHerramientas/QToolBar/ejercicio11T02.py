# Daniel García Méndez 2º DAM

import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana con menú y barra de herramientas")

        # creación de menú y barra de menú.
        menus_barra = self.menuBar()
        menu = menus_barra.addMenu("&Archivo")

        # Rutas de iconos
        ruta_icono_ojito = os.path.join(os.path.dirname(__file__), "ojo.png")
        ruta_icono_Cambia_Titulazo = os.path.join(os.path.dirname(__file__), "lapiz.png")
        ruta_icono_desactivar_XRP = os.path.join(os.path.dirname(__file__), "xrp.png")

        # Acción Mostrar mensaje hola
        self.muestra_hola = QAction(QIcon(ruta_icono_ojito), "Mostrar mensaje", self)
        # self.muestra_hola.setShortcut(QKeySequence("Ctrl+M"))
        self.muestra_hola.setWhatsThis("Muestra 'Hola' en la consola")
        self.muestra_hola.triggered.connect(self.imprime_hola)
        menu.addAction(self.muestra_hola)

        # Acción PARA CAmbiar título
        self.cambiar_Titulazo = QAction(QIcon(ruta_icono_Cambia_Titulazo), "Cambiar título", self)
        # self.accion_cambiar.setShortcut(QKeySequence("Ctrl+T"))
        self.cambiar_Titulazo.setWhatsThis("Cambia el título de la ventana")
        self.cambiar_Titulazo.triggered.connect(self.cambiar_titulo)
        menu.addAction(self.cambiar_Titulazo)

        # Acción Desactivar acciones
        self.accion_desactivar = QAction(QIcon(ruta_icono_desactivar_XRP), "Desactivar acciones", self)
        # self.accion_desactivar.setShortcut(QKeySequence("Ctrl+D"))
        self.accion_desactivar.setWhatsThis("Desactiva las dos acciones.")
        self.accion_desactivar.triggered.connect(self.desactivar_acciones)
        menu.addAction(self.accion_desactivar)

        #BARRA HERRAMIENTAS PRINCIPAL 
        barra_herramientas = QToolBar("Barra principal")
        # He usado ToolButtonStyle para que me muestre todas las opciones que permiten mostrar estilos 
        # enlace de referencia https://doc.qt.io/qt-6/qstyleoptiontoolbutton.html
        barra_herramientas.setToolButtonStyle(  Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        barra_herramientas.addAction(self.muestra_hola)
        barra_herramientas.addAction(self.cambiar_Titulazo)
        barra_herramientas.addAction(self.accion_desactivar)
        self.addToolBar(barra_herramientas)

        # barra secundaria
        barra_secundaria = QToolBar("Barra secundaria")
        barra_secundaria.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        activaOpciones = QAction(QIcon(ruta_icono_ojito), "Activar acciones", self)
        activaOpciones.setWhatsThis("Vuelve a activar las acciones.")
        activaOpciones.triggered.connect(self.activar_acciones)
        barra_secundaria.addAction(activaOpciones)

        self.addToolBar(barra_secundaria)

    def imprime_hola(self):
        print("Hola")

    def cambiar_titulo(self):
        self.setWindowTitle("Título cambiado")

    def desactivar_acciones(self):
        self.muestra_hola.setEnabled(False)
        self.cambiar_Titulazo.setEnabled(False)

    def activar_acciones(self):
        self.muestra_hola.setEnabled(True)
        self.cambiar_Titulazo.setEnabled(True)

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()