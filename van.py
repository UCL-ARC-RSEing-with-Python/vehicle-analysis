from dataclasses import dataclass
from datetime import datetime

MS_TO_MPH = 2.23694
DENSITY_AIR = 1.225


@dataclass
class Van:
    """Represents a single Van.

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

    @property
    def top_speed(self) -> float:
        """Top speed of the vehicle in miles per hour (mph)."""
        return MS_TO_MPH * (
            2.0 * self.power / DENSITY_AIR / self.c_drag / self.x_section
        ) ** (1.0 / 3.0)

    def __post_init__(self) -> None:
        """Run validation checks on the information provided to the instance.

        - Plates are automatically converted to uppercase.
        - Plates are checked to only contain valid characters, and be of correct length.
        - Cross-sections are checked to be within reasonable guidelines.
        """
        self.plate = str(self.plate).upper()
        if not self.plate.isalnum():
            raise ValueError(f"Plate is non-alphanumeric: {self.plate}")
        if len(self.plate) != 7:
            raise ValueError(f"Van Plate is not 7-digits long: {self.plate}")

        if not (2.5 <= self.x_section <= 4.0):
            raise ValueError(
                f"X-section outside acceptable range (2.5 <= {self.x_section}! <= 4.0)"
            )

    def value_on(self, date: datetime) -> float:
        """The estimated value of the vehicle on the given `date`."""
        td = date - self.manufacture_date
        yrs = td.total_seconds() / (60 * 60 * 24 * 365)
        return self.rrp / (1.6**yrs)
