import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PySide6.QtCore import Qt

# ----------------------------------------------------------------------
# CLASE PERSONALIZADA: VisorCoordenadas
# Hereda de QWidget porque vamos a pintar sobre él
# ----------------------------------------------------------------------
class VisorCoordenadas(QWidget):
    def __init__(self):
        super().__init__()
        # Fondo blanco para que se vea bien el dibujo
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        self.setMinimumSize(300, 300)

        # Variables de estado para guardar dónde se hizo clic
        # Iniciamos en -1 para indicar que aún no hay clic
        self.click_x = -1
        self.click_y = -1

    # --- 1. CAPTURA DE EVENTOS (El "Controlador") ---
    def mousePressEvent(self, event):
        """
        Este método salta automáticamente cuando el usuario hace clic.
        event.position().x() nos da la coordenada.
        """
        # Guardamos las coordenadas del clic en las variables de la clase
        self.click_x = int(event.position().x())
        self.click_y = int(event.position().y())

        # ¡IMPORTANTE! Llamamos a update() para forzar que se ejecute paintEvent de nuevo
        # Sin esto, el dibujo no se actualizaría hasta redimensionar la ventana.
        self.update()

    # --- 2. DIBUJO (La "Vista") ---
    def paintEvent(self, event):
        """
        Aquí ponemos toda la lógica de dibujo. Se borra y pinta de nuevo cada vez.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Para que las líneas no se vean pixeladas

        # Si aún no han hecho clic (x es -1), mostramos un mensaje de espera
        if self.click_x == -1:
            painter.setPen(Qt.gray)
            painter.drawText(self.rect(), Qt.AlignCenter, "Haz clic en cualquier lugar...")
            return

        # --- DIBUJAR LA DIANA ---
        # Configuramos un lápiz rojo y grueso
        pen = QPen(QColor("red"))
        pen.setWidth(2)
        painter.setPen(pen)

        # Dibujamos una cruz centrada en el punto del clic
        radio = 10
        # Línea horizontal
        painter.drawLine(self.click_x - radio, self.click_y, self.click_x + radio, self.click_y)
        # Línea vertical
        painter.drawLine(self.click_x, self.click_y - radio, self.click_x, self.click_y + radio)

        # --- DIBUJAR EL TEXTO ---
        # Configuramos un lápiz azul para el texto
        painter.setPen(QPen(QColor("blue")))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        
        texto = f"({self.click_x}, {self.click_y})"
        # Dibujamos el texto un poco desplazado para que no tape la cruz
        painter.drawText(self.click_x + 15, self.click_y - 15, texto)
        
        # Siempre finalizar el painter
        painter.end()

# ----------------------------------------------------------------------
# VENTANA PRINCIPAL
# ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Repaso Examen - Ejercicio Painter Eventos")

        self.visor = VisorCoordenadas()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Prueba de Widget Personalizado (Haz Clic):"))
        layout.addWidget(self.visor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # En este ejercicio NO usamos QSS externo, es lógica pura de Python
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())