import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):
	"""储存飞船的各种属性"""
	
	def __init__(self, ai_settings, screen):
		"""初始化飞船并设置其初始位置"""
		super(Ship,self).__init__() # super括号里的可以不要
		self.screen = screen
		self.ai_settings = ai_settings
		#加载飞船图像并获取其外接矩形
		self.image = pg.image.load('image/ship1.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		"""
		self.shipname = input("请问要哪一搜飞船? origin/flat/gif: ")
		if self.shipname == 'origin':
			self.image = pg.image.load('image/ship2.bmp')
			self.rect = self.image.get_rect()
			self.screen_rect = screen.get_rect()
		elif self.shipname == 'gif':
			self.image = pg.image.load('image/ship3.gif')
			self.rect = self.image.get_rect()
			self.screen_rect = screen.get_rect()
		elif self.shipname == 'flat' or self.shipname or self.shipname == '':
			self.image = pg.image.load('image/ship1.png')
			self.rect = self.image.get_rect()
			self.screen_rect = screen.get_rect()
		"""	
		
		
		# 将每艘新飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# 在飞船的属性center中存储小数值
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		# 移动标志
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False		
		
		
	def update(self):
		"""根据标志调整飞船的移动"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.centerx += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.centerx -= self.ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > self.screen_rect.top:
			#print(self.screen_rect.top)
			self.centery -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.centery += self.ai_settings.ship_speed_factor		
			
		# 根据self.center更新self.rect.centerx
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)
		
	def center_ship(self):
		"""让飞船在屏幕上居中"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
