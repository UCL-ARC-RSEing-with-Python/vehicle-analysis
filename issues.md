# Refactoring and Templating: An Iterative Process

The overall plan of these tasks is to build up to describing "vehicles" using a template pattern / method (<https://refactoring.guru/design-patterns/template-method>), then write a suitable "collection" class for them which can operate on the template rather than needing to check the individual classes specifically.

This will be done as an iterative process, alongside some refactoring.
This hopefully makes the problem easy to motivate, and the `analyse_script.py` file is deliberately written verbosely to exaggerate this effect.
The idea is to replicate how these sorts of code improvements come about naturally in software projects; typically code is written to "get it working", and once you have a proof of concept or basic structure, improvements like this can be undertaken (preferably _before_ the code-base becomes too big)!
As such, the tasks broadly proceed in the following manner:

- Identify how a single vehicle is currently represented. Also identify why the different vehicle types - and treatment thereof - causes problems with the readability and structure of the current code.
- (In sub-groups) Create `dataclass`es to represent the three vehicle types.
- (In sub-groups) Implement the post-processing and validation checks on these classes.
- (In sub-groups) Have the `dataclass`es be able to compute the vehicle statistics using properties or methods.
- Combine everyone's work and review their PRs.
  The idea here is that they should see that each individual group has written essentially the same class, just with a few methods and numbers being different here-and-there!
- Use the classes that were created in the script.
  This should make the script quite a bit less verbose and a lot more readable, though there is still a ways to go.
- Template the three `Car`, `Van`, and `HGV` classes using a new `Vehicle` class.
  Getting them to do this "in reverse" will hopefully make the process of writing the abstract `Vehicle` class easier.
  And it's a bit more reflective of how this might come up naturally during a refactoring phase of development.
- Create the collection class, `Garage`, that stores multiple vehicles.
- Implement methods on the `Garage` class that can make use of the `Vehicle` template to conduct the required tasks.
  This removes the need for the "per-vehicle-type" logic in the `if` blocks, which also leads to much cleaner looking code.
  It will also hopefully inspire the students to identify further simplifications that can be made (finding "the best vehicle for X" will reduce to sorting the `Garage.vehicles` using the relevant method from the `Vehicle` class, for example).

It might be worth noting that our approach via classes for the objects might not always be the best approach for large, tabular datasets - there will be some aspects where the tabular structure of the data is a superior way to represent the information than having collections of individual objects.

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
      # Calculate and return top speed in mph
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

## Step 6: Templating the vehicle classes

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

## Step 7: Create the `Garage`

We also need to create a `Garage` class to help with loading and analysing the vehicle information.
The `Garage` class is used to describe a collection of vehicles, to complement the `Car`, `Van`, and `HGV` classes which describe a single vehicle (of the respective type).
Because we know that all our vehicle classes template the `Vehicle` class, we can write our `Garage` class assuming that all the objects we're storing are `Vehicle`s, and thus can use all of the methods, attributes, and properties defined on the `Vehicle` class in the `Garage` class methods (without worrying what the actual type of each particular vehicle is).

Create the `garage.py` file and the `Garage` class:

```python
from vehicle import Vehicle

class Garage:
    vehicles: list[Vehicle]

    def __init__(
      self,
      car_file: Path | None = None,
      van_file: Path | None = None,
      hgv_file: Path | None = None,
    ) -> None:
        ...
```

Write a suitable `__init__` method for the `Garage` class, which uses the above signature, and is inspired by the code in `analyse_vehicles.py`.
The `Garage.vehicles` attribute is intended to store the same information as the `vehicles` list in `analyse_vehicles.py`.

## Step 8: Refactor the script computations into `Garage` methods

`analyse_vehicles.py` is currently calculating three things from the vehicle list:

- The most valuable vehicle at a given point in time.
- The vehicle with the greatest top speed.
- The total net worth, forecast over time, of all the vehicles.

Working together or in small groups, design suitable methods for the `Garage` class to perform these calculations.
You may want to use the existing code in `analyse_vehicles.py` as inspiration to get started, but you might also find that there are more efficient ways to write these methods once you've worked on them for a bit.
Additionally, don't forget that we know everything in `Garage.vehicles` is going to be a `Vehicle`, which means you can make use of the attributes and methods which are attached to that class...

As you go, be sure to update the relevant parts of `analyse_vehicles.py` so that it uses the `Garage` class rather than it's current `vehicles` list.
Do you even need to import the other classes (`Car`, `Van`, `HGV`) into the script any more?

<details>
<summary>Some hints for `Garage` methods</summary>
Consider creating the following methods:

- `most_valuable_vehicle(self, at_date: datetime) -> Vehicle`
- `fastest_vehicle(self) -> Vehicle`
- `forecast_net_worth(self, date_range: list[datetime]) -> plt.Figure`

</details>

<details>
<summary>Hints for simplifications</summary>

Finding the fastest vehicle or the most valuable vehicle can be done by sorting all the `Garage.vehicles` into order by either their top speed or current price (respectively), and then taking the first entry.
Python's `sorted` function [just so happens to take a special `key` argument too](https://www.w3schools.com/python/ref_func_sorted.asp), which can be used to determine how sorting should take place... if only our vehicles came with something to help us compute their top speeds / current value.
</details>
