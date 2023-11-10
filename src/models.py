from dataclasses import dataclass


@dataclass
class ScheduleEventRequest:
    name: str = ""
    description: str = ""
    day: str = ""
    start_time: str = ""
    start_minute: str = ""
    duration: str = ""