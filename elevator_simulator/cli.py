# elevator_simulator/cli.py
import argparse
from .elevator import Elevator
from .controller import ElevatorController
from .requests import ReqType

def run_demo():
    e = Elevator(id=1, min_floor=1, max_floor=10, door_time=2)
    c = ElevatorController(e)

    print("Initial status:", e.status())
    c.submit(5, ReqType.HALL_DOWN)
    for _ in range(3): c.tick()
    c.submit(3, ReqType.HALL_UP)
    for _ in range(2): c.tick()
    c.submit(8, ReqType.INTERNAL)
    total = c.run_until_idle(max_ticks=200)
    print(f"Ran {total} ticks; final status: {e.status()}")
    for line in e.log[-50:]:
        print(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="run a canned demo")
    args = parser.parse_args()
    if args.demo:
        run_demo()
    else:
        print("Try: python -m elevator_simulator.cli --demo")

if __name__ == "__main__":
    main()
