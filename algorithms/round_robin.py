from collections import deque

from widgets.base_simulator import BaseSimulator


class RoundRobinAlgorithm:
    def __init__(self):
        self.queue = deque()
        self.current_process = None
        self.time_quantum_counter = 0
        self.current_time = 0

    def add_process(self, process):
        self.queue.append(process)

    def has_pending(self):
        return bool(self.current_process or self.queue)

    def tick(self, processes, quantum):
        if self.current_process is None:
            if not self.queue:
                return {
                    "finished": True,
                    "cpu_text": "CPU Status: Finished All Tasks",
                    "cpu_color": "#6A9955",
                    "time": self.current_time,
                }
            self.current_process = self.queue.popleft()
            self.time_quantum_counter = 0

        self.current_process.remaining_time -= 1
        self.time_quantum_counter += 1
        self.current_time += 1

        cpu_text = f"CPU Status: Running Process '{self.current_process.pid}'"

        if self.current_process.remaining_time == 0:
            processes.remove(self.current_process)
            self.current_process = None
        elif self.time_quantum_counter == quantum:
            self.queue.append(self.current_process)
            self.current_process = None

        return {
            "finished": False,
            "cpu_text": cpu_text,
            "cpu_color": "#569CD6",
            "time": self.current_time,
        }


class RoundRobinSimulator(BaseSimulator):
    def __init__(self):
        super().__init__("Round Robin Scheduler", "Round Robin Simulator", needs_quantum=True)

    def create_algorithm(self):
        return RoundRobinAlgorithm()
