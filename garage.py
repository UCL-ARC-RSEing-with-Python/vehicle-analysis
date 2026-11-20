from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
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

    def fastest_vehicle(self) -> Vehicle:
        """Return the vehicle with the greatest top speed."""
        if not self.vehicles:
            raise ValueError("Garage does not store any vehicles!")

        return max(self.vehicles, key=lambda v: v.top_speed)

    def forecast_net_worth(
        self, date_range: list[datetime], save: Path | None = None
    ) -> plt.Figure:
        """Forecast net worth of all vehicles in the `Garage` over the given dates.

        Args:
            date_range:
                List of `datetime` objects, at which to forecast total worth of all vehicles.
            save:
                Path to save the generated figure to, if desired.

        Returns:
            plt.Figure:
                Forecast plot.
        """
        net_worth = [0.0 for _ in range(len(date_range))]
        for i, date in enumerate(date_range):
            for v in self.vehicles:
                net_worth[i] += v.value_on(date)

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(date_range, net_worth)
        ax.tick_params(axis="x", labelrotation=-75)
        ax.grid(visible=True)
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Price of all Vehicles (£k)")
        fig.tight_layout()

        if save is not None:
            fig.savefig(save)
        return fig

    def most_valuable_vehicle(self, on_date: datetime) -> Vehicle:
        """Return the most valuable vehicle by estimated cost, on the given date."""
        if not self.vehicles:
            raise ValueError("Garage does not store any vehicles!")

        return max(self.vehicles, key=lambda v: v.value_on(on_date))
