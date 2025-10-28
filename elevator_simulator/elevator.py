# elevator_simulator/elevator.py
from enum import Enum
from typing import Optional, Set, Dict
from .requests import ReqType

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    def __init__(self, id:int=1, min_floor:int=1, max_floor:int=10, door_time:int=2):
        self.id = id
        self.current_floor = min_floor
        self.direction = Direction.IDLE
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.up_targets: Set[int] = set()
        self.down_targets: Set[int] = set()
        self.door_timer = 0
        self.door_time = door_time
        self.log = []

    def add_request(self, floor:int, req_type:ReqType):
        if floor < self.min_floor or floor > self.max_floor:
            raise ValueError("floor out of range")
        # Immediate stop if on same floor and idle
        if floor == self.current_floor and self.direction == Direction.IDLE and self.door_timer == 0:
            self.door_timer = self.door_time
            self.log.append(f"Immediate stop at floor {floor} for request {req_type.name}")
            return
        if floor > self.current_floor:
            self.up_targets.add(floor)
        elif floor < self.current_floor:
            self.down_targets.add(floor)
        else:
            # same floor but doors closed / moving -> treat as up target to be picked soon
            self.up_targets.add(floor)

    def has_pending(self) -> bool:
        return bool(self.up_targets or self.down_targets or self.door_timer > 0)

    def next_target(self) -> Optional[int]:
        if self.direction == Direction.UP or self.direction == Direction.IDLE:
            if self.up_targets:
                return min(self.up_targets)
            if self.down_targets:
                return max(self.down_targets)
        elif self.direction == Direction.DOWN:
            if self.down_targets:
                return max(self.down_targets)
            if self.up_targets:
                return min(self.up_targets)
        return None

    def open_doors_at_current(self):
        self.up_targets.discard(self.current_floor)
        self.down_targets.discard(self.current_floor)
        self.door_timer = self.door_time
        self.log.append(f"Stopping at floor {self.current_floor} and opening doors for {self.door_time} ticks")

    def step(self):
        # handle door timer first
        if self.door_timer > 0:
            self.door_timer -= 1
            self.log.append(f"Doors open at floor {self.current_floor} ({self.door_timer} ticks left)")
            return

        target = self.next_target()
        if target is None:
            self.direction = Direction.IDLE
            self.log.append("Idle")
            return

        if target == self.current_floor:
            self.open_doors_at_current()
            return

        if self.direction == Direction.IDLE:
            self.direction = Direction.UP if target > self.current_floor else Direction.DOWN

        if self.direction == Direction.UP:
            self.current_floor += 1
            self.log.append(f"Moving up -> floor {self.current_floor}")
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1
            self.log.append(f"Moving down -> floor {self.current_floor}")

        if self.current_floor in self.up_targets or self.current_floor in self.down_targets:
            self.open_doors_at_current()

        # optional direction adjustment for next ticks:
        if self.direction == Direction.UP and not any(t > self.current_floor for t in self.up_targets):
            if self.down_targets:
                self.direction = Direction.DOWN
        if self.direction == Direction.DOWN and not any(t < self.current_floor for t in self.down_targets):
            if self.up_targets:
                self.direction = Direction.UP

    def status(self) -> Dict:
        return {
            "id": self.id,
            "floor": self.current_floor,
            "dir": self.direction.name,
            "up_targets": sorted(self.up_targets),
            "down_targets": sorted(self.down_targets, reverse=True),
            "door_timer": self.door_timer
        }
