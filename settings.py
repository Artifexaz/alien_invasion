"""设置设置类，储存设置项"""

class Settings():
	"""储存《外星人入侵》的所有设置项"""
	
	def __init__(self):
		"""初始化游戏的设置"""
		# 屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230) #灰白色
		# 飞船设置
		self.ship_limit = 5
		
		# 子弹设置
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (56,180,139) #翠绿
		self.bullets_allowed = 3 # 限制子弹数量

		# 外星人设置
		self.drop_distance = 13 # 指定向下移动距离
		
		# 以什么样的速度加快游戏节奏
		self.speedup_scale = 1.05
		# 外星人分数提高的速度
		self.score_scale = 1.5
		# 从那一关开始外星人全部出动
		self.level_deadline = 20
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""初始化随游戏进行而改变的设置"""
		self.ship_speed_factor = 1.3
		self.alien_speed_factor = 1
		self.bullet_speed_factor = 3
		self.level_number = 1
		self.drop_speed_factor = 0.5
		self.alien_points = 50

		# fleet_direction为1向右移动，为-1向左移动
		self.fleet_direction = 1
	
	def increase_speed(self):
		"""提高速度设置，提高外星人点数，提升级数"""
		self.ship_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.drop_speed_factor *= self.speedup_scale
		self.alien_points = int(self.score_scale * self.alien_points)
		self.level_number += 1
		#print(self.alien_points)
		
