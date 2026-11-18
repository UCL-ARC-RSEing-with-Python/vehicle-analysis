# Car Dealership Analysis

This code-base is distributed by a vehicle manufacturer to its sales teams in their dealership outlets.
The code is designed to allow the sales teams to extract information such as the net worth of their vehicles, the forecasted degradation in value over time, and commonly-enquired about car properties like top speed and engine power.
However, in it's current state the code-base is little more than a single script, requiring a lot of implicit knowledge to fully understand.

## Vehicle Specifications

The company manufactures three types of vehicles; cars, vans, and HGVs (Heavy Goods Vehicles - think industrial lorries, trucks, and trains).
This information is then exported to `.csv` records, with the relevant records being passed to the sales team along with the physical shipment of the vehicle itself.
All vehicles that are manufactured come with the following information (the text in parenthesis denotes the CSV-column header the information appears under):

- The vehicle's license plate (`"Plate"`).
  This is a alphanumeric string; for road-vehicles this is typically 7 characters long, and for non-road vehicles typically 4 characters long.
  Lowercase letters are not used in these strings.
- Recommended Retail Price (RRP), in £1,000 (`"RRP"`).
  This is the price at which the manufacturer recommends the vehicle be sold at, when completely new.
- The date that assembly of the vehicle was completed (`"Manufacture Date"`).
  This is given as a date in `YYYY-MM-DD` format, though is string-valued inside the CSV file.
- The power that the vehicle's engine can generate (`"Engine Power"`), which in turn affects it's top speed and acceleration.
  This value is given in units of $\mathrm{kg} \ \mathrm{m}^2 \mathrm{s}^3$.
- The vehicle's Drag Coefficient (`"c_drag"`).
  This is a dimensionless number (a value that doesn't have any units) that appears in various mechanics-related calculations, broadly quantifying how much air resistance and other drag forces affect the vehicle.
  A higher value corresponds to a greater slowdown effect due to drag.
- The vehicle's front-facing cross section (`"Cross Section"`), given in $\mathrm{m}^2$.
  This is another parameter that affects how the vehicle interacts with resistance forces when moving, but is also helpful for determining whether a vehicle will fit on a driveway or under a narrow bridge!

Each sales team then has three files containing these records for all the cars, vans, and HGVs that they have possession of.
Note that the columns of the CSV file(s) are not guaranteed to be sorted into any particular order (but all headers will be present in the files).

## Vehicle Statistics
