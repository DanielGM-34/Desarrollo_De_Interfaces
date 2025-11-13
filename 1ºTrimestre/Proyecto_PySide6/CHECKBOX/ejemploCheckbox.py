from PySide6.QtWidgets import QMainWindow, QApplication, QCheckBox
from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi aplicación.")
        widget = QCheckBox("Esto es un checkbox XRPPPPP")

        widget.setCheckState(Qt.CheckState.PartiallyChecked)
        widget.setTristate(True)
        widget.stateChanged.connect(self.muestra_estado)
        self.setCentralWidget(widget)  # ¡Importante! Para que el checkbox se muestre

    def muestra_estado(self, s):
        state = Qt.CheckState(s)
        print(state == Qt.CheckState.Checked)
        print(s)

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()
