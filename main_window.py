from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame

from styles import get_stylesheet
from algorithms.round_robin import RoundRobinSimulator
from algorithms.fcfs import FcfsSimulator
from algorithms.sjf import SjfSimulator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduling Simulator")
        self.setGeometry(220, 120, 900, 600)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)
        self.active_simulator = None

        self.init_ui()
        self.apply_stylesheet()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        title = QLabel("CPU Scheduling Simulator")
        title.setObjectName("HeroTitle")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(title)

        panel = QFrame()
        panel.setObjectName("Panel")
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)
        panel_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        rr_button = QPushButton("Round Robin")
        rr_button.setObjectName("MenuBtn")
        rr_button.setCursor(Qt.PointingHandCursor)
        rr_button.clicked.connect(lambda: self.open_simulator(RoundRobinSimulator))
        rr_button.setFixedWidth(320)

        fcfs_button = QPushButton("FCFS")
        fcfs_button.setObjectName("MenuBtn")
        fcfs_button.setCursor(Qt.PointingHandCursor)
        fcfs_button.clicked.connect(lambda: self.open_simulator(FcfsSimulator))
        fcfs_button.setFixedWidth(320)

        sjf_button = QPushButton("Shortest Job First (SJF)")
        sjf_button.setObjectName("MenuBtn")
        sjf_button.setCursor(Qt.PointingHandCursor)
        sjf_button.clicked.connect(lambda: self.open_simulator(SjfSimulator))
        sjf_button.setFixedWidth(320)

        panel_layout.addWidget(rr_button)
        panel_layout.addWidget(fcfs_button)
        panel_layout.addWidget(sjf_button)
        panel.setLayout(panel_layout)
        panel.setMaximumWidth(380)

        main_layout.addStretch(1)
        main_layout.addWidget(panel, alignment=Qt.AlignHCenter)
        main_layout.addStretch(2)
        self.setLayout(main_layout)

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet())

    def open_simulator(self, simulator_class):
        self.active_simulator = simulator_class()
        self.active_simulator.set_on_close(self.show)
        self.active_simulator.show()
        self.hide()
