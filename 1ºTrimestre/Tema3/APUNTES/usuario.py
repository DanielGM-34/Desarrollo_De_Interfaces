import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QCheckBox, QRadioButton, QComboBox, QListWidget, QTableWidget,
    QTableWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QDateEdit, QTimeEdit
)
from PySide6.QtCore import Signal


# --- CampoTexto con señales personalizadas ---
class CampoTexto(QLineEdit):
    texto_valido = Signal(str)
    texto_invalido = Signal(str)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Escribe solo letras...")
        self.textChanged.connect(self._validar)

    def _validar(self, texto):
        if texto.isalpha():
            self.texto_valido.emit(texto)
        else:
            self.texto_invalido.emit(texto)


# --- Botón contador con señal personalizada ---
class BotonContador(QPushButton):
    contador_actualizado = Signal(int)

    def __init__(self):
        super().__init__("Pulsado 0 veces")
        self.__contador = 0
        self.clicked.connect(self._incrementar)

    def _incrementar(self):
        self.__contador += 1
        self.setText(f"Pulsado {self.__contador} veces")
        self.contador_actualizado.emit(self.__contador)


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
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel("")

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(QLabel("Inicia sesión"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def check_login(self):
        if self.user_input.text() == "admin" and self.pass_input.text() == "1234":
            self.main = MainWindow(self.user_input.text())
            self.main.show()
            self.close()
        else:
            self.error_label.setText("Usuario o contraseña incorrectos")
            self.user_input.clear()
            self.pass_input.clear()


# --- Ventana Principal ---
class MainWindow(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle(f"Bienvenido, {usuario}")

        main_layout = QVBoxLayout()

        # CampoTexto con señales
        campo = CampoTexto()
        campo.texto_valido.connect(lambda t: print("Texto válido:", t))
        campo.texto_invalido.connect(lambda t: print("Texto inválido:", t))
        main_layout.addWidget(campo)

        # Botón contador con señal
        boton_contador = BotonContador()
        boton_contador.contador_actualizado.connect(lambda v: print("Contador:", v))
        main_layout.addWidget(boton_contador)

        # Otros widgets básicos
        main_layout.addWidget(QLabel("Introduce tu nombre:"))
        main_layout.addWidget(QLineEdit())

        main_layout.addWidget(QLabel("Texto largo:"))
        main_layout.addWidget(QTextEdit())
        main_layout.addWidget(QPlainTextEdit("Texto plano"))

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(QPushButton("Aceptar"))
        botones_layout.addWidget(QPushButton("Cancelar"))
        main_layout.addLayout(botones_layout)

        main_layout.addWidget(QCheckBox("Acepto términos"))
        main_layout.addWidget(QRadioButton("Opción A"))
        main_layout.addWidget(QRadioButton("Opción B"))

        combo = QComboBox()
        combo.addItems(["Rojo", "Verde", "Azul"])
        main_layout.addWidget(combo)

        lista = QListWidget()
        lista.addItems(["Elemento 1", "Elemento 2", "Elemento 3"])
        main_layout.addWidget(lista)

        tabla = QTableWidget(3, 3)
        tabla.setHorizontalHeaderLabels(["Col1", "Col2", "Col3"])
        tabla.setItem(0, 0, QTableWidgetItem("Dato (0,0)"))
        main_layout.addWidget(tabla)

        main_layout.addWidget(QSpinBox())
        main_layout.addWidget(QDoubleSpinBox())

        slider = QSlider()
        slider.setMinimum(0)
        slider.setMaximum(100)
        main_layout.addWidget(slider)

        progress = QProgressBar()
        progress.setValue(50)
        main_layout.addWidget(progress)

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

        group = QGroupBox("Formulario")
        form_layout = QFormLayout()
        form_layout.addRow("Fecha:", QDateEdit())
        form_layout.addRow("Hora:", QTimeEdit())
        group.setLayout(form_layout)
        main_layout.addWidget(group)

        contenedor = QWidget()
        contenedor.setLayout(main_layout)
        self.setCentralWidget(contenedor)


# --- Main ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Estilos oscuros
    qss = """
    QWidget {
        background-color: #121212;
        font-family: "Segoe UI";
        font-size: 14px;
        color: #f0f0f0;
    }
    QPushButton {
        background-color: #1f1f1f;
        color: white;
        border-radius: 6px;
        padding: 6px 12px;
        border: 1px solid #3498db;
    }
    QPushButton:hover { background-color: #3498db; }
    QPushButton:pressed { background-color: #2980b9; }
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 2px solid #3498db;
        border-radius: 6px;
        padding: 4px;
    }
    QCheckBox::indicator {
        width: 18px; height: 18px;
        border: 1px solid #7f8c8d;
        background-color: #1e1e1e;
        border-radius: 3px;
    }
    QCheckBox::indicator:checked { background-color: #2ecc71; }
    """
    app.setStyleSheet(qss)

    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
