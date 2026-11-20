from datetime import datetime

from vehicle import Vehicle


class Car(Vehicle):
    @property
    def required_plate_length(self) -> int:
        return 7

    @property
    def cross_section_range(self) -> tuple[float, float]:
        return (2.0, 2.4)

    def value_on(self, date: datetime) -> float:
        """The estimated value of the vehicle on the given `date`."""
        yrs = self.years_since_manufacture(date)
        return self.rrp / (2.0**yrs)
