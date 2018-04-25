import random

class TileLogic():
	"""Logic for a Tile"""
	def __init__(self, logic_pos):
		self.logic_pos = logic_pos
		
		self.is_selected = False
		self.is_cursor = False

		#Astar tests
		self.is_path_test = False
		self.is_visited = False
		self.iteration_visit = 0
		self.path_color_test = (0, 0, 0)


		self.is_free = True
		self.cost = 1

		self.in_range = False
		self.in_range_but_busy = False
		self.is_entity = False
		self.entity = None