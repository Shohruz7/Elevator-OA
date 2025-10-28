# tests/test_elevator.py
import pytest
from elevator_simulator.elevator import Elevator
from elevator_simulator.controller import ElevatorController
from elevator_simulator.requests import ReqType

def test_single_request_up():
    e = Elevator(id=1, min_floor=1, max_floor=5, door_time=1)
    c = ElevatorController(e)
    c.submit(3, ReqType.HALL_UP)
    c.run_until_idle(max_ticks=50)
    assert e.current_floor == 3

def test_requests_mixed():
    e = Elevator(id=1, min_floor=1, max_floor=5, door_time=1)
    c = ElevatorController(e)
    c.submit(5, ReqType.HALL_UP)
    c.tick()
    c.submit(2, ReqType.HALL_DOWN)
    c.run_until_idle(max_ticks=200)
    assert 1 <= e.current_floor <= 5
