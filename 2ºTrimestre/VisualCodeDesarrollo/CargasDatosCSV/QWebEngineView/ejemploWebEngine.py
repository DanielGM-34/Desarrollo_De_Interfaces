from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl, QDir
from PySide6.QtWebEngineWidgets import QWebEngineView


class VentanaInformes(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout vertical que organizará todos los elementos de la ventana
        self.layout_vertical = QVBoxLayout()
        self.setLayout(self.layout_vertical)

        # Botón para abrir el informe en el navegador
        boton_abrir = QPushButton('Abrir informe')
        boton_abrir.clicked.connect(self.abrir_informe)
        self.layout_vertical.addWidget(boton_abrir)

        # Ruta absoluta al informe HTML
        ruta_absoluta = QDir().absoluteFilePath("./DI_U05_A03_11.html")

        # Visor web para mostrar el informe dentro de la aplicación
        view = QWebEngineView()
        view.load(QUrl.fromLocalFile(ruta_absoluta))
        self.layout_vertical.addWidget(view)

        # Tamaño inicial de la ventana
        self.resize(800, 600)

    def abrir_informe(self):
        # Ruta absoluta al informe HTML
        ruta_absoluta = QDir().absoluteFilePath("./DI_U05_A03_11.html")

        # Abrir el informe en el navegador predeterminado
        QDesktopServices.openUrl(QUrl.fromLocalFile(ruta_absoluta))



app = QApplication([])
ventana_informes = VentanaInformes()
ventana_informes.show()
app.exec()