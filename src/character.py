import settings as sett
import random

class Character():
	"""docstring for Character"""
	def __init__(self, name, sprite, x, y, selectable, team):
		self.name = name

		self.sprite = sprite

		self.x = x
		self.y = y

		self.selectable = selectable

		self.team = team

		self.mouvement = 3

		self.maxhitpoint = random.randint(5, 15)
		self.hitpoint = self.maxhitpoint
		
		self.attack = random.randint(3, 6)

		self.armor = random.randint(0, 3)

		sett.all_entities_list.append(self)
		sett.all_sprites_list.add(self.sprite)
		
	def kill(self):
		print(self.name + " is dead !")
		self.sprite.kill()

	def attackOther(self, otherEnt):
		dmg = max(self.attack - otherEnt.armor, 1)
		otherEnt.hitpoint -= dmg

		#Play attack animation
		self.sprite.animation = self.sprite.animation_attack
		self.sprite.play_attack = True

		print(self.name + " : Attack " + otherEnt.name + " for " + str(dmg) + " damage")

	def update(self):
		tw, th = int(float(sett.width)/float(sett.nb_tiles_w)), int(float(sett.height)/float(sett.nb_tiles_h))
		self.sprite.update()
		self.sprite.rect.x, self.sprite.rect.y = self.y * tw, self.x * th

	def is_dead(self):
		return self.hitpoint <= 0
