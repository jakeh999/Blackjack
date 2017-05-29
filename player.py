class Player:
	__score = None
	__name = None
	__is_robot = False

	def __init__(self, name, starter_score=500, is_robot=False):
		if not name:
			raise ValueError("Please enter a name.")
		else:
			self.__name = name
		if starter_score > 0:
			self.__score = starter_score
		else:
			raise ValueError("Please enter a starting score greater than 0!")
		self.__is_robot = is_robot

	def get_name(self):
		return self.__name

	def is_robot(self):
		return self.__is_robot

	def change_score(self, chips):
		if (self.__score + chips) < 0:
			raise ValueError("You don't have enough chips!")
		else:
			self.__score += chips

	def get_score(self):
		return self.__score
