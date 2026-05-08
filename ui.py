import sys
from collections import deque

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QSpinBox,
    QLineEdit, QMessageBox, QHeaderView, QFrame, QAbstractItemView
)


class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time


class RoundRobinSimulator(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Round Robin Scheduler")
        self.setGeometry(200, 100, 900, 600)

        self.processes = []
        self.queue = deque()

        self.current_process = None
        self.time_quantum_counter = 0
        self.current_time = 0

        self.init_ui()
        self.apply_stylesheet()

        # Timer for real-time execution
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_scheduler)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # =====================================
        # Title
        # =====================================
        title = QLabel("Round Robin Simulator")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(title)

        # =====================================
        # Input Section
        # =====================================
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

        self.quantum_input = QSpinBox()
        self.quantum_input.setRange(1, 20)
        self.quantum_input.setValue(2)
        self.quantum_input.setPrefix("Quantum: ")

        add_button = QPushButton("Add Process")
        add_button.setObjectName("PrimaryBtn")
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.add_process)

        input_layout.addWidget(self.pid_input)
        input_layout.addWidget(self.burst_input)
        input_layout.addWidget(self.quantum_input)
        input_layout.addWidget(add_button)

        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame)

        # =====================================
        # Process Table
        # =====================================
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

        # =====================================
        # Status & Controls Section
        # =====================================
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Status Panel
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

        # Controls Panel
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
        # Professional Dark Theme CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
                font-size: 13px;
            }

            QLabel#Title {
                font-size: 22px;
                font-weight: 600;
                color: #ffffff;
            }

            QLabel#StatusLabel {
                font-size: 14px;
                font-family: 'Consolas', monospace;
                color: #4EC9B0; /* Sleek mint green for status */
            }

            QFrame#Panel {
                background-color: #252526;
                border: 1px solid #333333;
                border-radius: 6px;
            }

            QLineEdit, QSpinBox {
                background-color: #3c3c3c;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 10px;
                color: #ffffff;
            }

            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #007acc;
                background-color: #464646;
            }

            /* Buttons */
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 600;
            }

            QPushButton#PrimaryBtn {
                background-color: #0e639c;
                color: #ffffff;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #1177bb;
            }

            QPushButton#DangerBtn {
                background-color: #c53929;
                color: #ffffff;
            }
            QPushButton#DangerBtn:hover {
                background-color: #d84636;
            }

            /* Table Styling */
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #252526;
                border: 1px solid #333333;
                border-radius: 6px;
                outline: none;
            }

            QHeaderView::section {
                background-color: #2d2d30;
                color: #ffffff;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #333333;
                font-weight: 600;
                text-align: left;
            }

            QTableWidget::item {
                padding: 4px 8px;
                border-bottom: 1px solid #2d2d30;
            }
        """)

    def add_process(self):
        pid = self.pid_input.text().strip()
        burst_time = self.burst_input.value()

        if pid == "":
            QMessageBox.warning(self, "Input Error", "Please enter a valid Process ID.")
            return

        process = Process(pid, burst_time)
        self.processes.append(process)
        self.queue.append(process)

        self.update_table()
        self.pid_input.clear()

    def update_table(self):
        self.table.setRowCount(len(self.processes))

        for row, process in enumerate(self.processes):
            pid_item = QTableWidgetItem(process.pid)
            burst_item = QTableWidgetItem(str(process.burst_time))
            rem_item = QTableWidgetItem(str(process.remaining_time))

            # Optional: Center text in cells
            for item in (pid_item, burst_item, rem_item):
                item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, pid_item)
            self.table.setItem(row, 1, burst_item)
            self.table.setItem(row, 2, rem_item)

    def start_simulation(self):
        if not self.queue and self.current_process is None:
            QMessageBox.information(self, "Notice", "No processes in the queue.")
            return
        self.timer.start(1000)

    def stop_simulation(self):
        self.timer.stop()
        self.cpu_label.setText("CPU Status: Paused")
        self.cpu_label.setStyleSheet("color: #DCDCAA;") # Yellowish for paused

    def run_scheduler(self):
        # Pick next process
        if self.current_process is None:
            if not self.queue:
                self.cpu_label.setText("CPU Status: Finished All Tasks")
                self.cpu_label.setStyleSheet("color: #6A9955;") # Muted green
                self.timer.stop()
                return

            self.current_process = self.queue.popleft()
            self.time_quantum_counter = 0

        # Execute process
        self.current_process.remaining_time -= 1
        self.time_quantum_counter += 1
        self.current_time += 1

        self.cpu_label.setStyleSheet("color: #569CD6;") # Blue for running
        self.cpu_label.setText(f"CPU Status: Running Process '{self.current_process.pid}'")
        self.time_label.setText(f"Current Time: {self.current_time}s")

        # Process Finished
        if self.current_process.remaining_time == 0:
            finished_process = self.current_process
            self.processes.remove(finished_process)
            self.current_process = None

        # Quantum Expired
        elif self.time_quantum_counter == self.quantum_input.value():
            self.queue.append(self.current_process)
            self.current_process = None

        self.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundRobinSimulator()
    window.show()
    sys.exit(app.exec_())