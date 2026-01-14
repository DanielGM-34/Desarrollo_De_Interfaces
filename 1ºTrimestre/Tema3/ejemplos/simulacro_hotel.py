import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QComboBox, QDateEdit, QSpinBox, QProgressBar, QSlider, QDial,
    QMessageBox, QToolBar
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QDate

class HotelManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Hotelera 'Grand PySide' ⭐⭐⭐⭐⭐")
        self.resize(700, 650)

        # --- 1. MENÚS Y BARRAS ---
        self.setup_menu()

        # --- 2. WIDGET CENTRAL ---
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # LAYOUT PRINCIPAL (Vertical)
        # Este layout contiene toda la ventana de arriba a abajo
        main_layout = QVBoxLayout(widget_central)

        # =================================================================
        # SECCIÓN 1: DATOS DEL HUÉSPED (Layouts Anidados)
        # =================================================================
        grupo_cliente = QGroupBox("1. Datos del Huésped")
        layout_cliente_v = QVBoxLayout() # Vertical dentro del grupo

        # FILA 1: Nombre y Apellido (Horizontal)
        fila1_h = QHBoxLayout() 
        
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre...")
        self.input_nombre.textChanged.connect(self.validar_progreso) # Lógica

        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Apellido...")
        self.input_apellido.textChanged.connect(self.validar_progreso)

        fila1_h.addWidget(QLabel("Nombre:"))
        fila1_h.addWidget(self.input_nombre)
        fila1_h.addWidget(QLabel("Apellido:"))
        fila1_h.addWidget(self.input_apellido)

        layout_cliente_v.addLayout(fila1_h) # Añadimos la fila horizontal al vertical

        # FILA 2: Fecha Entrada y Noches (Horizontal)
        fila2_h = QHBoxLayout()
        
        self.input_fecha = QDateEdit()
        self.input_fecha.setDate(QDate.currentDate()) # Fecha de hoy
        self.input_fecha.setCalendarPopup(True) # Desplegable bonito

        self.input_noches = QSpinBox()
        self.input_noches.setRange(1, 30)
        self.input_noches.setSuffix(" noches")

        fila2_h.addWidget(QLabel("Check-in:"))
        fila2_h.addWidget(self.input_fecha)
        fila2_h.addWidget(QLabel("Duración:"))
        fila2_h.addWidget(self.input_noches)

        layout_cliente_v.addLayout(fila2_h)
        
        grupo_cliente.setLayout(layout_cliente_v)
        main_layout.addWidget(grupo_cliente)

        # =================================================================
        # SECCIÓN 2: PREFERENCIAS (Sliders y Diales)
        # =================================================================
        grupo_pref = QGroupBox("2. Confort de la Habitación")
        layout_pref_h = QHBoxLayout() # Todo en horizontal

        # COLUMNA IZQUIERDA: Temperatura (Slider)
        layout_temp = QVBoxLayout()
        self.lbl_temp = QLabel("Temperatura: 22°C")
        self.lbl_temp.setAlignment(Qt.AlignCenter)
        
        self.slider_temp = QSlider(Qt.Horizontal)
        self.slider_temp.setRange(16, 30)
        self.slider_temp.setValue(22)
        # Conectar señal
        self.slider_temp.valueChanged.connect(self.actualizar_temp)

        layout_temp.addWidget(self.lbl_temp)
        layout_temp.addWidget(self.slider_temp)

        # COLUMNA DERECHA: Iluminación (Dial/Rueda)
        layout_luz = QVBoxLayout()
        self.lbl_luz = QLabel("Iluminación: 50%")
        self.lbl_luz.setAlignment(Qt.AlignCenter)

        self.dial_luz = QDial()
        self.dial_luz.setRange(0, 100)
        self.dial_luz.setValue(50)
        self.dial_luz.setNotchesVisible(True) # Muescas visuales
        self.dial_luz.valueChanged.connect(self.actualizar_luz)

        layout_luz.addWidget(self.lbl_luz)
        layout_luz.addWidget(self.dial_luz)

        # Añadimos las dos columnas al layout horizontal del grupo
        layout_pref_h.addLayout(layout_temp)
        layout_pref_h.addLine = QWidget() # Separador visual (truco)
        layout_pref_h.addLayout(layout_luz)

        grupo_pref.setLayout(layout_pref_h)
        main_layout.addWidget(grupo_pref)

        # =================================================================
        # SECCIÓN 3: EXTRAS Y NOTAS
        # =================================================================
        layout_extras = QHBoxLayout()

        # Izquierda: Checkboxes y Radios
        layout_opciones = QVBoxLayout()
        self.chk_desayuno = QCheckBox("Incluir Desayuno Premium")
        self.chk_spa = QCheckBox("Acceso al Spa")
        
        self.radio_std = QRadioButton("Habitación Estándar")
        self.radio_vip = QRadioButton("Suite VIP (+100€)")
        self.radio_std.setChecked(True)

        layout_opciones.addWidget(QLabel("<b>Extras:</b>"))
        layout_opciones.addWidget(self.chk_desayuno)
        layout_opciones.addWidget(self.chk_spa)
        layout_opciones.addSpacing(10)
        layout_opciones.addWidget(QLabel("<b>Tipo:</b>"))
        layout_opciones.addWidget(self.radio_std)
        layout_opciones.addWidget(self.radio_vip)

        # Derecha: Bloc de notas
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Peticiones especiales (alérgias, cuna, etc)...")
        self.txt_notas.textChanged.connect(self.validar_progreso)

        layout_extras.addLayout(layout_opciones)
        layout_extras.addWidget(self.txt_notas)

        main_layout.addLayout(layout_extras)

        # =================================================================
        # SECCIÓN 4: BARRA DE PROGRESO Y BOTONES
        # =================================================================
        main_layout.addSpacing(10)
        main_layout.addWidget(QLabel("Progreso de la Reserva:"))
        
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setRange(0, 100)
        self.barra_progreso.setValue(0)
        main_layout.addWidget(self.barra_progreso)

        # Botonera Inferior
        layout_botones = QHBoxLayout()
        
        self.btn_limpiar = QPushButton("Limpiar Todo")
        self.btn_limpiar.setObjectName("btnLimpiar") # ID Naranja
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

        self.btn_confirmar = QPushButton("CONFIRMAR RESERVA")
        self.btn_confirmar.setObjectName("btnConfirmar") # ID Azul
        self.btn_confirmar.setEnabled(False) # Empieza apagado
        self.btn_confirmar.clicked.connect(self.confirmar_reserva)

        layout_botones.addWidget(self.btn_limpiar)
        layout_botones.addStretch()
        layout_botones.addWidget(self.btn_confirmar)

        main_layout.addLayout(layout_botones)

    # ---------------------------------------------------------------------
    # LÓGICA (SLOTS)
    # ---------------------------------------------------------------------

    def setup_menu(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        accion_salir = QAction("Salir", self)
        accion_salir.triggered.connect(self.close)
        toolbar.addAction(accion_salir)

    def actualizar_temp(self, valor):
        self.lbl_temp.setText(f"Temperatura: {valor}°C")

    def actualizar_luz(self, valor):
        self.lbl_luz.setText(f"Iluminación: {valor}%")

    def validar_progreso(self):
        """Calcula el % completado y activa/desactiva el botón"""
        progreso = 0
        
        # 1. Validar Nombre (33%)
        texto_nombre = self.input_nombre.text().strip()
        if len(texto_nombre) > 2:
            progreso += 33
            self.input_nombre.setProperty("estado", "ok")
        else:
            self.input_nombre.setProperty("estado", "error")
        
        # 2. Validar Apellido (33%)
        texto_apellido = self.input_apellido.text().strip()
        if len(texto_apellido) > 2:
            progreso += 33
            self.input_apellido.setProperty("estado", "ok")
        else:
            self.input_apellido.setProperty("estado", "error")

        # 3. Validar Notas (34%) - Opcional pero cuenta para el 100%
        if len(self.txt_notas.toPlainText()) > 5:
            progreso += 34
        
        # Actualizar visualmente
        self.barra_progreso.setValue(progreso)
        
        # Refrescar estilos dinámicos
        self.input_nombre.style().unpolish(self.input_nombre)
        self.input_nombre.style().polish(self.input_nombre)
        self.input_apellido.style().unpolish(self.input_apellido)
        self.input_apellido.style().polish(self.input_apellido)

        # Activar botón solo si tenemos nombre y apellido (mínimo 66%)
        if progreso >= 66:
            self.btn_confirmar.setEnabled(True)
            self.btn_confirmar.setText(f"CONFIRMAR RESERVA ({progreso}%)")
        else:
            self.btn_confirmar.setEnabled(False)
            self.btn_confirmar.setText("Faltan datos...")

    def limpiar_formulario(self):
        self.input_nombre.clear()
        self.input_apellido.clear()
        self.txt_notas.clear()
        self.slider_temp.setValue(22)
        self.dial_luz.setValue(50)
        self.chk_desayuno.setChecked(False)
        self.chk_spa.setChecked(False)
        self.barra_progreso.setValue(0)
        print("--- Formulario Limpiado ---")

    def confirmar_reserva(self):
        nombre = self.input_nombre.text()
        tipo = "VIP" if self.radio_vip.isChecked() else "Estándar"
        temp = self.slider_temp.value()
        
        print("\n" + "="*40)
        print("✅ NUEVA RESERVA CONFIRMADA")
        print("="*40)
        print(f"Huésped: {nombre} {self.input_apellido.text()}")
        print(f"Habitación: {tipo}")
        print(f"Ambiente: {temp}°C / {self.dial_luz.value()}% Luz")
        print("="*40 + "\n")
        
        QMessageBox.information(self, "Reserva", f"Reserva confirmada para {nombre}.\n¡Bienvenido!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga de estilos
    try:
        with open("estilos_hotel.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ Crea el archivo estilos_hotel.qss primero")

    ventana = HotelManager()
    ventana.show()
    sys.exit(app.exec())