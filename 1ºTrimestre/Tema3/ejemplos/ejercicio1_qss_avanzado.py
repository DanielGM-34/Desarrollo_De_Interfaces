import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QComboBox, QPushButton, QLabel
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EJERCICIO 1: Panel de Búsqueda")
        self.resize(350, 300)
        
        # --- WIDGETS ---
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Hola") # Texto ejemplo foto
        
        # Combo box
        self.combo_category = QComboBox()
        self.combo_category.addItems(["Ropa", "Electrónica", "Libros"])
        
        # Botón Aplicar
        self.btn_filter = QPushButton("Aplicar Filtro")
        self.btn_filter.clicked.connect(self.ejecutar_filtro)

        # ETIQUETA DE RESULTADO
        self.label_resultado = QLabel("Esperando filtro...")
        self.label_resultado.setAlignment(Qt.AlignCenter)
        
        # IMPORTANTE: Le ponemos un ID para que el QSS lo reconozca
        self.label_resultado.setObjectName("LabelResultado")
        # Establecemos la propiedad inicial en 'inactivo'
        self.label_resultado.setProperty("estado", "inactivo")

        # Botón inferior
        self.btn_disabled = QPushButton("Botón Deshabilitado")
        self.btn_disabled.setEnabled(False) 

        # --- LAYOUTS (Igual que antes) ---
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.combo_category)
        search_layout.addWidget(self.btn_filter)
        
        contenedor_central = QWidget()
        layout = QVBoxLayout(contenedor_central)
        layout.setSpacing(15) # Un poco de aire entre elementos
        
        layout.addWidget(QLabel("Filtro de Búsqueda:"))
        layout.addWidget(self.input_search)
        layout.addLayout(search_layout)
        layout.addWidget(self.label_resultado)
        layout.addWidget(self.btn_disabled) 
        
        self.setCentralWidget(contenedor_central)
        
        # Lógica para habilitar el botón de abajo al escribir
        self.input_search.textChanged.connect(self.validar_texto)


    def validar_texto(self, texto):
        if len(texto) > 0:
            self.btn_disabled.setEnabled(True)
            self.btn_disabled.setText("Botón Habilitado")
        else:
            self.btn_disabled.setEnabled(False)

    def ejecutar_filtro(self):
        # 1. Cambiar el texto
        texto = self.input_search.text()
        categoria = self.combo_category.currentText()
        if not texto: texto = "..."
            
        self.label_resultado.setText(f"Buscando: {texto}\nEn: {categoria}")
        
        # 2. CAMBIAR EL ESTILO VÍA PROPIEDAD DINÁMICA
        # Cambiamos la propiedad 'estado' a 'activo'
        self.label_resultado.setProperty("estado", "activo")
        
        # 3. REFRESCAR ESTILO (Obligatorio para propiedades personalizadas)
        # Esto le dice a Qt: "Oye, he cambiado una propiedad, vuelve a leer el QSS"
        self.label_resultado.style().unpolish(self.label_resultado)
        self.label_resultado.style().polish(self.label_resultado)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga del QSS
    try:
        with open("Sandoval_Cristina_estilos_T3.1.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo .qss primero")

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())