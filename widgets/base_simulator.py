from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QSpinBox, QLineEdit,
    QMessageBox, QHeaderView, QFrame, QAbstractItemView
)

from styles import get_stylesheet
from process import Process


class BaseSimulator(QWidget):
    def __init__(self, window_title, header_title, needs_quantum=False):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setGeometry(200, 100, 900, 600)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)

        self.needs_quantum = needs_quantum
        self.processes = []
        self.algorithm = self.create_algorithm()
        self._on_close = None

        self.init_ui(header_title)
        self.apply_stylesheet()

        self.timer = QTimer()
        self.timer.timeout.connect(self.run_scheduler)

    def create_algorithm(self):
        raise NotImplementedError()

    def set_on_close(self, callback):
        self._on_close = callback

    def closeEvent(self, event):
        if self._on_close:
            self._on_close()
        event.accept()

    def init_ui(self, header_title):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(header_title)
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        back_button = QPushButton("Back")
        back_button.setObjectName("PrimaryBtn")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.go_back)

        header_layout.addWidget(title)
        header_layout.addStretch(1)
        header_layout.addWidget(back_button)

        main_layout.addLayout(header_layout)

        input_frame = QFrame()
        input_frame.setObjectName("Panel")
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(16, 16, 16, 16)
        input_layout.setSpacing(15)

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Process ID (e.g., P1)")

        self.burst_input = QSpinBox()
        self.burst_input.setRange(1, 100)
        self.burst_input.setValue(5)
        self.burst_input.setPrefix("Burst: ")

        input_layout.addWidget(self.pid_input)
        input_layout.addWidget(self.burst_input)

        self.quantum_input = None
        if self.needs_quantum:
            self.quantum_input = QSpinBox()
            self.quantum_input.setRange(1, 20)
            self.quantum_input.setValue(2)
            self.quantum_input.setPrefix("Quantum: ")
            input_layout.addWidget(self.quantum_input)

        add_button = QPushButton("Add Process")
        add_button.setObjectName("PrimaryBtn")
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.add_process)
        input_layout.addWidget(add_button)

        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Process ID", "Initial Burst", "Remaining Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        status_frame = QFrame()
        status_frame.setObjectName("Panel")
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(16, 16, 16, 16)

        self.cpu_label = QLabel("CPU Status: Idle")
        self.cpu_label.setObjectName("StatusLabel")
        self.time_label = QLabel("Current Time: 0s")
        self.time_label.setObjectName("StatusLabel")

        status_layout.addWidget(self.cpu_label)
        status_layout.addWidget(self.time_label)
        status_frame.setLayout(status_layout)

        control_frame = QFrame()
        control_frame.setObjectName("Panel")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(16, 16, 16, 16)
        control_layout.setSpacing(10)

        start_button = QPushButton("Start Simulation")
        start_button.setObjectName("PrimaryBtn")
        start_button.setCursor(Qt.PointingHandCursor)

        stop_button = QPushButton("Stop")
        stop_button.setObjectName("DangerBtn")
        stop_button.setCursor(Qt.PointingHandCursor)

        start_button.clicked.connect(self.start_simulation)
        stop_button.clicked.connect(self.stop_simulation)

        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)
        control_frame.setLayout(control_layout)

        bottom_layout.addWidget(status_frame, stretch=2)
        bottom_layout.addWidget(control_frame, stretch=1)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet())

    def add_process(self):
        pid = self.pid_input.text().strip()
        burst_time = self.burst_input.value()

        if pid == "":
            QMessageBox.warning(self, "Input Error", "Please enter a valid Process ID.")
            return

        process = Process(pid, burst_time)
        self.processes.append(process)
        self.algorithm.add_process(process)

        self.update_table()
        self.pid_input.clear()

    def update_table(self):
        self.table.setRowCount(len(self.processes))

        for row, process in enumerate(self.processes):
            pid_item = QTableWidgetItem(process.pid)
            burst_item = QTableWidgetItem(str(process.burst_time))
            rem_item = QTableWidgetItem(str(process.remaining_time))

            for item in (pid_item, burst_item, rem_item):
                item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, pid_item)
            self.table.setItem(row, 1, burst_item)
            self.table.setItem(row, 2, rem_item)

    def start_simulation(self):
        if not self.processes and not self.algorithm.has_pending():
            QMessageBox.information(self, "Notice", "No processes in the queue.")
            return
        self.timer.start(1000)

    def stop_simulation(self):
        self.timer.stop()
        self.cpu_label.setText("CPU Status: Paused")
        self.cpu_label.setStyleSheet("color: #DCDCAA;")

    def run_scheduler(self):
        quantum = self.quantum_input.value() if self.quantum_input else None
        info = self.algorithm.tick(self.processes, quantum)

        if info.get("finished"):
            self.cpu_label.setText(info.get("cpu_text", "CPU Status: Finished All Tasks"))
            self.cpu_label.setStyleSheet(f"color: {info.get('cpu_color', '#6A9955')};")
            self.timer.stop()
            self.update_table()
            return

        self.cpu_label.setText(info.get("cpu_text", "CPU Status: Running"))
        self.cpu_label.setStyleSheet(f"color: {info.get('cpu_color', '#569CD6')};")
        self.time_label.setText(f"Current Time: {info.get('time', 0)}s")
        self.update_table()

    def go_back(self):
        self.timer.stop()
        self.close()
