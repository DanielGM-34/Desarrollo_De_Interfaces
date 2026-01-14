import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QCheckBox, QRadioButton, QGroupBox
)
# Necesitamos QColor y QPalette para cambiar colores desde Python (o setStyleSheet)
from PySide6.QtGui import QPalette, QColor 

class VentanaSelectores(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Repaso Examen - Lógica de Temas")
        self.resize(300, 250)

        # Widget central y layout base
        self.central_widget = QWidget() # Lo guardamos en self para acceder luego
        layout_principal = QVBoxLayout(self.central_widget)

        # --- 1. CHECKBOX ---
        self.check_terminos = QCheckBox("Aceptar términos y condiciones")
        
        # --- 2. RADIO BUTTONS ---
        grupo_modos = QGroupBox("Selecciona el Modo")
        layout_grupo = QVBoxLayout()
        
        self.radio_claro = QRadioButton("Modo Claro")
        self.radio_oscuro = QRadioButton("Modo Oscuro")
        
        # Configuración inicial
        self.radio_claro.setChecked(True)

        # --- 🔴 PARTE NUEVA: CONECTAR SEÑALES (LOGICA) ---
        # Conectamos la señal 'toggled' (cambio de estado) a nuestra función
        self.radio_claro.toggled.connect(self.cambiar_tema)
        self.radio_oscuro.toggled.connect(self.cambiar_tema)

        layout_grupo.addWidget(self.radio_claro)
        layout_grupo.addWidget(self.radio_oscuro)
        
        # Asignamos el layout al grupo (lo que faltaba antes)
        grupo_modos.setLayout(layout_grupo)

        # Añadimos todo al layout principal
        layout_principal.addWidget(self.check_terminos)
        layout_principal.addSpacing(20)
        layout_principal.addWidget(grupo_modos)
        layout_principal.addStretch()

        self.setCentralWidget(self.central_widget)
        
        # Llamamos a la función una vez al inicio para poner el color correcto
        self.cambiar_tema()

    # --- 🔴 PARTE NUEVA: EL SLOT (LA FUNCIÓN QUE HACE EL CAMBIO) ---
    def cambiar_tema(self):
        """
        Esta función se ejecuta cada vez que tocas un RadioButton.
        Comprueba cuál está marcado y cambia el color de fondo.
        """
        # Si está marcado el oscuro...
        if self.radio_oscuro.isChecked():
            # Cambiamos el estilo del widget central a oscuro
            # (Esto se suma al estilo QSS global, no lo borra)
            self.central_widget.setStyleSheet("background-color: #2c3e50; color: white;")
            self.check_terminos.setStyleSheet("color: white;") # Para que el texto se lea
            
        # Si no (es decir, está marcado el claro)...
        else:
            self.central_widget.setStyleSheet("background-color: #f0f0f0; color: black;")
            self.check_terminos.setStyleSheet("color: black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargamos el QSS externo para la FORMA de los botones (bordes, hover, etc)
    try:
        with open("estilos_ejercicio1.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ No se encontró el QSS, pero la lógica de colores funcionará igual.")

    ventana = VentanaSelectores()
    ventana.show()
    app.exec()