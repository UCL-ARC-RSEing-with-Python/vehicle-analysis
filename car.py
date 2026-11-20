from dataclasses import dataclass
from datetime import datetime


@dataclass
class Car:
    """Represents a single Car.

    Attributes:
        c_drag: Drag coefficient of the vehicle.
        manufacture_date: Date the vehicle was assembled.
        plate: Plate-identifier of the vehicle.
        power: Engine power in watts (kg m^-2 s^-3)
        rrp: Recommended retail price in £1000 when the vehicle is in mint condition.
        x_section: Front-facing cross-sectional area (m^2).
    """

    c_drag: float
    manufacture_date: datetime
    plate: str
    power: float
    rrp: float
    x_section: float
