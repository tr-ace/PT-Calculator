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