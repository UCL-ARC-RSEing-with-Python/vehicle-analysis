from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

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

    vehicles = []
    for car in cars:
        veh_type = "car"
        car["plate"] = str(car["plate"]).upper()
        if not all(char.isalnum() for char in car["plate"]):
            raise ValueError(f"Plate is non-alphanumeric: {car['plate']}")
        if len(car["plate"]) != 7:
            raise ValueError(f"Car plate is not 7-digits long: {car['plate']}")
        x_section = car["Cross Section (m^2)"]
        if not (2.0 <= x_section <= 2.4):
            raise ValueError(
                f"X-section outside acceptable range (2.0 <= {x_section}! <= 2.4)"
            )
        vehicles.append({"type": "car", **car})
    for van in vans:
        veh_type = "van"
        van["plate"] = str(van["plate"]).upper()
        if not all(char.isalnum() for char in van["plate"]):
            raise ValueError(f"Plate is non-alphanumeric: {van['plate']}")
        if len(van["plate"]) != 7:
            raise ValueError(f"Van plate is not 7-digits long: {van['plate']}")
        x_section = van["Cross Section (m^2)"]
        if not (2.5 <= x_section <= 4.5):
            raise ValueError(
                f"X-section outside acceptable range (2.5 <= {x_section}! <= 4.0)"
            )
        vehicles.append({"type": "van", **van})
    for hgv in hgvs:
        veh_type = "hgv"
        hgv["plate"] = str(hgv["plate"]).upper()
        if not all(char.isalnum() for char in hgv["plate"]):
            raise ValueError(f"Plate is non-alphanumeric: {van['plate']}")
        if len(hgv["plate"]) != 4:
            raise ValueError(f"HGV plate is not 4-digits long: {van['plate']}")
        x_section = hgv["Cross Section (m^2)"]
        if not (9.0 <= x_section <= 10.0):
            raise ValueError(
                f"X-section outside acceptable range (9.0 <= {x_section}! <= 10.0)"
            )
        vehicles.append({"type": "hgv", **hgv})

    # Find the most valuable vehicle at a given point in time
    t = datetime.now()  # using today as an example, but could be any date

    # Optional: what would happen if there are no vehicles?
    mvv = vehicles[0]
    td: timedelta = t - mvv["Manufacture Date"]
    yrs = td.total_seconds() / (60 * 60 * 24 * 365)
    if mvv["type"] == "car":
        highest_p = mvv["RRP (£k)"] / (2**yrs)
    elif mvv["type"] == "van":
        highest_p = mvv["RRP (£k)"] / (1.6**yrs)
    else:
        highest_p = mvv["RRP (£k)"] / (1.0 + 2.0 * yrs**2)
    for v in vehicles:
        # Work out how much the vehicle has degraded in value since manufacture,
        # and then check if it's still worth more than the current most valuable
        # vehicle found
        td: timedelta = t - v["Manufacture Date"]
        yrs = td.total_seconds() / (60 * 60 * 24 * 365)

        if v["type"] == "car":
            p = v["RRP (£k)"] / (2**yrs)
        elif v["type"] == "van":
            p = v["RRP (£k)"] / (1.6**yrs)
        else:
            p = v["RRP (£k)"] / (1.0 + 2.0 ** (yrs**2))

        if p > highest_p:
            mmv = v
            highest_p = p

    print("Most valuable vehicle is currently", mmv, "at effective price", highest_p)

    # Find the vehicle with the highest theoretical top speed
    fastest = vehicles[0]
    density_of_air = 1.225  # kg m^-3
    highest_ts = (
        2.0
        * fastest["Engine Power (kg m^2 / s^3)"]
        / density_of_air
        / fastest["Drag Coefficient"]
        / fastest["Cross Section (m^2)"]
    )
    for v in vehicles:
        ts = (
            2.0
            * v["Engine Power (kg m^2 / s^3)"]
            / density_of_air
            / v["Drag Coefficient"]
            / v["Cross Section (m^2)"]
        )
        if ts > highest_ts:
            fastest = v
            highest_ts = ts

    print("Fastest vehicle is", fastest, "with top speed", highest_ts)

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
            td: timedelta = date - v["Manufacture Date"]
            yrs = td.total_seconds() / (60 * 60 * 24 * 365)
            if v["type"] == "car":
                total_price += v["RRP (£k)"] / (2**yrs)
            elif v["type"] == "van":
                total_price += v["RRP (£k)"] / (1.6**yrs)
            else:
                total_price += v["RRP (£k)"] / (1.0 + 2.0 ** (yrs**2))
        total_veh_values.append(total_price)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(forecast_dates, total_veh_values)
    ax.tick_params(axis="x", labelrotation=-75)
    ax.grid(visible=True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Price of all Vehicles (£k)")
    fig.tight_layout()
    fig.savefig("./price_forecast.png")
