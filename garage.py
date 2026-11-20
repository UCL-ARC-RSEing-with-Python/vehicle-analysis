from pathlib import Path

import pandas as pd

from car import Car
from hgv import HGV
from van import Van
from vehicle import Vehicle


class Garage:
    """Stores a collection of `Vehicle`s for analysis."""

    vehicles: list[Vehicle]

    def __init__(
        self,
        car_file: Path | None = None,
        van_file: Path | None = None,
        hgv_file: Path | None = None,
    ) -> None:
        """Create a `Garage` from a collection of files.

        Args:
            car_file: Path | None
                Cars to be loaded.
            van_file: Path | None
                Vans to be loaded.
            hgv_file: Path | None
                HGVs to be loaded.
        """

        self.vehicles = []

        for file, cls in zip([car_file, van_file, hgv_file], [Car, Van, HGV]):
            vehs = pd.read_csv(file, parse_dates=["Manufacture Date"]).to_dict(
                orient="records"
            )
            for v in vehs:
                self.vehicles.append(
                    cls(
                        c_drag=v["Drag Coefficient"],
                        manufacture_date=v["Manufacture Date"],
                        plate=v["Plate"],
                        power=v["Engine Power"],
                        rrp=v["RRP"],
                        x_section=v["Cross Section"],
                    )
                )
