from widgets.base_simulator import BaseSimulator


class SjfAlgorithm:
    def __init__(self):
        self.ready = []
        self.current_process = None
        self.current_time = 0

    def add_process(self, process):
        self.ready.append(process)

    def has_pending(self):
        return bool(self.current_process or self.ready)

    def tick(self, processes, quantum=None):
        if self.current_process is None:
            if not self.ready:
                return {
                    "finished": True,
                    "cpu_text": "CPU Status: Finished All Tasks",
                    "cpu_color": "#6A9955",
                    "time": self.current_time,
                }
            self.ready.sort(key=lambda p: (p.burst_time, p.pid))
            self.current_process = self.ready.pop(0)

        self.current_process.remaining_time -= 1
        self.current_time += 1

        cpu_text = f"CPU Status: Running Process '{self.current_process.pid}'"

        if self.current_process.remaining_time == 0:
            processes.remove(self.current_process)
            self.current_process = None

        return {
            "finished": False,
            "cpu_text": cpu_text,
            "cpu_color": "#569CD6",
            "time": self.current_time,
        }


class SjfSimulator(BaseSimulator):
    def __init__(self):
        super().__init__("SJF Scheduler", "SJF Simulator", needs_quantum=False)

    def create_algorithm(self):
        return SjfAlgorithm()
