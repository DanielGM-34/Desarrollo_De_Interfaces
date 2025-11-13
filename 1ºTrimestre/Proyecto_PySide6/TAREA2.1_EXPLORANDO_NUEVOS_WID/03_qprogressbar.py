# Daniel García Méndez 2ºDAM 
from PySide6.QtWidgets import QApplication, QMainWindow,QProgressBar,QLabel
from PySide6.QtCore import QTimer

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.progreso_actual=0
        self.timer=QTimer(self)
        self.BarraProgresiva = QProgressBar()
        self.BarraProgresiva.setRange(0,100)
        self.setCentralWidget(self.BarraProgresiva)

        self.timer.timeout.connect(self.preguntar_usuario)
        self.BarraProgresiva.setValue(self.progreso_actual)
        self.timer.start(2000)

    def cambiar_progreso(self, modo):
        if modo == "aumentar":
            if self.progreso_actual<=80:
                self.progreso_actual+=20
                print("Progreso actual " + str(self.progreso_actual))
            elif self.progreso_actual==100:
                print("No puedes sumar más progreso porque ya ha sido completado")
        
        elif modo =="disminuir":
            if self.progreso_actual>=20:
                self.progreso_actual-=20
                print("Progreso actual " + str(self.progreso_actual))

            elif self.progreso_actual<20:
                print("No puedes restar más progreso porque progreso es menor a 20")

        self.BarraProgresiva.setValue(self.progreso_actual)
        if self.progreso_actual==100:
            self.setWindowTitle("Tarea completada")
        
        else:
            self.setWindowTitle("Progreso actual " + str(self.progreso_actual) )


    def preguntar_usuario(self):
        print("Menú de opciones:")
        print("0 salir.")
        print("1 aumentar progreso.")
        print("2 retroceder progreso.")

        op = int(input("Selecciona una opción: 0 1 2 "))
        if op == 0:
            print("Saliendo...")
            self.timer.stop()
            self.close()
        elif op == 1:
            self.cambiar_progreso("aumentar")
        elif op == 2:
            self.cambiar_progreso("disminuir")
        else:
            print("Opción inválida")

app = QApplication([])
window = VentanaPrincipal()
window.show()
app.exec()