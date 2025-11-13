from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QPushButton

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout horizontal")

        # Layout horizontal
        layoutHorizontal = QHBoxLayout()

        # Widget principal
        componente_principal = QWidget()
        componente_principal.setLayout(layoutHorizontal)
        self.setCentralWidget(componente_principal)

        # Crear los botones manualmente
        boton1 = QPushButton("Uno")
        boton1.setFixedHeight(50)

        boton2 = QPushButton("Dos")
        boton2.setFixedHeight(50)

        boton3 = QPushButton("Tres")
        boton3.setFixedHeight(50)

        boton4 = QPushButton("Cuatro")
        boton4.setFixedHeight(50)

        boton5 = QPushButton("Cinco")
        boton5.setFixedHeight(50)

        # Añadirlos al layout uno por uno
        layoutHorizontal.addWidget(boton1)
        layoutHorizontal.addWidget(boton2)
        layoutHorizontal.addWidget(boton3)
        layoutHorizontal.addWidget(boton4)
        layoutHorizontal.addWidget(boton5)

app = QApplication([])
windows = VentanaPrincipal()
windows.show()
app.exec()
