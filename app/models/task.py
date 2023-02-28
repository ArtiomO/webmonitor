from dataclasses import dataclass


@dataclass
class TaskParameter:
    interval: int
    args: tuple
