from PySide6.QtWidgets import(
    QApplication, QMainWindow, QPushButton,QLabel
)

class OtraVentanita(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("La otra ventanita")

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación con dos ventanas")

        self.otra_ventana=None

        self.boton=QPushButton("Mostrar/ocultar otra ventana")
        self.boton.clicked.connect(self.mostrar_otra_ventana)
        self.setCentralWidget(self.boton)

    def mostrar_otra_ventana(self):
        if self.otra_ventana is None:
            self.otra_ventana=OtraVentanita()
            self.otra_ventana.show()
        else: 
            if self.otra_ventana.isHidden():
                self.otra_ventana.move(self.pos())
                self.otra_ventana.show()
            else:
                self.otra_ventana.hide()

app=QApplication([])
window=VentanaPrincipal()
window.show()
app.exec()