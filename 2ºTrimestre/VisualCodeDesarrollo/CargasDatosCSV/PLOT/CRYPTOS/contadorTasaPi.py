from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsOpacityEffect
)
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QPixmap
import sys
import time

MINING_RATE_PER_HOUR = 0.0092
MINING_RATE_PER_SECOND = MINING_RATE_PER_HOUR / 3600


class MiningWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contador de Minado PI")
        self.total_mined = 0.0
        self.running = False
        self.last_time = time.time()
        self.next_pi_target = 1.0  # cuando llegue a 1π, luego 2π, 3π…

        # --- Widgets principales ---
        self.label = QLabel("Minado acumulado: 0.00000000 π", self)
        self.start_btn = QPushButton("Iniciar")
        self.stop_btn = QPushButton("Detener")

        # --- Imagen con animación ---
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("pi.png").scaled(200, 200, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.hide()

        # Efecto de opacidad para animación
        self.opacity_effect = QGraphicsOpacityEffect()
        self.image_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)

        # Eventos
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

    def start(self):
        if not self.running:
            self.running = True
            self.last_time = time.time()
            self.timer.start(200)

    def stop(self):
        self.running = False
        self.timer.stop()

    def update_counter(self):
        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now

        self.total_mined += MINING_RATE_PER_SECOND * elapsed
        self.label.setText(f"Minado acumulado: {self.total_mined:.8f} π")

        # Si alcanzamos 1π, 2π, 3π...
        if self.total_mined >= self.next_pi_target:
            self.show_pi_animation()
            self.next_pi_target += 1  # siguiente objetivo

    def show_pi_animation(self):
        self.image_label.show()

        # Fade-in
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(800)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.OutCubic)

        # Fade-out
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(800)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.setEasingCurve(QEasingCurve.InCubic)

        # Encadenar animaciones
        self.fade_in.finished.connect(self.fade_out.start)
        self.fade_out.finished.connect(self.image_label.hide)

        self.fade_in.start()


app = QApplication(sys.argv)
window = MiningWindow()
window.show()
sys.exit(app.exec())
