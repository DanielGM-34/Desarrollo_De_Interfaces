# Daniel García Méndez 2DAM

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QPushButton, QHBoxLayout, QVBoxLayout
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layouts anidados")
        contenedorWidget = QWidget()
        self.setCentralWidget(contenedorWidget)

        # Este layout contendrá los dos layouts h y v.
        layout_contenedor = QHBoxLayout()
        contenedorWidget.setLayout(layout_contenedor)

        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(QPushButton("H1"))
        layout_horizontal.addWidget(QPushButton("H2"))
        layout_horizontal.addWidget(QPushButton("H3"))
        layout_horizontal.addWidget(QPushButton("H4"))

        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(QPushButton("V1"))
        layout_vertical.addWidget(QPushButton("V2"))
        layout_vertical.addWidget(QPushButton("V3"))
        layout_vertical.addWidget(QPushButton("V4"))
        
        layout_contenedor.addLayout(layout_vertical)
        layout_contenedor.addLayout(layout_horizontal)
        



app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()
