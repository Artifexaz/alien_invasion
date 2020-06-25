#coding:utf-8
#import sys

import pygame as pg
from pygame.sprite import Group 

from settings import Settings
from ship import Ship
import game_function as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
#from alien import Alien

def run_game():
	# 初始化游戏并创建一个屏幕对象
	#pygame.font.init()
	#cur_font = pygame.font.SysFont("semiHei",10)
	pg.init() # 初始化背景设置
	ai_settings = Settings()
	screen = pg.display.set_mode((ai_settings.screen_width,
	ai_settings.screen_height))
	screen.fill(ai_settings.bg_color) # 事先填充所需颜色
	# 创建一个名为screen的显示窗口，实参(1200,800)是一个元组，指的是游戏窗口尺寸
	
	pg.display.set_caption('外星人入侵!')
	# 对象screen是一个surface，在这个游戏中，每个元素（外星人，飞船）都是个surface
	# 我们激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface
	
	# 创建一个play按钮，一个继续按钮，一个重新开始按钮
	play_button = Button(ai_settings,screen,"开始游戏",[56,180,139], # 翠绿
	ai_settings.screen_width/2,ai_settings.screen_height/2) 
	resume_button = Button(ai_settings,screen,"继续",[42,146,165], # 墨绿
	ai_settings.screen_width/2,ai_settings.screen_height/2+50)
	restart_button = Button(ai_settings,screen,"重新开始",[216,95,77], # 红
	ai_settings.screen_width/2,ai_settings.screen_height/2-50)
	
	# 创建一个用于存储游戏统计信息的实例和一个计分板实例
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	# 创建一艘飞船，个用于存储子弹和外星人的编组Group
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	# 创建一个外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# 开始游戏的主循环
	while True:
		# 监视键盘和鼠标事件
		gf.check_events(ai_settings,stats,sb,screen,ship,bullets,aliens
		,play_button,resume_button,restart_button)
		if stats.game_active:
			# 更新飞船、子弹和外星人的位置
			ship.update()
			gf.update_bulltes(ai_settings,sb,screen,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
			# 更新屏幕
		gf.update_screen(ai_settings ,stats, sb ,screen, ship, 
		aliens, bullets, play_button,resume_button,restart_button)
		
run_game()
