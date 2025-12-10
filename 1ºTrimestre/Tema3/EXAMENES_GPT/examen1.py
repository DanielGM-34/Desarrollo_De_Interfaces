import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QFont

# CampoTexto
class CampoTexto(QLineEdit):
    texto_valido = Signal(str)
    texto_invalido = Signal(str)
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Escribe solo letras…")
        self.textChanged.connect(self._validar)
    def _validar(self, t):
        (self.texto_valido.emit(t) if t.isalpha() else self.texto_invalido.emit(t))

# BotonContador
class BotonContador(QPushButton):
    contador_actualizado = Signal(int)
    def __init__(self):
        super().__init__("Pulsado 0 veces")
        self._c = 0
        self.clicked.connect(self._inc)
    def _inc(self):
        self._c += 1
        self.setText(f"Pulsado {self._c} veces")
        self.contador_actualizado.emit(self._c)

# ContadorSimple
class ContadorSimple(QWidget):
    valor_cambiado = Signal(int)
    def __init__(self):
        super().__init__()
        self._v = 0
        self.lbl = QLabel("0"); self.lbl.setAlignment(Qt.AlignCenter)
        bmas = QPushButton("+"); bmenos = QPushButton("-")
        bmas.clicked.connect(self._inc); bmenos.clicked.connect(self._dec)
        h = QHBoxLayout(self); h.addWidget(bmenos); h.addWidget(self.lbl); h.addWidget(bmas)
    def _inc(self):
        self._v += 1; self.lbl.setText(str(self._v)); self.valor_cambiado.emit(self._v)
    def _dec(self):
        self._v -= 1; self.lbl.setText(str(self._v)); self.valor_cambiado.emit(self._v)

# IndicadorCircular
class IndicadorCircular(QWidget):
    def __init__(self, texto="READY"):
        super().__init__()
        self._t = texto
    def setTexto(self, t):
        self._t = t; self.update()
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        lado = min(self.width(), self.height())
        r = self.rect().adjusted(
            (self.width()-lado)//2, (self.height()-lado)//2,
            -(self.width()-lado)//2, -(self.height()-lado)//2
        )
        p.setBrush(QColor("red")); p.setPen(QPen(Qt.black, 2)); p.drawEllipse(r)
        p.setPen(QPen(Qt.white)); p.setFont(QFont("Segoe UI", 12)); p.drawText(r, Qt.AlignCenter, self._t)

# MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Examen práctico – Integrado")
        w = QWidget(); v = QVBoxLayout(w)

        # CampoTexto con labels
        campo = CampoTexto()
        lbl_ok = QLabel("Texto válido: "); lbl_ko = QLabel("Texto inválido: ")
        campo.texto_valido.connect(lambda t: lbl_ok.setText(f"Texto válido: {t}"))
        campo.texto_invalido.connect(lambda t: lbl_ko.setText(f"Texto inválido: {t}"))
        v.addWidget(campo); v.addWidget(lbl_ok); v.addWidget(lbl_ko)

        # BotonContador
        btnc = BotonContador()
        btnc.contador_actualizado.connect(lambda n: self.statusBar().showMessage(f"Contador: {n}"))
        v.addWidget(btnc)

        # ContadorSimple
        cont = ContadorSimple()
        cont.valor_cambiado.connect(lambda n: self.statusBar().showMessage(f"Valor contador simple: {n}"))
        v.addWidget(cont)

        # IndicadorCircular + botón
        indicador = IndicadorCircular("READY")
        cambiar = QPushButton("Cambiar a OK")
        cambiar.clicked.connect(lambda: indicador.setTexto("OK"))
        v.addWidget(indicador); v.addWidget(cambiar)

        self.setCentralWidget(w)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QWidget { background-color: #121212; color: #f0f0f0; font-family: "Segoe UI"; }
        QPushButton { background-color: #0055aa; color: white; border-radius: 6px; padding: 6px 12px; }
        QPushButton:hover { background-color: #1abc9c; }
        QLineEdit { background-color: #1e1e1e; color: white; border: 2px solid #e74c3c; border-radius: 8px; padding: 6px; }
        QLabel { color: #e0e0e0; }
        QStatusBar { background-color: #1f1f1f; color: #cccccc; }
    """)
    win = MainWindow()
    win.resize(500, 600)
    win.show()
    sys.exit(app.exec())
