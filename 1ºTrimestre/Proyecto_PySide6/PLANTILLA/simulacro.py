import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLineEdit, QTextEdit, QComboBox, QRadioButton,
    QFormLayout, QVBoxLayout, QToolBar, QStatusBar,
    QMessageBox,QHBoxLayout

    # TODO: aÃ±adir aquÃ­ los widgets que necesites (QLineEdit, QTextEdit...)
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # TODO: tí­tulo y tamaÃ±o mÃ­nimo de la ventana
        self.setWindowTitle("Mini Bloc de Notas.")
        self.setMinimumSize(500, 400)

        # TODO: declarar atributos de widgets (title, categoria, prioridad, area de texto)
        # self.line_edit_titulo = None
        # ...

        self.line_edit_titulo = None
        self.combo_categoria = None
        self.radio_normal = None
        self.radio_alta = None
        self.texto_nota = None

        # TODO: declarar acciones (limpiar, imprimir, salir, acerca de)
        # self.accion_limpiar_nota = None
        # ...

        self.accion_limpiar = None
        self.accion_imprimir = None
        self.accion_salir = None
        self.accion_acerca_de = None

        # ConstrucciÃ³n general
        self.crear_central()       # TODO: completar
        self.crear_acciones()      # TODO: completar
        self.crear_menus()         # TODO: completar
        self.crear_toolbar()       # TODO: completar
        self.crear_statusbar()     # TODO: completar
        self.conectar_senales()    # TODO: completar

    # =========================
    # CREACIÃ“N DE LA ZONA CENTRAL
    # =========================
    def crear_central(self):
        widget_central = QWidget()

        self.line_edit_titulo = QLineEdit()
        self.line_edit_titulo.setPlaceholderText("Introduce el título de la nota...")
        self.line_edit_titulo.setMaxLength(100)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(['Trabajo','Ideas','Otros'])

        self.radio_normal = QRadioButton("Normal")
        self.radio_alta = QRadioButton("Alta")
        self.radio_normal.setChecked(True)

        self.texto_nota = QTextEdit()
        self.texto_nota.setPlaceholderText("Escribe el contenido de la nota...")

        # Layout formulario
        layout_form = QFormLayout()
        layout_form.addRow("Título:", self.line_edit_titulo)
        layout_form.addRow("Categoría:", self.combo_categoria)

        # 👉 Radiobuttons en la misma fila, uno a la izq y otro a la der
        layout_prioridad = QHBoxLayout()
        layout_prioridad.addWidget(self.radio_normal, alignment=Qt.AlignLeft)
        layout_prioridad.addWidget(self.radio_alta, alignment=Qt.AlignRight)
        layout_form.addRow("Prioridad:", layout_prioridad)

        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_form)
        layout_principal.addWidget(self.texto_nota)

        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    # =========================
    # ACCIONES, MENÚS Y TOOLBAR
    # =========================
    def crear_acciones(self):
        # TODO: crear acciones (QAction) con texto y atajos
        # self.accion_limpiar_nota = QAction("Limpiar nota", self)
        # self.accion_limpiar_nota.triggered.connect(...)

        self.accion_limpiar = QAction("Limpiar nota", self)
        self.accion_limpiar.setShortcut("Ctrl+L")

        self.accion_imprimir = QAction("Imprimir nota", self)
        self.accion_imprimir.setShortcut("Ctrl+P")

        self.accion_salir = QAction("Salir", self)
        self.accion_salir.setShortcut("Ctrl+Q")

        self.accion_acerca_de = QAction("Acerca de…", self)

    def crear_menus(self):
        # TODO: crear la barra de menÃºs y aÃ±adir los menÃºs Archivo y Ayuda
        # barra_menus = self.menuBar()
        # menu_archivo = barra_menus.addMenu("Archivo")
        # menu_archivo.addAction(...)

        barra = self.menuBar()

        menu_archivo = barra.addMenu("Archivo")
        menu_archivo.addAction(self.accion_limpiar)
        menu_archivo.addAction(self.accion_imprimir)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_ayuda = barra.addMenu("Ayuda")
        menu_ayuda.addAction(self.accion_acerca_de)

    def crear_toolbar(self):
        # TODO: crear barra de herramientas y aÃ±adir las acciones bÃ¡sicas
        # toolbar = QToolBar()
        # toolbar.addAction(...)
        
        toolbar = QToolBar("Barra de Herramientas")
        self.addToolBar(toolbar)

        toolbar.addAction(self.accion_limpiar)
        toolbar.addAction(self.accion_imprimir)

    def crear_statusbar(self):
        # TODO: crear barra de estado y mostrar un mensaje inicial
        # barra_estado = QStatusBar()
        # self.setStatusBar(barra_estado)
        
        barra_estado = QStatusBar()
        barra_estado.showMessage("Listo")
        self.setStatusBar(barra_estado)

    # =========================
    # SEÑALES
    # =========================
    def conectar_senales(self):
        # TODO conectar seÃ±ales como textChanged, currentTextChanged, toggled...
        self.line_edit_titulo.textChanged.connect(self.slot_titulo_cambiado)
        self.combo_categoria.currentTextChanged.connect(self.slot_categoria_cambiada)
        self.radio_normal.toggled.connect(self.slot_prioridad_cambiada)
        self.radio_alta.toggled.connect(self.slot_prioridad_cambiada)

        # Acciones
        self.accion_limpiar.triggered.connect(self.slot_limpiar_nota)
        self.accion_imprimir.triggered.connect(self.slot_imprimir_nota)
        self.accion_salir.triggered.connect(self.slot_salir)
        self.accion_acerca_de.triggered.connect(self.slot_acerca_de)

    # =========================
    # FUNCIONES DE UTILIDAD
    # =========================
    def obtener_prioridad_actual(self):
        # TODO devolver prioridad actual
        prioridad = ""
        if self.radio_alta.isChecked():
            prioridad = "Alta"
        else:
            prioridad = "Normal"
        return prioridad    # Ãºnico return

    def limpiar_contenido_nota(self):
        # TODO borrar tÃ­tulo, categorÃ­a, prioridad y contenido
        self.line_edit_titulo.clear()
        self.combo_categoria.setCurrentIndex(0)
        self.radio_normal.setChecked(True)
        self.texto_nota.clear()

    def imprimir_en_consola(self):
        # TODO imprimir la nota completa usando print con comas
        print("=========== NOTA ===========")
        print("Título:", self.line_edit_titulo.text())
        print("Categoría:", self.combo_categoria.currentText())
        print("Prioridad:", self.obtener_prioridad_actual())
        print("----------------------------")
        print("Contenido:")
        print(self.texto_nota.toPlainText())
        print("============================\n")

    # =========================
    # SLOTS (LOGICA)
    # =========================
    def slot_limpiar_nota(self):
        # TODO mostrar cuadro de confirmaciÃ³n y limpiar si aceptan
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Seguro que quieres limpiar la nota?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.limpiar_contenido_nota()
            self.statusBar().showMessage("Nota limpiada", 2000)

    def slot_imprimir_nota(self):
        # TODO llamar a imprimir_en_consola y mostrar mensaje
        self.imprimir_en_consola()
        self.statusBar().showMessage("Nota impresa en consola", 2000)

    def slot_salir(self):
        # TODO pedir confirmaciÃ³n antes de cerrar
        respuesta = QMessageBox.question(
            self, "Salir", "¿Deseas cerrar la aplicación?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def slot_acerca_de(self):
        # TODO mostrar QMessageBox.information
        QMessageBox.information(
            self,
            "Acerca de",
            "Mini Bloc de Notas\nEjemplo creado con PySide6."
        )

    def slot_titulo_cambiado(self, nuevo_titulo):
        self.setWindowTitle(f"Mini Bloc de Notas - {nuevo_titulo}")
        self.statusBar().showMessage("Título actualizado", 1500)

    def slot_categoria_cambiada(self, nueva_categoria):
        self.statusBar().showMessage(f"Categoría: {nueva_categoria}", 1500)

    def slot_prioridad_cambiada(self, checked):
        if checked:
            prioridad = self.obtener_prioridad_actual()
            self.statusBar().showMessage(f"Prioridad: {prioridad}", 1500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())