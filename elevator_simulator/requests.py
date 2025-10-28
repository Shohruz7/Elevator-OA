# elevator_simulator/requests.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

class ReqType(Enum):
    HALL_UP = auto()
    HALL_DOWN = auto()
    INTERNAL = auto()

@dataclass(order=True)
class Request:
    time: float
    floor: int = field(compare=False)
    req_type: ReqType = field(compare=False)
    id: int = field(default=0, compare=False)

    def __repr__(self) -> str:
        return f"Request(id={self.id}, floor={self.floor}, type={self.req_type.name}, t={self.time})"
