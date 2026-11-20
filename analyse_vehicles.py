from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from garage import Garage

DATA_DIR = Path(__file__).parent / "data"

if __name__ == "__main__":
    # Load the data about cars in the Garage...
    car_file = DATA_DIR / "cars.csv"
    van_file = DATA_DIR / "vans.csv"
    hgv_file = DATA_DIR / "hgvs.csv"

    garage = Garage(car_file=car_file, van_file=van_file, hgv_file=hgv_file)

    # Find the most valuable vehicle at a given point in time
    today = datetime.now()  # using today as an example, but could be any date
    most_valuable_vehicle = garage.most_valuable_vehicle(today)
    print(
        "Most valuable vehicle is currently",
        most_valuable_vehicle,
        "at effective price",
        most_valuable_vehicle.value_on(today),
    )

    # Find the vehicle with the highest theoretical top speed
    fastest_vehicle = garage.fastest_vehicle()
    print(
        "Fastest vehicle is",
        fastest_vehicle,
        "with top speed",
        fastest_vehicle.top_speed,
        "mph",
    )

    # Forecast the net worth of all vehicles over time
    forecast_until = datetime(year=2030, month=1, day=1)
    forecast_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    forecast_frequency = timedelta(days=30)
    n_dates = np.ceil((forecast_until - forecast_start) / forecast_frequency).astype(
        int
    )
    forecast_dates = [forecast_start + i * forecast_frequency for i in range(n_dates)]

    forecast_fig = garage.forecast_net_worth(
        forecast_dates, save="./price_forecast.png"
    )
    forecast_fig.show()
