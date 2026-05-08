# CPU Scheduling Simulator (PyQt5)

A polished, dark-themed CPU scheduling simulator for Operating Systems courses. It includes a main menu launcher and three real-time visual simulators: Round Robin, FCFS, and non-preemptive SJF. The UI matches a professional VSCode-inspired aesthetic and updates process execution using `QTimer`.

## Features

- Dark, modern UI with consistent styling across all windows
- Main menu launcher to choose the algorithm
- Real-time simulation with smooth table updates
- Algorithms included:
  - Round Robin (time quantum, queue rotation)
  - FCFS (first-come, first-served)
  - SJF (non-preemptive, shortest burst time)

## Project Structure

```
project/
├── main.py
├── main_window.py
├── styles.py
├── process.py
├── algorithms/
│   ├── round_robin.py
│   ├── fcfs.py
│   └── sjf.py
└── widgets/
    └── base_simulator.py
```

## Requirements

- Python 3.8+
- PyQt5

## Setup and Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install PyQt5
python main.py
```

## How It Works

- `MainWindow` provides the launcher UI and opens the chosen simulator.
- `BaseSimulator` holds the shared UI layout, table updates, and timer loop.
- Each algorithm module implements its own scheduling logic and plugs into `BaseSimulator`.
- `styles.py` ensures consistent UI styling across all windows.

## Notes

- The simulator windows default to maximized mode.
- Use the Back button to return to the main menu.
