import sys
# AQUI ESTABA EL ERROR: Faltaba QGridLayout en esta lista
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QComboBox, QSpinBox, QSlider, QDial, QLCDNumber,
    QButtonGroup, QScrollArea, QMessageBox, QSpacerItem, QSizePolicy, 
    QFormLayout, QGridLayout 
)
from PySide6.QtCore import Qt

class PizzeriaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bella Napoli - Sistema de Pedidos")
        self.resize(850, 700)

        # --- WIDGET CENTRAL CON SCROLL ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget_central = QWidget()
        scroll.setWidget(widget_central)
        self.setCentralWidget(scroll)

        # Layout Principal
        layout_principal = QHBoxLayout(widget_central)

        # =================================================================
        # COLUMNA IZQUIERDA: CONFIGURACIÓN DE LA PIZZA
        # =================================================================
        columna_izq = QVBoxLayout()

        # 1. GRUPO MASA Y TAMAÑO
        grupo_base = QGroupBox("1. La Base")
        layout_base = QFormLayout()

        # Combo para Masa
        self.combo_masa = QComboBox()
        self.combo_masa.addItems(["Fina y Crujiente", "Clásica Napolitana", "Bordes Rellenos de Queso (+2€)"])
        self.combo_masa.currentIndexChanged.connect(self.calcular_precio)

        # Radio Buttons para Tamaño
        self.grupo_tamano = QButtonGroup(self)
        layout_radios = QHBoxLayout()
        
        self.rad_peq = QRadioButton("Pequeña (8€)")
        self.rad_med = QRadioButton("Mediana (12€)")
        self.rad_fam = QRadioButton("Familiar (18€)")
        self.rad_med.setChecked(True)

        self.grupo_tamano.addButton(self.rad_peq, 8)
        self.grupo_tamano.addButton(self.rad_med, 12)
        self.grupo_tamano.addButton(self.rad_fam, 18)
        
        self.grupo_tamano.buttonClicked.connect(self.calcular_precio)

        layout_radios.addWidget(self.rad_peq)
        layout_radios.addWidget(self.rad_med)
        layout_radios.addWidget(self.rad_fam)

        layout_base.addRow("Tipo de Masa:", self.combo_masa)
        layout_base.addRow("Tamaño:", layout_radios)
        grupo_base.setLayout(layout_base)
        columna_izq.addWidget(grupo_base)

        # 2. GRUPO INGREDIENTES (Checkboxes en Cuadrícula)
        grupo_ing = QGroupBox("2. Ingredientes Extra (+1€ c/u)")
        
        # --- CORRECCIÓN AQUÍ: Usamos QGridLayout que ya está importado arriba ---
        layout_grid_ing = QGridLayout() 

        self.ingredientes = []
        nombres_ing = ["Pepperoni", "Champiñones", "Bacon", "Cebolla", "Extra Queso", "Aceitunas"]
        
        for i, nombre in enumerate(nombres_ing):
            chk = QCheckBox(nombre)
            chk.stateChanged.connect(self.calcular_precio)
            self.ingredientes.append(chk)
            # Fila i // 2, Columna i % 2 (Truco matemático: 0,0 | 0,1 | 1,0 | 1,1...)
            layout_grid_ing.addWidget(chk, i // 2, i % 2)

        grupo_ing.setLayout(layout_grid_ing)
        columna_izq.addWidget(grupo_ing)

        # 3. GRUPO NIVEL PICANTE
        grupo_picante = QGroupBox("3. Nivel de Picante 🌶️")
        layout_picante = QVBoxLayout()
        
        self.lbl_picante = QLabel("Nivel: 0 (Suave)")
        self.lbl_picante.setAlignment(Qt.AlignCenter)
        
        self.slider_picante = QSlider(Qt.Horizontal)
        self.slider_picante.setRange(0, 10)
        self.slider_picante.setTickPosition(QSlider.TicksBelow)
        self.slider_picante.setTickInterval(1)
        self.slider_picante.valueChanged.connect(self.actualizar_texto_picante)

        layout_picante.addWidget(self.lbl_picante)
        layout_picante.addWidget(self.slider_picante)
        grupo_picante.setLayout(layout_picante)
        columna_izq.addWidget(grupo_picante)

        layout_principal.addLayout(columna_izq, 2)

        # =================================================================
        # COLUMNA DERECHA: RESUMEN Y PAGO
        # =================================================================
        columna_der = QVBoxLayout()

        # 4. PROPINA (DIAL)
        grupo_propina = QGroupBox("Propina (%)")
        layout_dial = QVBoxLayout()
        
        self.dial_propina = QDial()
        self.dial_propina.setRange(0, 20)
        self.dial_propina.setNotchesVisible(True)
        self.dial_propina.setWrapping(False)
        self.dial_propina.valueChanged.connect(self.calcular_precio)
        
        self.lbl_propina_val = QLabel("0%")
        self.lbl_propina_val.setAlignment(Qt.AlignCenter)
        self.lbl_propina_val.setStyleSheet("font-size: 18px; color: #e65100; font-weight: bold;")

        layout_dial.addWidget(self.dial_propina)
        layout_dial.addWidget(self.lbl_propina_val)
        grupo_propina.setLayout(layout_dial)
        columna_der.addWidget(grupo_propina)

        # 5. CANTIDAD
        grupo_cant = QGroupBox("Cantidad")
        layout_cant = QVBoxLayout()
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 10)
        self.spin_cantidad.setSuffix(" uds")
        self.spin_cantidad.valueChanged.connect(self.calcular_precio)
        self.spin_cantidad.setStyleSheet("font-size: 16px;")
        layout_cant.addWidget(self.spin_cantidad)
        grupo_cant.setLayout(layout_cant)
        columna_der.addWidget(grupo_cant)

        # 6. TOTAL (LCD Number)
        grupo_total = QGroupBox("TOTAL A PAGAR")
        layout_total = QVBoxLayout()
        
        self.lcd_total = QLCDNumber()
        self.lcd_total.setDigitCount(6)
        self.lcd_total.setSmallDecimalPoint(True)
        self.lcd_total.display(0.0)
        self.lcd_total.setMinimumHeight(80)
        
        layout_total.addWidget(self.lcd_total)
        grupo_total.setLayout(layout_total)
        columna_der.addWidget(grupo_total)

        # 7. DATOS ENTREGA Y BOTONES
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección de entrega (Obligatorio)")
        self.input_direccion.textChanged.connect(self.validar_direccion)
        self.input_direccion.setProperty("obligatorio", "true")

        layout_botones = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("btnCancelar")
        self.btn_cancelar.clicked.connect(self.close)

        self.btn_pedir = QPushButton("PEDIR AHORA")
        self.btn_pedir.setObjectName("btnPedir")
        self.btn_pedir.setEnabled(False)
        self.btn_pedir.clicked.connect(self.enviar_pedido)

        layout_botones.addWidget(self.btn_cancelar)
        layout_botones.addWidget(self.btn_pedir)

        columna_der.addWidget(QLabel("Dirección:"))
        columna_der.addWidget(self.input_direccion)
        columna_der.addSpacing(20)
        columna_der.addLayout(layout_botones)
        columna_der.addStretch()

        layout_principal.addLayout(columna_der, 1)

        # Cálculo inicial
        self.calcular_precio()

    # ----------------------------------------------------------------------
    # LÓGICA
    # ----------------------------------------------------------------------

    def actualizar_texto_picante(self, valor):
        mensajes = ["Sin picante", "Suave", "Medio", "Picante", "Muy Picante", "INFIERNO 🔥"]
        indice = valor // 2 
        self.lbl_picante.setText(f"Nivel {valor}: {mensajes[indice]}")

    def validar_direccion(self, texto):
        if len(texto.strip()) > 5:
            self.btn_pedir.setEnabled(True)
            self.input_direccion.setProperty("obligatorio", "false")
        else:
            self.btn_pedir.setEnabled(False)
            self.input_direccion.setProperty("obligatorio", "true")
        
        self.input_direccion.style().unpolish(self.input_direccion)
        self.input_direccion.style().polish(self.input_direccion)

    def calcular_precio(self):
        precio = 0.0
        # Precio base según tamaño
        precio += self.grupo_tamano.checkedId()

        # Extra por masa rellena
        if "Rellenos" in self.combo_masa.currentText():
            precio += 2.0

        # Ingredientes extra
        extras = 0
        for chk in self.ingredientes:
            if chk.isChecked():
                extras += 1.0
        precio += extras

        # Cantidad
        cantidad = self.spin_cantidad.value()
        subtotal = precio * cantidad

        # Propina
        porcentaje_propina = self.dial_propina.value()
        self.lbl_propina_val.setText(f"{porcentaje_propina}%")
        
        total = subtotal * (1 + porcentaje_propina / 100)

        self.lcd_total.display(f"{total:.2f}")

    def enviar_pedido(self):
        total_pagar = self.lcd_total.value()
        direccion = self.input_direccion.text()
        
        print(f"--- PEDIDO ENVIADO ---")
        print(f"Dirección: {direccion}")
        print(f"Total: {total_pagar}€")
        
        QMessageBox.information(self, "¡Pizza en camino!", 
                                f"Tu pedido ha sido recibido.\nTotal: {total_pagar}€\nLlegará en 30 min.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilos_pizzeria.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ No encuentro 'estilos_pizzeria.qss'.")

    ventana = PizzeriaApp()
    ventana.show()
    sys.exit(app.exec())