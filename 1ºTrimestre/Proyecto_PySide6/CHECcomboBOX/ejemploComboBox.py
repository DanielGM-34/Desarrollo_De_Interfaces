from PySide6.QtWidgets import QMainWindow, QApplication, QComboBox
from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi aplicación.")

        self.combo = QComboBox()
        self.combo.addItems(["Uno", "Dos", "Tres"])

        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.combo.setMaxCount(9)

        self.combo.currentIndexChanged.connect(self.cambio_indice)
        self.combo.currentTextChanged.connect(self.cambio_texto)
        

        self.setCentralWidget(self.combo)  # Corrección aquí

    def cambio_indice(self, y):
        print("Índice seleccionado: ", y)
    
    def cambio_texto(self, s):
        print("Texto seleccionado: ", s)

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()
