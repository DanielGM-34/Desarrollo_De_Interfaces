# Daniel García Méndez 2ºDAM


import sys
import os
import platform
import getpass
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EJERCICIO 12")

          # --- RUTAS DE ICONOS ---
        base = os.path.dirname(__file__)
        icono_tiempo = os.path.join(base, "tiempo.png")
        icono_limpiar = os.path.join(base, "limpia.png")
        icono_info_SISTEMA = os.path.join(base, "infoSO.png")

        # --- MENÚ ---
        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Archivo")

        # --- ACCIONES ---
        accion_mensaje = QAction(QIcon(icono_tiempo),"Mostrar mensaje temporal", self)
        accion_mensaje.setShortcut(QKeySequence("Ctrl+T"))
        accion_mensaje.triggered.connect(self.mostrar_mensaje_temporal)

        accion_limpiar = QAction(QIcon(icono_limpiar),"Limpiar mensaje", self)
        accion_limpiar.setShortcut(QKeySequence("Ctrl+L"))
        accion_limpiar.triggered.connect(self.limpiar_mensaje)

        accion_info = QAction(QIcon(icono_info_SISTEMA),"Mostrar información del sistema", self)
        accion_info.setShortcut(QKeySequence("Ctrl+I"))
        accion_info.triggered.connect(self.mostrar_info_sistema)

        # Añadir acciones al menú
        menu.addAction(accion_mensaje)
        menu.addAction(accion_limpiar)
        menu.addAction(accion_info)

        # --- BARRA DE HERRAMIENTAS ---
        barra_herramientas = QToolBar("Barra principal")
        barra_herramientas.addAction(accion_mensaje)
        barra_herramientas.addAction(accion_limpiar)
        barra_herramientas.addAction(accion_info)
        self.addToolBar(barra_herramientas)

        # --- BARRA DE ESTADO ---
        self.barra_estado = self.statusBar()
        self.barra_estado.showMessage("Aplicación iniciada correctamente", 2000)

        usuario = getpass.getuser()
        self.barra_estado.addPermanentWidget(QLabel("Usuario: " + usuario))

        # --- QTimer ---
        self.indice_mensaje = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cambiar_mensaje)
        self.timer.start(5000)

    def mostrar_mensaje_temporal(self):
        self.barra_estado.showMessage("Mensaje temporal: desaparece en 3 segundos", 3000)

    def limpiar_mensaje(self):
        self.barra_estado.clearMessage()

    def mostrar_info_sistema(self):
        sistema = platform.system()
        self.barra_estado.addWidget(QLabel("Sistema: " + sistema))

    def cambiar_mensaje(self):
        if self.indice_mensaje == 0:
            self.barra_estado.showMessage("Esperando acción...", 5000)
            self.indice_mensaje = 1
        else:
            self.barra_estado.showMessage("Listo para trabajar", 5000)
            self.indice_mensaje = 0

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()