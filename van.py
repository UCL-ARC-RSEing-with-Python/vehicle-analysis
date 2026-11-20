from dataclasses import dataclass
from datetime import datetime


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
