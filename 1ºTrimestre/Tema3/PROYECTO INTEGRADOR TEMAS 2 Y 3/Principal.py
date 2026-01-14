from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream
from Ventana_principal import VentanaPrincipal
import sys  

def cargar_qss(app):
    archivo = QFile("Garcia_Daniel_estilos.qss")
    if archivo.exists() and archivo.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(archivo)
        qss = stream.readAll()
        app.setStyleSheet(qss)
        archivo.close()

def main():
    app = QApplication(sys.argv)
    cargar_qss(app)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
