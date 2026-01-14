import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QSlider, QColorDialog
)
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap, QAction
from PySide6.QtCore import Qt, QPoint

# ==============================================================================
# 1. WIDGET PIZARRA (La magia del Buffer)
# ==============================================================================
class PizarraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        
        # 1. Creamos el "papel" en blanco (Buffer)
        # Lo hacemos null al principio, lo inicializamos en el primer resize
        self.lienzo = None 
        
        # Variables de dibujo
        self.ultimo_punto = QPoint() # Para saber desde dónde tirar la línea
        self.color_pincel = Qt.black
        self.grosor_pincel = 3

    def set_color(self, color):
        self.color_pincel = color

    def set_grosor(self, grosor):
        self.grosor_pincel = grosor

    def limpiar(self):
        # Pintamos todo el lienzo de blanco
        self.lienzo.fill(Qt.white)
        self.update()

    # --- EVENTOS DE REDIMENSIONADO ---
    def resizeEvent(self, event):
        """Si cambian el tamaño de la ventana, creamos un lienzo nuevo"""
        if self.lienzo is None:
            # Creamos el mapa de píxeles del tamaño del widget
            self.lienzo = QPixmap(self.size())
            self.lienzo.fill(Qt.white) # Fondo blanco
        else:
            # Opción: Escalar el dibujo viejo al nuevo tamaño (o crear uno nuevo)
            # Aquí creamos uno nuevo y copiamos lo viejo para no perder el dibujo
            nuevo_lienzo = QPixmap(self.size())
            nuevo_lienzo.fill(Qt.white)
            
            painter = QPainter(nuevo_lienzo)
            painter.drawPixmap(0, 0, self.lienzo)
            painter.end()
            self.lienzo = nuevo_lienzo
            
        super().resizeEvent(event)

    # --- EVENTOS DEL RATÓN (Aquí se dibuja) ---
    
    def mousePressEvent(self, event):
        """Al hacer clic, guardamos dónde empezamos"""
        if event.button() == Qt.LeftButton:
            self.ultimo_punto = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Al arrastrar, pintamos una línea desde el último punto al actual"""
        # Solo si el botón izquierdo está apretado
        if event.buttons() & Qt.LeftButton:
            
            # 1. Configurar el pintor SOBRE EL LIENZO (no sobre el widget)
            painter = QPainter(self.lienzo)
            
            pincel = QPen(self.color_pincel, self.grosor_pincel, 
                          Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pincel)
            
            # 2. Dibujar línea
            punto_actual = event.position().toPoint()
            painter.drawLine(self.ultimo_punto, punto_actual)
            
            painter.end() # Importante cerrar el pintor
            
            # 3. Actualizar referencia y pedir repintado visual
            self.ultimo_punto = punto_actual
            self.update() # Llama a paintEvent para mostrar el cambio

    # --- EL EVENTO DE PINTURA (Solo muestra la imagen) ---
    def paintEvent(self, event):
        """Aquí solo volcamos el QPixmap en pantalla"""
        if self.lienzo:
            canvas_painter = QPainter(self)
            # Dibujamos la imagen completa (el buffer)
            canvas_painter.drawPixmap(0, 0, self.lienzo) 

# ==============================================================================
# 2. VENTANA PRINCIPAL
# ==============================================================================
class VentanaPaint(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulacro: Mini Paint")
        self.resize(600, 500)

        # Aplicamos un poco de estilo QSS a la ventana
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QPushButton { 
                background-color: #ddd; border: 1px solid #999; 
                padding: 5px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #ccc; }
            QLabel { font-family: sans-serif; font-size: 12px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 1. Pizarra
        self.pizarra = PizarraWidget()
        # Ponemos un borde con CSS al contenedor de la pizarra si queremos
        # Pero el widget pizarra ocupa todo
        
        # 2. Controles
        panel_control = QHBoxLayout()
        
        btn_limpiar = QPushButton("🗑️ Borrar Todo")
        btn_limpiar.clicked.connect(self.pizarra.limpiar)
        
        btn_color = QPushButton("🎨 Color")
        btn_color.clicked.connect(self.cambiar_color)
        
        slider_grosor = QSlider(Qt.Horizontal)
        slider_grosor.setRange(1, 20)
        slider_grosor.setValue(3)
        slider_grosor.valueChanged.connect(self.pizarra.set_grosor)
        
        panel_control.addWidget(btn_limpiar)
        panel_control.addWidget(btn_color)
        panel_control.addWidget(QLabel("Grosor:"))
        panel_control.addWidget(slider_grosor)

        layout.addWidget(self.pizarra, 1) # Expansión 1
        layout.addLayout(panel_control)

    def cambiar_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pizarra.set_color(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPaint()
    ventana.show()
    sys.exit(app.exec())