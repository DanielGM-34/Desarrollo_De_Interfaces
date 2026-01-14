import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QCheckBox, QPushButton,
    QTabWidget, QGroupBox, QMessageBox
)

class VentanaExamen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Examen: Registro con Pestañas")
        self.resize(450, 400)

        # 1. Crear el componente de Pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs) # Las pestañas son el centro de la ventana

        # 2. Crear las dos pestañas (son widgets vacíos al principio)
        self.pestana1 = QWidget()
        self.pestana2 = QWidget()

        # 3. Añadirlas al controlador de pestañas
        self.tabs.addTab(self.pestana1, "Formulario Registro")
        self.tabs.addTab(self.pestana2, "Información")

        # 4. Configurar el contenido de cada pestaña
        self.configurar_pestana_formulario()
        self.configurar_pestana_info()

    def configurar_pestana_formulario(self):
        """Aquí metemos todo el formulario que pidió la profesora"""
        layout_principal = QVBoxLayout()

        # --- CAMPO DE TEXTO ---
        self.label_nombre = QLabel("Nombre del Alumno:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Escribe tu nombre aquí...")

        # --- RADIO BUTTONS (Grupo exclusivo) ---
        self.group_turno = QGroupBox("Turno Preferente")
        layout_radio = QVBoxLayout()
        
        self.radio_morning = QRadioButton("Mañana")
        self.radio_afternoon = QRadioButton("Tarde")
        self.radio_morning.setChecked(True) # Marcar uno por defecto

        layout_radio.addWidget(self.radio_morning)
        layout_radio.addWidget(self.radio_afternoon)
        self.group_turno.setLayout(layout_radio)

        # --- CHECKBOX ---
        self.check_terminos = QCheckBox("Acepto las condiciones del centro")

        # --- BOTONES (Enviar y Borrar) ---
        layout_botones = QHBoxLayout()
        
        self.btn_enviar = QPushButton("Enviar Datos")
        # IMPORTANTE: Le damos un ID para que el QSS sepa cuál es cuál (Verde)
        self.btn_enviar.setObjectName("btnEnviar")
        # Conectar lógica
        self.btn_enviar.clicked.connect(self.accion_enviar)

        self.btn_borrar = QPushButton("Borrar Campos")
        # IMPORTANTE: ID para el QSS (Rojo)
        self.btn_borrar.setObjectName("btnBorrar")
        # Conectar lógica
        self.btn_borrar.clicked.connect(self.accion_borrar)

        layout_botones.addWidget(self.btn_borrar)
        layout_botones.addWidget(self.btn_enviar)

        # --- AÑADIR TODO AL LAYOUT DE LA PESTAÑA 1 ---
        layout_principal.addWidget(self.label_nombre)
        layout_principal.addWidget(self.input_nombre)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.group_turno)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.check_terminos)
        layout_principal.addStretch() # Empujar botones al final
        layout_principal.addLayout(layout_botones)

        # Asignar el layout a la pestaña
        self.pestana1.setLayout(layout_principal)

    def configurar_pestana_info(self):
        """Segunda pestaña simple para rellenar hueco"""
        layout = QVBoxLayout()
        lbl = QLabel("Instrucciones del Examen:\n\n1. Rellena el formulario.\n2. Pulsa Enviar.\n3. Si te equivocas, pulsa Borrar.")
        layout.addWidget(lbl)
        self.pestana2.setLayout(layout)

    # --- LÓGICA DE LOS BOTONES ---

    def accion_borrar(self):
        """Limpia todos los campos"""
        self.input_nombre.clear()
        self.radio_morning.setChecked(True) # Volver al default
        self.check_terminos.setChecked(False)
        print("Campos borrados.")

    def accion_enviar(self):
        """Simula el envío y valida"""
        nombre = self.input_nombre.text()
        
        # Validación simple
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
            return

        if not self.check_terminos.isChecked():
            QMessageBox.warning(self, "Error", "Debes aceptar los términos.")
            return
        
        # Si todo está bien
        turno = "Mañana" if self.radio_morning.isChecked() else "Tarde"
        mensaje = f"Datos Enviados:\nNombre: {nombre}\nTurno: {turno}"
        QMessageBox.information(self, "Éxito", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga del QSS
    try:
        # AQUI ESTA LA CLAVE: añadimos encoding="utf-8"
        with open("estilos_examen.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print("✅ Estilos cargados correctamente.")
    except FileNotFoundError:
        print("⚠️ NO SE ENCONTRÓ EL QSS. La app funcionará pero se verá fea.")
    except Exception as e:
        print(f"⚠️ Otro error cargando estilos: {e}")

    ventana = VentanaExamen()
    ventana.show()
    sys.exit(app.exec())