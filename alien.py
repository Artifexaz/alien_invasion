import pygame as pg
from pygame.sprite import Sprite
#import random
#import numpy as np

class Alien(Sprite):
	"""表示单个外星人的类"""
	
	def __init__(self, ai_settings, screen):
		"""初始化外星人的位置"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# 加载外星人图像，并设置其rect属性
		self.image = pg.image.load('image/alien_yellow.png')
		self.rect = self.image.get_rect()
		
		# 每个外星人最初在屏幕左上角附近
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# 存储外星人的准确位置
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
		# 外星人在边缘移动的距离
		self.edge_distance = 0
	
	def check_edges(self):
		"""如果外星人位于屏幕边缘。则返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True	
		
	def update(self):
		"""向右或者左移动外星人"""
		self.x += (self.ai_settings.alien_speed_factor*
		self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image,self.rect)
	
		"""	
	def random_update(self):
		# 随机移动外星人
		if not self.check_edges():
			self.x_speed = (self.ai_settings.fleet_direction*
			random.choice(np.arange(0,1.0,0.01)))
			#self.y_speed = random.choice(np.arange(-5,5.1,0.01))
			#for i in range(20):
			self.x += (self.ai_settings.alien_speed_factor*
			self.x_speed)
			self.rect.x = self.x
			
				#self.y += (self.ai_settings.drop_speed_factor*
				#self.y_speed)
				#self.rect.y = self.y
				#self.screen.blit(self.image,self.rect)
				#pg.display.flip		
		else:
			self.x += (self.ai_settings.alien_speed_factor*
			self.ai_settings.fleet_direction)
			self.rect.x = self.x					
		"""
