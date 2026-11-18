Overall plan is for us to encode our vehicles using a template pattern / method.
We're also going to make use of dataclasses

- Step 1: create simple dataclasses to represent cars, vans, and hgvs. (They will look similar!)
  - Post-init for X-section range validation
  - `value_at_time` method
  - `top_speed` property
  - other derived things...
  - use sensible attribute names, and make sure to document them!!!
- Step 2: rework the script to make use of the new classes!
  - Loading no longer needs the vehicle type to be specified
  - Highest price avoids the `if type[...]` blocks
  - Both methods can avoid doing the calculation explicitly, can just use the created property / method
  - Can even now use `sorted` with a suitable `key` argument if you want to be fancy!
- Step 3: Implement a base class for the template method, `Vehicle`.
  - cars, vans, and hgvs are all created in the same way, they just have different ranges for the X-section and different degradation formulae
  - use properties for the values that will change on a per-subclass basis
  - use ABC to flag the methods & properties that need to be filled in!
  - `__post_init__` can be implemented on the base class using the abstract properties...
  - `top_speed` can be directly implemented on the base class as a property
  - `value_at_time` will need to be an abstract method since it varies for each vehicle type.
- Step 4: Implement a `Garage` class to help with loading the data.
  - `Garage` instance starts off without any cars in it
  - Has 3 methods for "adding" vehicles that are loaded from the csv files (`load_cars`, `load_vans`, etc). Note that this can actually be generalised to `load(veh_class, **info)`...
  - Provide methods for finding the fastest & most expensive cars, based on the script. (Again this can be generalised to `find_best_by_key(key="price")` etc)
  - Can add the `forecast_net_worth` function to the class too, refactor it to take the start date, end date, frequency, and whether or not to save! Return the figure created!
