from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi aplicación")

        widget = QLabel("Hello")
        widget.setPixmap(QPixmap("gato.jpg"))
        widget.setScaledContents(True)
        self.setCentralWidget(widget)

app= QApplication([])
window= VentanaPrincipal()
window.show()
app.exec()
