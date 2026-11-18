# FOOBAR FIXME

Overall plan is for us to encode our vehicles using a template pattern / method (<https://refactoring.guru/design-patterns/template-method>).
We're also going to make use of dataclasses

## Step 0: How is a single vehicle represented in the code?

Working with your group, identify how a single vehicle (be it a car, van, or HGV) is represented in the code-base.
What Python type is it represented by?
What attributes or values does this type contain?

Also identify the validation checks that are being run on the values read in from the data file, for each type of vehicle.

To help you later, you might also want to attempt to identify any calculations that take place within the code, that involve vehicle specification values.
Do these differ between vehicle types?
Or are they identical?
Is there a bit of both?

## Step 1: Representing each vehicle type as a `dataclass`

[Python's `dataclass`es](https://docs.python.org/3/library/dataclasses.html) are a convenient means of storing data that contains a lot of "derived" attributes or statistics.
They also come with a helpful amount of baked-in features; like automatic definition of an `__init__` method, customisable post-initialisation options via the special `__post_init__` method, and support for comparison and casting to other types like `tuple` and `dict`.

Within your group, split up into 3 sub-groups of 1 or 2 members.
Each group should work on it's own branch; and create a `dataclass` that can represent a single vehicle, however make sure that all three of your sub-groups coordinate on the names for your class' attributes and properties!
You might also want to give your class a suitable docstring that explains what the values stored in its attributes are.

Then;

- Have 1 sub-group implement the `Car` class inside a `car.py` file, which should be a `dataclass` that represents a single car.
- Have 1 sub-group implement the `Van` class inside a `van.py` file, which should be a `dataclass` that represents a single van.
- Have 1 sub-group implement the `HGV` class inside a `hgv.py` file, which should be a `dataclass` that represents a single HGV.

You should design these classes so that you can create them entirely from the information contained in a single row of the input `CSV` files.
An instance of each class should store [all the specifications](./README.md#vehicle-specifications) of the vehicle it represents.

## Step 2: Implement post-processing and validation

Still within your groups of 3, on your separate branches, implement the validation checks for your vehicle type inside the `__post_init__` method.

```python
@dataclass
class Car/Van/HGV:
  ...

  def __post_init__(self) -> None:
    # Run validation checks or post-input value processing here
```

You will need to examine the `analyse_vehicles.py` script to identify how the script is currently validating (the data provided for) the specifications of your vehicle type.
In particular;

- What happens to lowercase characters if they appear in the vehicle plate?
- Are there any restrictions placed on the plate lengths?
- Are there any other restrictions placed on the values provided to the other attributes?

## Step 3: Implement vehicle statistics

Still within your groups of 3, on your separate branches, add methods and properties to your `dataclass` that can be used to calculate [the vehicle statistics](./README.md).

- The `top_speed` should be implemented as a `property` of your class;

  ```python
  class Car/Van/HGV:
    ...

    @property
    def top_speed(self) -> float:
      # Calculate and return top speed
  ```

- The `current_value` of a vehicle will need to be a method on your class, that takes the date at which the valuation takes place as an input.
  
  ```python
  class Car/Van/HGV:
    ...

    def current_value(self, date_of_valuation: datetime) -> float:
      # Calculate the vehicle's current valuation.

## Step 4: Review your group-mates' work

Once all three sub-groups are ready, have everyone open a pull-request using their branch.
Either review each other's pull requests (subgroup A review subgroup B, B review C, and C review A for example) via GitHub, or discuss the changes in each PR in-person and take appropriate action.

Once you're happy, merge the pull-requests into your `main` branch.

## Step 5: Use your classes in the script

Now working together as one group again, create a new branch off `main` after merging your pull-requests [from the previous step](#step-4-review-your-group-mates-work).

Update the `analyse_vehicles.py` script so that it uses your `Car`, `Van`, and `HGV` classes, rather than the Python containers it's currently using.

How much code needs to change?
Is any code in the script now redundant because of what you've implemented in the classes?
Does the script read any better, and is it any easier to follow?

Once you have made the necessary changes, do a quick self-review of your work.
If you're happy, merge everything back into `main`!

> [!NOTE]
> The tasks can split into streams here.
> One stream can implement the template pattern on the various vehicle classes, whilst the other can work on refactoring the remaining code into the `Garage` class.

## Step 6A: Templating the vehicle classes

If you look at the `Car`, `Van`, and `HGV` classes you have created, you're probably going to spot that they all look very similar!

- Do they share any identical attributes?
- Do they share any properties or methods with identical "signatures" (same inputs, same name, and same output _type_)?

What you might realise is that we can adopt [a template design pattern](https://refactoring.guru/design-patterns/template-method) for our various vehicle classes.
This will make adding a new vehicle type in the future much easier, and will also ensure that any behaviour specific to each vehicle type is isolated to a single place, rather than spread out all over the code-base.

As such, create the `vehicle.py` file and the `Vehicle` class inside it.

```python
from abc import ABC, abstractmethod

@dataclass
class Vehicle(ABC):
  # The common attributes used to create each vehicle should go here!

  @property
  def top_speed(self) -> float:
    ... # can you implement this calculation?

  @abstractmethod
  def __post_init__(self) -> None:
    ...

  @abstractmethod
  def current_value(self, valuation_date: datetime) -> float:
    ...
```

`ABC` stands for "Abstract Base Class".
Making a class an `ABC` is like saying "instances of this class should never be created, but multiple objects in this code-base use the same interface as this class".
An ABC also allows us to "mark" certain methods or properties as `abstractmethod`s - these are methods that all subclasses are expected to provide, but _may be different in how they operate_ to each other.

In our case;

- `Vehicle` will be an `ABC`, because we are never going to have just a "vehicle".
  We always have either a `Car`, `Van`, or `HGV`.
- _But_ all three of `Car`, `Van`, and `HGV` share the same attributes, properties and methods - so they should use the `Vehicle` class as their template.
  As such, they should all be changed to be _subclasses_ of `Vehicle`.
  > [!NOTE]
  > `Vehicle` is already a `dataclass`, so you don't need to specify that `Car`, `Van`, and `HGV` are `dataclass`es any-more - they will also inherit this from `Vehicle`.
  > You might need to implement their `__post_init__` methods though!
- The `top_speed` is calculated in the same way for all three vehicle types.
  This means that we can implement it on the `Vehicle` class once, to save implementing it separately on the `Car`, `Van`, and `HGV` classes.
- The `current_value` method is subclass-specific.
  Although it takes the same inputs (and returns the same output type) for each vehicle type, the actual calculation is different.
  As such, it needs to be specified as an `abstractmethod` on the `Vehicle` class, but the implementation needs to be left blank (this is what the `...`s in the code sample above do).
  `current_valuation` then needs to be implemented on each of the specific classes.
- The `__post_init__` method might seem sub-class specific at first, and you could certainly implement it in this way.
  However, you could also implement `__post_init__` on the `Vehicle` class, and use abstract properties to fill in the blanks.
  Consider, for example, if you can make use of the following suggestion:

  ```python
  class Vehicle(ABC):

    @property
    @abstractmethod
    def required_plate_length(self) -> int:
      ...

    @property
    @abstractmethod
    def cross_section_range(self) -> tuple[float, float]:
      ...
    
    def __post_init__(self) -> None:
      self.plate = # does handling lowercase plate letters change between classes?
      if len(self.plate) != self.required_plate_length:
        # What do we do in this case?

      if not (self.cross_section_range[0] <= self.cross_section <= self.cross_section_range[1]):
        # What do we do here?
  ```

## Step 6B: Create the `Garage`

- Step 4: Implement a `Garage` class to help with loading the data.
  - `Garage` instance starts off without any cars in it
  - Has 3 methods for "adding" vehicles that are loaded from the csv files (`load_cars`, `load_vans`, etc). Note that this can actually be generalised to `load(veh_class, **info)`...
  - Provide methods for finding the fastest & most expensive cars, based on the script. (Again this can be generalised to `find_best_by_key(key="price")` etc)
  - Can add the `forecast_net_worth` function to the class too, refactor it to take the start date, end date, frequency, and whether or not to save! Return the figure created!
