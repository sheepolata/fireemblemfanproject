import pygame
import math

class Character_sprite(pygame.sprite.Sprite):
	"""docstring for Character"""
	def __init__(self, animation_base, animation_select, animation_attack, w, h):
		pygame.sprite.Sprite.__init__(self)

		self.w, self.h = w, h

		self.animation_base = animation_base
		self.animation_select = animation_select
		self.play_attack = False
		self.animation_attack = animation_attack

		self.animation = self.animation_base
		self.image = self.animation[0]
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.rect = self.image.get_rect()

		self.anim_cpt = 0
		self.anim_att_cpt = 0


	def update(self):
		tresh = 35
		maxi = tresh * len(self.animation)
		if not self.play_attack:
			self.anim_cpt += 1

			index = int(math.ceil((float(self.anim_cpt) / float(maxi)) * len(self.animation))) - 1

			self.image = self.animation[index]
			self.image = pygame.transform.scale(self.image, (self.w, self.h))
			self.rect = self.image.get_rect()

			if self.anim_cpt >= maxi:
				self.anim_cpt = 0
		elif self.play_attack:
			self.anim_att_cpt += 1
			
			index = int(math.ceil((float(self.anim_att_cpt) / float(maxi)) * len(self.animation))) - 1

			self.image = self.animation[index]
			self.image = pygame.transform.scale(self.image, (self.w, self.h))
			self.rect = self.image.get_rect()

			if self.anim_att_cpt >= maxi:
				self.anim_att_cpt = 0
				self.animation = self.animation_base
				self.play_attack = False


		