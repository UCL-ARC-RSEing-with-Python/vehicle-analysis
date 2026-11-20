from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from car import Car
from hgv import HGV
from van import Van

DATA_DIR = Path(__file__).parent / "data"
MS_TO_MPH = 2.23694

if __name__ == "__main__":
    # Load the data about cars in the Garage...
    car_file = DATA_DIR / "cars.csv"
    van_file = DATA_DIR / "vans.csv"
    hgv_file = DATA_DIR / "hgvs.csv"

    cars = pd.read_csv(car_file, parse_dates=["Manufacture Date"]).to_dict(
        orient="records"
    )
    vans = pd.read_csv(van_file, parse_dates=["Manufacture Date"]).to_dict(
        orient="records"
    )
    hgvs = pd.read_csv(hgv_file, parse_dates=["Manufacture Date"]).to_dict(
        orient="records"
    )

    vehicles: list[Car | Van | HGV] = []
    for car in cars:
        vehicles.append(
            Car(
                c_drag=car["Drag Coefficient"],
                manufacture_date=car["Manufacture Date"],
                plate=car["Plate"],
                power=car["Engine Power"],
                rrp=car["RRP"],
                x_section=car["Cross Section"],
            )
        )
    for van in vans:
        vehicles.append(
            Van(
                c_drag=van["Drag Coefficient"],
                manufacture_date=van["Manufacture Date"],
                plate=van["Plate"],
                power=van["Engine Power"],
                rrp=van["RRP"],
                x_section=van["Cross Section"],
            )
        )
    for hgv in hgvs:
        vehicles.append(
            HGV(
                c_drag=hgv["Drag Coefficient"],
                manufacture_date=hgv["Manufacture Date"],
                plate=hgv["Plate"],
                power=hgv["Engine Power"],
                rrp=hgv["RRP"],
                x_section=hgv["Cross Section"],
            )
        )

    # Find the most valuable vehicle at a given point in time
    t = datetime.now()  # using today as an example, but could be any date

    # Optional: what would happen if there are no vehicles?
    mvv = vehicles[0]
    highest_p = mvv.value_on(t)
    for v in vehicles:
        # Work out how much the vehicle has degraded in value since manufacture,
        # and then check if it's still worth more than the current most valuable
        # vehicle found
        p = v.value_on(t)
        if p > highest_p:
            mmv = v
            highest_p = p

    print("Most valuable vehicle is currently", mmv, "at effective price", highest_p)

    # Find the vehicle with the highest theoretical top speed
    fastest = vehicles[0]
    highest_ts = fastest.top_speed
    for v in vehicles:
        ts = v.top_speed
        if ts > highest_ts:
            fastest = v
            highest_ts = ts

    print("Fastest vehicle is", fastest, "with top speed", highest_ts, "mph")

    # Forecast the net worth of all vehicles over time
    forecast_until = datetime(year=2030, month=1, day=1)
    forecast_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    forecast_frequency = timedelta(days=30)
    n_dates = np.ceil((forecast_until - forecast_start) / forecast_frequency).astype(
        int
    )
    forecast_dates = [forecast_start + i * forecast_frequency for i in range(n_dates)]

    total_veh_values = []
    for date in forecast_dates:
        total_price = 0.0
        for v in vehicles:
            total_price += v.value_on(date)
        total_veh_values.append(total_price)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(forecast_dates, total_veh_values)
    ax.tick_params(axis="x", labelrotation=-75)
    ax.grid(visible=True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Price of all Vehicles (£k)")
    fig.tight_layout()
    fig.savefig("./price_forecast.png")
