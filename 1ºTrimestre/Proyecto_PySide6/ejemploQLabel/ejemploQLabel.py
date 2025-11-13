from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
class ventanaPrin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi aplicacion")
        etiqueta = QLabel("Holaa")
        fuente = etiqueta.font()
        fuente.setPointSize(30)
        etiqueta.setFont(fuente)


        etiqueta.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(etiqueta)


app = QApplication([])
window = ventanaPrin()
window.show()
app.exec()