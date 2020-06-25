import pygame as pg
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	
	def __init__(self, ai_settings, screen, stats):
		"""初始化计分板显示器的属性"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		# 显示信息时使用的字体设置
		self.text_color = (30,30,30) # 深灰
		self.title_color = (255,204,0) # 橘黄
		self.font = pg.font.SysFont('SimHei', 30)
		
		# 准备初始的分图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ship()
		
	def prep_score(self):
		"""将得分转换为一幅渲染的图像"""
		rounded_score = round(self.stats.score,-1) # -1表示整圆到最近的10倍数
		self.score_str = "{:,}".format(rounded_score)
		"""
		这里使用了一个字符串格式设置指令，它让python将数值转换为字符串时，
		在其中插入逗号，例如输出1,000,000而不是1000000
		"""
		self.score_image = self.font.render("得分: " + self.score_str,
		True,self.text_color,self.ai_settings.bg_color)
		
		# 将得分放在屏幕右上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = self.screen_rect.top + 10
		
	def prep_high_score(self):
		"""将最高得分转换为一幅渲染的图像"""
		rounded_score = round(self.stats.high_score,-1) # -1表示整圆到最近的10倍数
		self.high_score_str = "{:,}".format(rounded_score)

		self.high_score_image = self.font.render("最高分: "
		+ self.high_score_str,True,self.text_color,
		self.ai_settings.bg_color)
		
		# 将得分放在屏幕右上角
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top + 10		
	
	def prep_level(self):
		"""将等级数转换为一幅渲染的图像"""
		self.level_str = str(self.ai_settings.level_number)
		
		self.level_image = self.font.render("等级: " + self.level_str,
		True,self.text_color,self.ai_settings.bg_color)
		
		# 将得分放在屏幕右上角
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right - 20
		self.level_rect.top = self.screen_rect.top + 50
		
	def prep_ship(self):
		"""显示还余下多少搜飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.left = (self.screen_rect.left + 20 +
			ship_number * ship.rect.width * 1.2)
			ship.rect.top = self.screen_rect.top + 10
			self.ships.add(ship)

	def show_score(self):
		"""在屏幕上显示得分"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)
	
	
	
