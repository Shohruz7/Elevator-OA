Elevator Simulator — Bluestaq Take-Home Challenge (Back-End)


This project implements “The Elevator” back-end coding challenge in Python.
It simulates a single elevator system that processes floor requests, moves between floors, and models door operations over discrete time steps.

🧩 Overview

The simulator models:

Elevator state – current floor, direction, pending requests.

Request types – hall up/down calls and internal (inside elevator) requests.

Scheduler logic – continues moving in the current direction until all requests in that direction are served, then reverses if needed.

Door behavior – configurable open time per stop.



The design is modular and extensible for adding more elevators or advanced scheduling later.

🏗️ Project Structure
elevator_simulator/
├─ elevator_simulator/
│  ├─ __init__.py
│  ├─ requests.py        # Request dataclass + enums
│  ├─ elevator.py        # Elevator logic
│  ├─ controller.py      # ElevatorController (tick + request handling)
│  └─ cli.py             # Demo / CLI runner
├─ tests/
│  └─ test_elevator.py   # Basic pytest unit tests
├─ README.md
└─ requirements.txt

⚙️ Requirements
Python 3.9+
(Optional) pytest for running unit tests
