from json import load

class GameStats():
	"""跟踪游戏的统计信息"""
	
	def __init__(self,ai_settings):
		"""初始化统计信息"""
		self.ai_settings = ai_settings
		self.reset_stats() # 重置统计信息
		
		# 除非玩家reset最高分，否者不改变最好分
		try:
			with open("highest_score.json", 'r')as highest_score: # 读取
				self.high_score = round(load(highest_score))
		except FileNotFoundError:
			self.high_score = 0
				
		# 游戏刚启动时处于活动状态
		self.game_active = False
		
		# 刚启动时游戏不处于暂停状态
		self.game_resume = False
		
		# 鼠标按下没拿起来的的标志
		self.mouse_click = False
		
	def reset_stats(self):
		"""初始化在游戏运行期间可能变化的统计信息"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		#self.level = 1 在ai_settings里用level_number代替了
