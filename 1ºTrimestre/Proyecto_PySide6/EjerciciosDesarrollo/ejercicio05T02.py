# Daniel García Méndez 2ºDAM
from PySide6.QtWidgets import QMainWindow, QApplication, QCheckBox
from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        # Por defecto en desmarcado con valor 0
        self.checkBox = QCheckBox("Esto es un checkbox")
        
        # Por defecto en parcialmente check valor 1
        # self.checkBox.setTristate(True) 

        # Por defecto en check con valor 2
        # self.checkBox.setCheckState(Qt.CheckState.Checked)

        # Definir el título 
        self.setWindowTitle("Mi aplicación.")
        self.checkBox.setTristate(True)
        self.checkBox.stateChanged.connect(self.mostrar_estado)


        # Widget central
        self.setCentralWidget(self.checkBox)  # ¡Importante! Para que el checkbox se muestre

    def mostrar_estado(self, s):
        # Conversión a entero
        state = Qt.CheckState(s)
        if state == Qt.CheckState.Checked:
            print("Marcado completamente",s)
        elif state == Qt.CheckState.Unchecked:
            print("Desmarcado",s)
        else:
            print("Marcado parcialmente",s)

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()