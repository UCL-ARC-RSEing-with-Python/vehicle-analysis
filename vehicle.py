from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

MS_TO_MPH = 2.23694
DENSITY_AIR = 1.225


@dataclass
class Vehicle(ABC):
    """Template for representing a single Vehicle.

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

    @property
    @abstractmethod
    def required_plate_length(self) -> int:
        """The length of the vehicle's plate."""
        ...

    @property
    @abstractmethod
    def cross_section_range(self) -> tuple[float, float]:
        """Acceptable range for the vehicle's cross section (low, high)."""
        ...

    def __post_init__(self) -> None:
        """Run validation checks on the information provided to the instance.

        - Plates are automatically converted to uppercase.
        - Plates are checked to only contain valid characters, and be of correct length.
        - Cross-sections are checked to be within reasonable guidelines.
        """
        self.plate = str(self.plate).upper()
        if not self.plate.isalnum():
            raise ValueError(f"Plate is non-alphanumeric: {self.plate}")
        if len(self.plate) != self.required_plate_length:
            raise ValueError(
                f"Plate is not {self.required_plate_length}-digits long: {self.plate}"
            )

        if not (
            self.cross_section_range[0] <= self.x_section <= self.cross_section_range[1]
        ):
            raise ValueError(
                "X-section outside acceptable range "
                f"({self.cross_section_range[0]} <= "
                f"{self.x_section}! <= "
                f"{self.cross_section_range[1]})"
            )

    @abstractmethod
    def value_on(self, date: datetime) -> float:
        """The estimated value of the vehicle on the given `date`."""
        ...

    def years_since_manufacture(self, date: datetime) -> float:
        """Number of years between the vehicle manufacture date and the given `date`."""
        return (date - self.manufacture_date).total_seconds() / (60 * 60 * 24 * 365)
