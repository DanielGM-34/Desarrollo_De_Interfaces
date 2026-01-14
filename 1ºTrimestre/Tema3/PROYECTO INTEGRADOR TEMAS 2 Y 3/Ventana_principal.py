from PySide6.QtWidgets import (
    QMainWindow, QWidget, QMenuBar, QMenu, QToolBar, QStatusBar, QLabel,
    QDockWidget, QComboBox, QCheckBox, QTextEdit,
    QFormLayout, QVBoxLayout, QHBoxLayout, QMessageBox,QSpinBox,QSlider,QPushButton
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

from componentes import CampoNombreAula, IndicadorEstadoAula, DialogoConfiguracionAvanzada

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aula inteligente - Panel de control")
        self.setMinimumSize(900, 600)
        self._crear_acciones()
        self._crear_menu()
        self._crear_toolbar()
        self._crear_statusbar()
        self._crear_dock()
        self._crear_area_central()
        self._conectar_signals_slots()
        self._restablecer_aula()

    # --- Acciones ---
    def _crear_acciones(self):
        self.act_restablecer = QAction(QIcon("restablecer_icono.png"), "Restablecer aula", self)
        self.act_salir = QAction("Salir", self)
        self.act_acerca_de = QAction("Acerca de...", self)
        self.act_config_avanzada = QAction("Configuración avanzada...", self)

    # --- Menús ---
    def _crear_menu(self):
        barra_menu = self.menuBar()
        menu_archivo = barra_menu.addMenu("Archivo")
        menu_archivo.addAction(self.act_restablecer)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.act_salir)

        menu_ayuda = barra_menu.addMenu("Ayuda")
        menu_ayuda.addAction(self.act_acerca_de)

        menu_config = barra_menu.addMenu("Configuración")
        menu_config.addAction(self.act_config_avanzada)

    # --- Toolbar ---
    def _crear_toolbar(self):
        toolbar = QToolBar("Herramientas", self)
        toolbar.addAction(self.act_restablecer)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    # --- Status bar ---
    def _crear_statusbar(self):
        status = QStatusBar(self)
        self.setStatusBar(status)
        self.lbl_estado_aula = QLabel("Estado: Preparando")
        self.statusBar().addPermanentWidget(self.lbl_estado_aula)

    # --- Dock ---
    def _crear_dock(self):
       self.dock = QDockWidget("Configuración rápida", self)
       self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
       contenedor = QWidget(self.dock)

    # Checkboxes existentes

       self.chk_iluminacion_dock = QCheckBox("Iluminación encendida", contenedor)
       self.chk_proyector_dock = QCheckBox("Proyector activo", contenedor)
       self.chk_clima_dock = QCheckBox("Climatización activa", contenedor)
        # --- NUEVOS CONTROLES ---

       self.slider_volumen = QSlider(Qt.Horizontal, contenedor)
       self.slider_volumen.setRange(0, 100)
       self.slider_volumen.setValue(50)
       self.spin_temperatura = QSpinBox(contenedor)
       self.spin_temperatura.setRange(16, 30)
       self.spin_temperatura.setValue(22)
       self.slider_brillo = QSlider(Qt.Horizontal, contenedor)
       self.slider_brillo.setRange(0, 100)
       self.slider_brillo.setValue(70)
       self.cmb_modo_rapido = QComboBox(contenedor)
       self.cmb_modo_rapido.addItems(["Clase normal", "Examen", "Presentación", "Charla"])
       self.btn_bloquear = QPushButton("Bloquear aula", contenedor)
       layout_dock = QVBoxLayout()
       layout_dock.addWidget(self.chk_iluminacion_dock)
       layout_dock.addWidget(self.chk_proyector_dock)
       layout_dock.addWidget(self.chk_clima_dock)
       layout_dock.addWidget(QLabel("Volumen audio:"))
       layout_dock.addWidget(self.slider_volumen)
       layout_dock.addWidget(QLabel("Temperatura:"))
       layout_dock.addWidget(self.spin_temperatura)
       layout_dock.addWidget(QLabel("Brillo proyector:"))
       layout_dock.addWidget(self.slider_brillo)
       layout_dock.addWidget(QLabel("Modo rápido:"))
       layout_dock.addWidget(self.cmb_modo_rapido)
       layout_dock.addWidget(self.btn_bloquear)
       layout_dock.addStretch()
       contenedor.setLayout(layout_dock)
       self.dock.setWidget(contenedor)
       self.addDockWidget(Qt.RightDockWidgetArea, self.dock)


    # --- Área central ---
    def _crear_area_central(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        self.cmb_modo = QComboBox(central)
        self.cmb_modo.addItems(["Clase normal", "Examen", "Presentación", "Charla"])

        self.chk_iluminacion = QCheckBox("Iluminación encendida", central)
        self.chk_proyector = QCheckBox("Proyector activo", central)
        self.chk_clima = QCheckBox("Climatización activa", central)

        self.campo_nombre = CampoNombreAula(central)
        self.campo_nombre.setPlaceholderText("Nombre del aula...")

        self.txt_observaciones = QTextEdit(central)
        self.txt_observaciones.setPlaceholderText("Observaciones o incidencias...")

        self.indicador = IndicadorEstadoAula(central)
        self.indicador.setMinimumSize(180, 180)

        form = QFormLayout()
        form.addRow("Modo:", self.cmb_modo)
        form.addRow("Nombre del aula:", self.campo_nombre)

        opciones_layout = QVBoxLayout()
        opciones_layout.addWidget(self.chk_iluminacion)
        opciones_layout.addWidget(self.chk_proyector)
        opciones_layout.addWidget(self.chk_clima)

        superior = QHBoxLayout()
        superior.addLayout(form, stretch=2)
        superior.addLayout(opciones_layout, stretch=1)
        superior.addWidget(self.indicador, stretch=0, alignment=Qt.AlignCenter)

        main_layout = QVBoxLayout(central)
        main_layout.addLayout(superior)
        main_layout.addWidget(self.txt_observaciones)
        central.setLayout(main_layout)

    # --- Conexiones ---
    def _conectar_signals_slots(self):
        self.act_restablecer.triggered.connect(self._restablecer_aula)
        self.act_salir.triggered.connect(self._confirmar_salir)
        self.act_acerca_de.triggered.connect(self._mostrar_acerca_de)
        self.act_config_avanzada.triggered.connect(self._abrir_config_avanzada)

        self.cmb_modo.currentIndexChanged.connect(self._actualizar_estado_general)
        self.chk_iluminacion.toggled.connect(self._actualizar_estado_general)
        self.chk_proyector.toggled.connect(self._actualizar_estado_general)
        self.chk_clima.toggled.connect(self._actualizar_estado_general)

        self.campo_nombre.validity_changed.connect(self._actualizar_estado_general)

        # --- NUEVO: sincronización Dock ↔ Central ---
        # Dock → Central
        self.chk_iluminacion_dock.toggled.connect(self.chk_iluminacion.setChecked)
        self.chk_proyector_dock.toggled.connect(self.chk_proyector.setChecked)
        self.chk_clima_dock.toggled.connect(self.chk_clima.setChecked)

        # Central → Dock
        self.chk_iluminacion.toggled.connect(self.chk_iluminacion_dock.setChecked)
        self.chk_proyector.toggled.connect(self.chk_proyector_dock.setChecked)
        self.chk_clima.toggled.connect(self.chk_clima_dock.setChecked)

        # Bloquear aula boton
        self.btn_bloquear.clicked.connect(self._bloquear_aula)


    # --- Slots ---
    def _restablecer_aula(self):
        self.cmb_modo.setCurrentIndex(0)
        self.chk_iluminacion.setChecked(True)
        self.chk_proyector.setChecked(False)
        self.chk_clima.setChecked(True)
        self.campo_nombre.clear()
        self.txt_observaciones.clear()

        # --- NUEVO: restablecer colores del círculo ---
        self.indicador._color_correcto = "#48C78E"
        self.indicador._color_preparando = "#FFDD57"
        self.indicador._color_incidencia = "#F14668"

        self._actualizar_estado_general()
        self.statusBar().showMessage("Aula restablecida", 2000)



    def _confirmar_salir(self):
        respuesta = QMessageBox.question(self, "Salir", "¿Seguro que deseas salir?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.close()

    def _mostrar_acerca_de(self):
        QMessageBox.information(self, "Acerca de",
                                "Aula inteligente\nProyecto educativo con PySide6.")

    def _abrir_config_avanzada(self):
        dlg = DialogoConfiguracionAvanzada(self)
        dlg.establecer_colores(self.indicador._color_correcto,
                               self.indicador._color_preparando,
                               self.indicador._color_incidencia)
        if dlg.exec() == dlg.DialogCode.Accepted:
            correcto, preparando, incidencia = dlg.obtener_colores()
            self.indicador._color_correcto = correcto
            self.indicador._color_preparando = preparando
            self.indicador._color_incidencia = incidencia
            self._actualizar_estado_general()


    def _bloquear_aula(self): QMessageBox.information( self, "Bloqueo de aula", "El aula ha sido bloqueada correctamente.\nAcceso restringido hasta nuevo aviso." )

    def _actualizar_estado_general(self):
        nombre_valido = self.campo_nombre.es_valido()
        servicios_activos = (self.chk_iluminacion.isChecked() or
                             self.chk_proyector.isChecked() or
                             self.chk_clima.isChecked())

        if not nombre_valido:
            estado = "Incidencia"
        elif servicios_activos:
            estado = "Correcto"
        else:
            estado = "Preparando"

        self.indicador.set_estado(estado)
        self.lbl_estado_aula.setText(f"Estado: {estado}")
        self.statusBar().showMessage(f"Aula en estado {estado}", 1500)
