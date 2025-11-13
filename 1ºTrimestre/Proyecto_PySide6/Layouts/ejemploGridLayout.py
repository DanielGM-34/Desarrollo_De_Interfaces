from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
)
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout cuadrícula")
        # Creamos un objeto layout cuadrícula
        layout_cuadricula = QGridLayout()
        componente_principal = QWidget()
        componente_principal.setLayout(layout_cuadricula)
        self.setCentralWidget(componente_principal)
        # Añadimos cuatro botones a la primera fila
        # Los números indican la fila y la columna donde situar el widget
        layout_cuadricula.addWidget(QPushButton("0,0"), 0, 0)
        layout_cuadricula.addWidget(QPushButton("0,1"), 0, 1)
        layout_cuadricula.addWidget(QPushButton("0,2"), 0, 2)
        layout_cuadricula.addWidget(QPushButton("0,3"), 0, 3)
        # Añadimos un botón a la segunda fila que ocupe cuatro columnas
        layout_cuadricula.addWidget(QPushButton("1,0-3"), 1, 0, 1, 4)
        # Añadimos dos botones a la tercera fila, que ocupen dos columnas cada uno

        # Los dos primeros son la posiciòn y los restantes el nº de filas y comlumnas.
        layout_cuadricula.addWidget(QPushButton("2,0-1"), 2, 0, 1, 2)
        layout_cuadricula.addWidget(QPushButton("2,2-3"), 2, 2, 1, 2)

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()