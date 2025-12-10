from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QCheckBox, QRadioButton, QComboBox, QListWidget, QTableWidget,
    QTableWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QDateEdit, QTimeEdit
)
import sys


# --- Pantalla de Login ---
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(QLabel("Inicia sesión"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        if self.user_input.text() == "admin" and self.pass_input.text() == "1234":
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            self.user_input.setText("")
            self.pass_input.setText("")
            self.user_input.setPlaceholderText("Usuario incorrecto")
            self.pass_input.setPlaceholderText("Intenta de nuevo")


# --- Ventana Principal ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Completa con Estilos")

        main_layout = QVBoxLayout()

        # Etiquetas y entradas
        main_layout.addWidget(QLabel("Introduce tu nombre:"))
        main_layout.addWidget(QLineEdit())

        main_layout.addWidget(QLabel("Texto largo:"))
        main_layout.addWidget(QTextEdit())
        main_layout.addWidget(QPlainTextEdit("Texto plano"))

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(QPushButton("Aceptar"))
        botones_layout.addWidget(QPushButton("Cancelar"))
        main_layout.addLayout(botones_layout)

        # CheckBox y RadioButton
        main_layout.addWidget(QCheckBox("Acepto términos"))
        main_layout.addWidget(QRadioButton("Opción A"))
        main_layout.addWidget(QRadioButton("Opción B"))

        # ComboBox y Lista
        combo = QComboBox()
        combo.addItems(["Rojo", "Verde", "Azul"])
        main_layout.addWidget(combo)

        lista = QListWidget()
        lista.addItems(["Elemento 1", "Elemento 2", "Elemento 3"])
        main_layout.addWidget(lista)

        # Tabla
        tabla = QTableWidget(3, 3)
        tabla.setHorizontalHeaderLabels(["Col1", "Col2", "Col3"])
        tabla.setItem(0, 0, QTableWidgetItem("Dato (0,0)"))
        main_layout.addWidget(tabla)

        # SpinBox y Slider
        main_layout.addWidget(QSpinBox())
        main_layout.addWidget(QDoubleSpinBox())

        slider = QSlider()
        slider.setMinimum(0)
        slider.setMaximum(100)
        main_layout.addWidget(slider)

        # Barra de progreso
        progress = QProgressBar()
        progress.setValue(50)
        main_layout.addWidget(progress)

        # Tabs
        tabs = QTabWidget()
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("Contenido de la pestaña 1"))
        tab1.setLayout(tab1_layout)

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("Contenido de la pestaña 2"))
        tab2.setLayout(tab2_layout)

        tabs.addTab(tab1, "Pestaña 1")
        tabs.addTab(tab2, "Pestaña 2")
        main_layout.addWidget(tabs)

        # GroupBox con formulario
        group = QGroupBox("Formulario")
        form_layout = QFormLayout()
        form_layout.addRow("Fecha:", QDateEdit())
        form_layout.addRow("Hora:", QTimeEdit())
        group.setLayout(form_layout)
        main_layout.addWidget(group)

        # Contenedor principal
        contenedor = QWidget()
        contenedor.setLayout(main_layout)
        self.setCentralWidget(contenedor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # --- Cargar estilos desde archivo QSS ---
    try:
        with open("APUNTES/estilos.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Archivo estilos.qss no encontrado, usando estilo por defecto.")

    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
