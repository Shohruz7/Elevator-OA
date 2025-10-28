# elevator_simulator/controller.py
from .elevator import Elevator
from .requests import Request, ReqType

class ElevatorController:
    def __init__(self, elevator:Elevator):
        self.elevator = elevator
        self.time = 0.0
        self.request_counter = 0

    def submit(self, floor:int, req_type:ReqType) -> Request:
        self.request_counter += 1
        req = Request(time=self.time, floor=floor, req_type=req_type, id=self.request_counter)
        self.elevator.add_request(floor, req_type)
        return req

    def tick(self) -> None:
        self.time += 1.0
        self.elevator.step()

    def run_until_idle(self, max_ticks:int = 500) -> int:
        ticks = 0
        while self.elevator.has_pending() and ticks < max_ticks:
            self.tick()
            ticks += 1
        return ticks
