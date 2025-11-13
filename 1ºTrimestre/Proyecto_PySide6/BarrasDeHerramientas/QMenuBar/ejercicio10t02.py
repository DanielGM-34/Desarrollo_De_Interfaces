# Daniel García Méndez 2ºDAM
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

from PySide6.QtGui import QAction, QKeySequence

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = self.menuBar().addMenu("&Archivo")

        accion_mostrar_mensaje = QAction("Mostrar mensaje", self)
        accion_cambiar_titulo = QAction("Cambiar título", self)
        accion_salir = QAction("Salir", self)

        accion_mostrar_mensaje.setShortcut(QKeySequence("Ctrl + M"))
        accion_cambiar_titulo.setShortcut(QKeySequence("Ctrl + L"))
        accion_salir.setShortcut(QKeySequence("Ctrl + Q"))

        accion_mostrar_mensaje.triggered.connect(self.imprimir_por_consola)
        accion_cambiar_titulo.triggered.connect(self.cambiarTitulo)
        accion_salir.triggered.connect(self.salir)
        
        self.setWindowTitle("Menú de herramientas")
        menu.addAction(accion_mostrar_mensaje)
        # Este es para el título
        menu.addSeparator()   
        menu.addAction(accion_cambiar_titulo)

    # Añadir separadores para salir
        menu.addSeparator()   
        menu.addAction(accion_salir)


    
    
    def imprimir_por_consola(self):
        print("Hola desde el menú")

    def cambiarTitulo(self):
        self.setWindowTitle("Título cambiado desde el menú")
    
    def salir(self):
        print("Cerrando programa")
        self.close()

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()