
class TileLogic():
	"""Logic for a Tile"""
	def __init__(self, logic_pos):
		self.logic_pos = logic_pos
		self.is_selected = False
		self.is_cursor = False