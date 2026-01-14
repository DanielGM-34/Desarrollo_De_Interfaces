import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QComboBox, QFormLayout, QToolBar, QMessageBox, QSpinBox
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

class VentanaGestion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Incidencias v2.0 - Examen Completo")
        self.resize(500, 650)

        # --- 1. MENÚS Y BARRAS (Tema 2) ---
        self.crear_menus()
        
        # --- 2. WIDGET CENTRAL ---
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal vertical
        layout_principal = QVBoxLayout(widget_central)

        # === SECCIÓN 1: DATOS PERSONALES (Form Layout) ===
        grupo_datos = QGroupBox("1. Datos del Empleado")
        layout_datos = QFormLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre y Apellidos...")
        # Conectamos señal para validar en tiempo real
        self.input_nombre.textChanged.connect(self.validar_formulario)

        self.input_id = QSpinBox()
        self.input_id.setRange(1, 9999)
        self.input_id.setPrefix("ID-")

        self.combo_depto = QComboBox()
        self.combo_depto.addItems(["Informática", "RRHH", "Contabilidad", "Dirección"])

        layout_datos.addRow("Empleado:", self.input_nombre)
        layout_datos.addRow("Nº Identificación:", self.input_id)
        layout_datos.addRow("Departamento:", self.combo_depto)
        
        grupo_datos.setLayout(layout_datos)
        layout_principal.addWidget(grupo_datos)

        # === SECCIÓN 2: DETALLES (Radio Buttons y Checkbox) ===
        grupo_detalles = QGroupBox("2. Detalles de la Incidencia")
        layout_detalles = QVBoxLayout()

        layout_detalles.addWidget(QLabel("Nivel de Urgencia:"))
        
        # Layout horizontal para los radio buttons
        layout_radios = QHBoxLayout()
        self.radio_baja = QRadioButton("Baja")
        self.radio_media = QRadioButton("Media")
        self.radio_alta = QRadioButton("Alta")
        self.radio_media.setChecked(True) # Marcar uno por defecto

        layout_radios.addWidget(self.radio_baja)
        layout_radios.addWidget(self.radio_media)
        layout_radios.addWidget(self.radio_alta)
        
        layout_detalles.addLayout(layout_radios)
        
        # Checkboxes
        self.check_reinicio = QCheckBox("El equipo se reinicia solo")
        self.check_bloqueo = QCheckBox("Pantalla azul / Bloqueo")
        
        layout_detalles.addWidget(self.check_reinicio)
        layout_detalles.addWidget(self.check_bloqueo)
        
        grupo_detalles.setLayout(layout_detalles)
        layout_principal.addWidget(grupo_detalles)

        # === SECCIÓN 3: DESCRIPCIÓN (Bloc de Notas) ===
        grupo_desc = QGroupBox("3. Descripción del Problema")
        layout_desc = QVBoxLayout()
        
        self.texto_bloc = QTextEdit()
        self.texto_bloc.setPlaceholderText("Explique aquí qué ha pasado con todo detalle...")
        # Conectamos para validación
        self.texto_bloc.textChanged.connect(self.validar_formulario)
        
        layout_desc.addWidget(self.texto_bloc)
        grupo_desc.setLayout(layout_desc)
        layout_principal.addWidget(grupo_desc)

        # === SECCIÓN 4: BOTONES DE ACCIÓN ===
        layout_botones = QHBoxLayout()

        self.btn_borrar = QPushButton("Borrar Formulario")
        self.btn_borrar.setObjectName("btnBorrar") # ID para CSS Rojo
        self.btn_borrar.clicked.connect(self.accion_borrar)

        self.btn_enviar = QPushButton("ENVIAR INCIDENCIA")
        self.btn_enviar.setObjectName("btnEnviar") # ID para CSS Verde
        self.btn_enviar.setEnabled(False) # ¡EMPIEZA DESHABILITADO!
        self.btn_enviar.clicked.connect(self.accion_enviar)

        layout_botones.addWidget(self.btn_borrar)
        layout_botones.addWidget(self.btn_enviar)
        
        layout_principal.addStretch() # Empuja todo hacia arriba
        layout_principal.addLayout(layout_botones)

    def crear_menus(self):
        # Barra de Menú
        menu = self.menuBar()
        menu_archivo = menu.addMenu("&Archivo")
        
        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut("Ctrl+Q")
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)

        # Barra de Herramientas
        toolbar = QToolBar("Principal")
        self.addToolBar(toolbar)
        
        accion_limpiar = QAction("Limpiar Campos", self)
        accion_limpiar.triggered.connect(self.accion_borrar)
        toolbar.addAction(accion_limpiar)
        
        accion_ayuda = QAction("Ayuda", self)
        accion_ayuda.triggered.connect(lambda: print("Ayuda solicitada en terminal"))
        toolbar.addAction(accion_ayuda)

    # --- LÓGICA DEL EXAMEN ---

    def validar_formulario(self):
        """
        Se ejecuta cada vez que escribes en Nombre o en el Bloc de notas.
        Habilita el botón Enviar solo si hay texto en ambos.
        """
        nombre = self.input_nombre.text().strip()
        descripcion = self.texto_bloc.toPlainText().strip()

        # Validación Visual (Propiedad Dinámica para el CSS)
        if len(nombre) > 0:
            self.input_nombre.setProperty("valido", "true")
        else:
            self.input_nombre.setProperty("valido", "false")
        
        # Forzar recarga de estilo del input
        self.input_nombre.style().unpolish(self.input_nombre)
        self.input_nombre.style().polish(self.input_nombre)

        # Lógica del botón deshabilitado
        if len(nombre) > 0 and len(descripcion) > 0:
            self.btn_enviar.setEnabled(True)
            self.btn_enviar.setText("ENVIAR INCIDENCIA (LISTO)")
        else:
            self.btn_enviar.setEnabled(False)
            self.btn_enviar.setText("Rellene nombre y descripción...")

    def accion_borrar(self):
        """Limpia todo el formulario"""
        self.input_nombre.clear()
        self.input_id.setValue(1)
        self.combo_depto.setCurrentIndex(0)
        self.radio_media.setChecked(True)
        self.check_reinicio.setChecked(False)
        self.check_bloqueo.setChecked(False)
        self.texto_bloc.clear()
        print("--- FORMULARIO REINICIADO ---")

    def accion_enviar(self):
        """Simula el envío y saca info por terminal"""
        nombre = self.input_nombre.text()
        id_emp = self.input_id.text()
        depto = self.combo_depto.currentText()
        
        urgencia = "Desconocida"
        if self.radio_baja.isChecked(): urgencia = "Baja"
        elif self.radio_media.isChecked(): urgencia = "Media"
        elif self.radio_alta.isChecked(): urgencia = "Alta"

        desc = self.texto_bloc.toPlainText()

        print("\n" + "="*30)
        print("🚀 ENVIANDO INCIDENCIA AL SERVIDOR")
        print("="*30)
        print(f"👤 Usuario: {nombre} ({id_emp})")
        print(f"🏢 Depto: {depto}")
        print(f"🔥 Urgencia: {urgencia}")
        print(f"📝 Problema: {desc}")
        print("="*30 + "\n")
        
        QMessageBox.information(self, "Enviado", "La incidencia se ha registrado correctamente.")
        self.accion_borrar()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carga de estilos
    try:
        with open("estilos_completo.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("¡OJO! No se encuentra 'estilos_completo.qss'. Crea el archivo primero.")

    ventana = VentanaGestion()
    ventana.show()
    sys.exit(app.exec())