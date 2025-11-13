# Daniel García Méndez 2ºDAM
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
class ventanaPrin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi aplicacion")
        etiqueta = QLabel("Sistema en espera")
        fuente = etiqueta.font()
        fuente.setPointSize(24)
        etiqueta.setFont(fuente)

        etiqueta.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.setCentralWidget(etiqueta)

        etiqueta.setText("Sistema en reiniciado")


app = QApplication([])
window = ventanaPrin()
window.show()
app.exec()