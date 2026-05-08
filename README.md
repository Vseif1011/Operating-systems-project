# CPU Scheduling Simulator (PyQt5)

A modern, dark-themed, and interactive CPU scheduling simulator useful for Operating Systems education and demonstration. It allows users to visualize and compare the scheduling of processes under three classic algorithms: Round Robin, FCFS (First-Come, First-Served), and non-preemptive SJF (Shortest Job First). Built using PyQt5, it features a professional UI, a main menu launcher, and clear, real-time visualizations of scheduling behavior for each algorithm.

## Features

- **Dark, modern UI** for all windows and dialogs
- **Main launcher menu** to select scheduling algorithms
- **Real-time simulation** with visual updates each second
- **Supports classic scheduling algorithms:**
  - **Round Robin** (user-defined quantum, cyclic queue rotation)
  - **First-Come, First-Served (FCFS)**
  - **Shortest Job First (SJF)** (non-preemptive, picks shortest burst in ready queue)
- **Easy process input** with Process ID and Burst Time
- **Summary/status display** for each simulation tick
- **Back button** for easy navigation

## Project Structure

```
project/
├── main.py
├── main_window.py
├── process.py
├── styles.py
├── ui.py
├── requirements.txt
├── algorithms/
│   ├── round_robin.py
│   ├── fcfs.py
│   ├── sjf.py
└── widgets/
    └── base_simulator.py
```

## How It Works

- **main.py:** Application entry point; starts the PyQt5 QApplication and opens the main window.
- **main_window.py:** Provides the main launcher menu where users select the scheduling algorithm.
- **widgets/base_simulator.py:** Abstract base for all simulators; manages layout, table, process input, control buttons, and ties to a simulation algorithm.
- **algorithms/*.py:** Each file implements the scheduling logic for one algorithm (`RoundRobinAlgorithm`, `FcfsAlgorithm`, `SjfAlgorithm`) and a corresponding simulator widget.
- **process.py:** Simple `Process` class used for process state.
- **styles.py:** Returns a dark theme stylesheet for a consistent, attractive look.
- **ui.py:** (For legacy/alternative simulation UI; main GUI uses main_window.py and base_simulator.py instead.)

## Usage

1. **Install requirements:**  
   Python 3.8+ and PyQt5 are required.  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install PyQt5
   ```

2. **Run the simulator:**  
   ```bash
   python main.py
   ```
   The main menu opens. Choose Round Robin, FCFS, or SJF to start a simulation.

3. **Simulate algorithms:**
   - Enter a Process ID (e.g., `P1`) and set its Burst Time.
   - (Round Robin only) Adjust the Time Quantum if needed.
   - Add multiple processes.
   - Click "Start Simulation" to watch the scheduler in action.

4. Use the **Back** button to return to the menu and switch algorithms.


## Notes

- Windows are maximized by default.
- All interactions are through a clear, modern interface.
- Code is cleanly separated by concerns (UI, algorithms, styling).

## Requirements

- Python 3.8+
- PyQt5

## License

_MIT or your custom license here._

---

Feel free to reference or modify this README as your project evolves!
