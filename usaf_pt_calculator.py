import json

class PTTest:
	def __init__(self, age, gender, ac, pushups, situps, is_walk, run_time):
		"""Initialize the PTTest() object and calculate.

		Initializes the PTTest() object with the data given, reads the `usaf_pt_scores.json` file to find the score values,
		and caluclate the individual and total USAF PT Test score.

		Args:
			age (str): Age range of the test taker. Acceptable inputs: "<30", "30-39", "40-49", "50-59", ">=60"
			gender (str): Gender of test taker. Acceptable inputs: "male", "female"
			ac (float): Abdominal Circumference (AC) of test taker
			pushups (int): Push-up rep count for the test taker
			situps (int): Sit-up rep count for the test taker
			is_walk (bool): Boolean flag to determine if walk test (True), or run test (False)
		"""

		self.age = age
		self.gender = gender
		self.ac = ac
		self.ac_score = 0.0
		self.pushups = pushups
		self.pushups_score = 0.0
		self.situps = situps
		self.situps_score = 0.0
		self.is_walk = is_walk
		self.run_time = run_time
		self.run = self.run_to_sec(run_time)
		self.run_score = 0.0
		self.scores = self.read_scores()
		self.calculate()

	def read_scores(self):
		"""Reads `usaf_pt_scores.json` into a dict.

		Returns:
			dict: Dict containing the `usaf_pt_scores.json` values
		"""
		with open("usaf_pt_scores.json", "r") as f:
			return json.load(f)

	def run_to_sec(self, run_time):
		"""Convert string `run_time` into seconds.

		Convert string `run_time` into seconds (e.g. `run_time`="10:06" returns 606).

		Returns:
			int: Number of seconds from `run_time`
		"""
		s = run_time.split(":")
		mins = int(s[0])
		secs = int(s[1])
		return int((mins * 60) + secs)

	def calculate(self):
		"""Calculate the USAF PT Test results.

		Calculates the USAF PT Test results for the Abdominal Circumference (AC), Push-ups, Sit-ups,
		and Run/Walk components. Saves the test results to the `self.result` and `self.total_score`
		variables.

		"""

		# AC Score
		ac_measurements = [x["inches"] for x in self.scores["age"][self.age]["ac"][self.gender]]
		# Sort AC measurements by the inches values in the list of dicts
		ac_sorted = sorted(self.scores["age"][self.age]["ac"][self.gender], key=lambda x: float(x["inches"]))
		# Get the smallest AC measurement
		ac_smallest = min(ac_measurements)
		# If the AC input is smaller than the smallest AC measurement in the scores list, the test taker
		# automatically receives the highest score
		if self.ac <= ac_smallest:
			self.ac_score = 20.0
		else:
			# If the AC input is larger than the smallest AC measurement in the scores list, continue to
			# loop the sorted `ac_sorted` scores list until a match is found
			for s in ac_sorted:
				if self.ac == s["inches"]:
					self.ac_score = s["points"]
			# If a match is never found, the AC input will result in a failing score of 0.0, since the 
			# `self.ac_score` is initialized to 0.0 in `__init__`


		# Push-ups Score
		pushups_reps = [x["reps"] for x in self.scores["age"][self.age]["pushups"][self.gender]]
		# Sort Push-ups measurements by the rep values in the list of dicts
		pushups_sorted = sorted(self.scores["age"][self.age]["pushups"][self.gender], key=lambda x: int(x["reps"]))
		# Get the smallet Push-ups rep count
		pushups_smallest = min(pushups_reps)
		# Get the largest Push-ups rep count
		pushups_largest = max(pushups_reps)
		# If the Push-ups input is smaller than `pushups_smallest`, the test taker has failed and receives a 0.0
		# in this component
		if self.pushups <= pushups_smallest:
			self.pushups_score = 0.0
		# Otherwise, if the Push-ups input is larger than `pushups_largest`, than the test taker automatically
		# passes this component with a score of 10.0
		elif self.pushups >= pushups_largest:
			self.pushups_score = 10.0
		else:
			# If the Push-ups input is between the smallest and largest records rep counts, begin looping the 
			# sorted list
			for s in pushups_sorted:
				# Since the score list provided by the USAF isn't perfectly incremental, there are some gaps
				# in the rep counts. To avoid not finding a match, this assigns the `self.pushups_score` to
				# the current iteration's points value, if the rep counts are equal, or the input rep count
				# is larger
				if self.pushups >= s["reps"]:
					self.pushups_score = s["points"]

		# Sit-ups Score
		situps_reps = [x["reps"] for x in self.scores["age"][self.age]["situps"][self.gender]]
		# Sort Sit-ups measurements by the rep values in the list of dicts
		situps_sorted = sorted(self.scores["age"][self.age]["situps"][self.gender], key=lambda x: int(x["reps"]))
		# Get the smallet Sit-ups rep count
		situps_smallest = min(situps_reps)
		# Get the largest Sit-ups rep count
		situps_largest = max(situps_reps)
		# If the Sit-ups input is smaller than `situps_smallest`, the test taker has failed and receives a 0.0
		# in this component
		if self.situps <= situps_smallest:
			self.situps_score = 0.0
		# Otherwise, if the Sit-ups input is larger than `situps_largest`, than the test taker automatically
		# passes this component with a score of 10.0
		elif self.situps >= situps_largest:
			self.situps_score = 10.0
		else:
			# If the Sit-ups input is between the smallest and largest records rep counts, begin looping the 
			# sorted list
			for s in situps_sorted:
				# Since the score list provided by the USAF isn't perfectly incremental, there are some gaps
				# in the rep counts. To avoid not finding a match, this assigns the `self.situps_score` to
				# the current iteration's points value, if the rep counts are equal, or the input rep count
				# is larger
				if self.situps >= s["reps"]:
					self.situps_score = s["points"]

		# Run/Walk Score

		# Check the `self.is_walk` bool flag to see if the run component is either a run or walk test
		run_key = "run"
		if self.is_walk:
			run_key = "walk"
		# Initialize `highest_time` to 0, to record the highest `max_time` inside the loop
		highest_time = 0
		# Loop through the run scores list of dicts
		for s in self.scores["age"][self.age][run_key][self.gender]:
			min_time = s["min_time"]["seconds"]
			max_time = s["max_time"]["seconds"]
			# Record the highest possible `max_time` value to check for a failure below
			if max_time > highest_time:
				highest_time = max_time
			# If `self.run` is between or equal to either the minimum or maximum times given inside of the
			# current run score dict, record the points value and break the loop
			if min_time <= self.run <= max_time:
				self.run_score = s["points"]
				break

		# Check if `self.run` time is longer than the highest `max_time` found.
		if self.run > highest_time:
			self.run_score = 0.0

		# Combine all component scores together		
		self.total_score = self.ac_score + self.pushups_score + self.situps_score + self.run_score

		# Failure/Unsatisfactory score
		if 0.0 in [self.ac_score, self.pushups_score, self.situps_score, self.run_score] or self.total_score < 75:
			# One or more components failed, which means the test was a fail
			self.result = "Unsatisfactory"
		# Satisfactory score
		elif 75 <= self.total_score <= 89.9:
			self.result = "Satisfactory"
		# Excellent score
		elif self.total_score >= 89.9:
			self.result = "Excellent"

	def print_results(self):
		"""Print out the scores calculated in `self.calculate`"""
		result_text = "PASSED"
		if self.result == "Unsatisfactory":
			result_text = "FAILED"
		run_text = "Run"
		if self.is_walk:
			run_text = "Walk"
		text = """AC (in.): {ac} ({ac_score} pts)
Push-ups: {pushups} ({pushups_score} pts)
Sit-ups\t: {situps} ({situps_score} pts)
{run_text}\t: {run_time} ({run_score} pts)
---------------------------------------
{result_text}\t: {result} ({total_score} pts)""".format(ac=self.ac, ac_score=self.ac_score, pushups=self.pushups,
		pushups_score=self.pushups_score, situps=self.situps, situps_score=self.situps_score, run_text=run_text,
		run_time=self.run_time, run_score=self.run_score, result_text=result_text,
		result=self.result, total_score=self.total_score)
		print(text)
