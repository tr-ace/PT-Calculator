# PT-Calculator
**PT-Calculator** is a Python module that allows for individuals to quickly calculate their United States Air Force (USAF) Physical Training (PT) test. The **PTTest** class accepts inputs for each component of the test. Then, during the class initialization, the score is calculated automatically. You can then view the results with `PTTest.print_results()` and/or the `PTTest.total_score` variable.

## Usage
The `PTTest.calculate()` function handles all of the scoring calculations by comparing the input values to the scores saved in the `usaf_pt_scores.json` file. This file contains United States Air Force (USAF) Physical Training (PT) test scores for males and females, spanning all 5 age groups for both genders.

```python
from usaf_pt_calculator import PTTest
```

### Reading the scores
If you would like to use the United States Air Force (USAF) Physical Training (PT) test scores JSON file for your own project, it can easily be parsed. The structure is as follows:
`"age"` -> `AGE_GROUP` -> `TEST_COMPONENT` -> `GENDER`
This will return a list of component scores for the respective age group, test component, and gender. Take a look at the `PTTest.calculate()` function to see how these are used to calculate the score. A live example can be found at [airforcecalculator.com](https://airforcecalculator.com) where I ported the Python code to JavaScript, and added some additional features.


## Examples

### Calculate a score
Using any method on collecting the individual component inputs, you can calculate the final score with ease by initializing the `PTTest` class with the values in order of:

Variable | Type | Description
--- | --- | ---
`age` | `str` | The age group for the test taker. (`<30`, `30-39`, `40-49`, `50-59`, `>=60`)
`gender` | `str` | The gender of the test taker. (`male`, `female`)
`ac` | `float` | The abdominal circumference (AC) of the test taker.
`pushups` | `int` | The number of push-up reps the test taker accomplished.
`situps` | `int` | The number of sit-up reps the test taker accomplished.
`is_walk` | `bool` | Whether the test taker performed a walk test, or run test. (`True` for walk, `False` for run)
`run_time` | `str` | The run/walk test time accomplished by the test taker. (`XX:XX`)

```python
from usaf_pt_calculator import PTTest

age = "<30"
gender = "male"
ac = 32.5
pushups = 55
situps = 45
is_walk = False
run_time = "9:39"

pt_test = PTTest(age, gender, ac, pushups, situps, is_walk, run_time)

pt_test.print_results()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer
PT-Calculator and AirForceCalculator.com are not affiliated with the United States Air Force or any component of the United States Department of Defense. All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them.

