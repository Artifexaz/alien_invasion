import sys
from random import randint
from time import sleep
#from numpy import  asarray,delete
from json import dump,load

import pygame as pg

from bullet import Bullet
from alien import Alien
from display import display_text

def check_high_score(stats, sb):
	"""检查是否诞生了新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def check_events(ai_settings,stats,sb,screen,ship,bullets,aliens
	,play_button,resume_button,restart_button):
	"""响应按键和鼠标事件"""
	for event in pg.event.get():
		if event.type == pg.QUIT:
			save_file(stats) # 退出游戏储存文件
			sys.exit()
		elif event.type == pg.KEYDOWN:
			check_keydown_events(event,ai_settings,sb,stats,
			screen,ship,bullets,aliens,play_button)
		elif event.type == pg.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pg.MOUSEBUTTONDOWN:
			stats.mouse_click = True # 表示鼠标按下
			draw_clicked_buttons(ai_settings,stats,screen,play_button,
			resume_button,restart_button)
		elif event.type == pg.MOUSEBUTTONUP:
			stats.mouse_click = False # 表示鼠标抬起	
			mouse_x,mouse_y = pg.mouse.get_pos()
			check_button(ai_settings,stats,sb,screen,ship,bullets,aliens,
			play_button,mouse_x,mouse_y,resume_button,restart_button)

def draw_clicked_buttons(ai_settings,stats,screen,
	play_button,resume_button,restart_button):
	"""画按下去的按钮"""
	mouse_x,mouse_y = pg.mouse.get_pos()
	play_button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	restart_button_cliked = restart_button.rect.collidepoint(mouse_x,mouse_y)
	resume_button_cliked = resume_button.rect.collidepoint(mouse_x,mouse_y)
	if (play_button_clicked 
		and not stats.game_active 
		and not stats.game_resume):
		"""如果点了开始就画出按下的开始键"""
		play_button.draw_button_clicked()
	elif (resume_button_cliked 
		and not stats.game_active 
		and stats.game_resume):
		"""如果点了继续就画出按下的继续键"""
		resume_button.draw_button_clicked()
	elif (restart_button_cliked
		and not stats.game_active 
		and stats.game_resume):
		"""如果点了重新开始就画出按下的重新开始键"""
		restart_button.draw_button_clicked()


def check_button(ai_settings,stats,sb,screen,ship,bullets,aliens,
	play_button,mouse_x,mouse_y,resume_button,restart_button):
	"""在玩家单击play按钮时开始游戏"""
	play_button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	restart_button_cliked = restart_button.rect.collidepoint(mouse_x,mouse_y)
	resume_button_cliked = resume_button.rect.collidepoint(mouse_x,mouse_y)
	if (play_button_clicked 
		and not stats.game_active 
		and not stats.game_resume):
		"""如果点了开始就开始游戏，且在暂停和游戏中点那个位置是无效的"""
		# 重置游戏的设置
		ai_settings.initialize_dynamic_settings()
		start_game(ai_settings,stats,sb,screen,ship,bullets,aliens,
		play_button)
	elif (resume_button_cliked 
		and not stats.game_active 
		and stats.game_resume):
		"""如果游戏没有处于活动，且处于暂停，则点暂停有效"""
		stats.game_active = True
		stats.game_resume = False
	elif (restart_button_cliked
		and not stats.game_active 
		and stats.game_resume):
		"""如果游戏没有处于活动，且处于暂停，则点重新开始有效"""
		stats.game_resume = False
		ai_settings.initialize_dynamic_settings()
		start_game(ai_settings,stats,sb,screen,ship,bullets,aliens,
		play_button)

	
def start_game(ai_settings,stats,sb,screen,ship,bullets,aliens,
	play_button):
	# 隐藏光标
	pg.mouse.set_visible(False)
	# 重置游戏统计信息
	stats.reset_stats()
	screen.fill(ai_settings.bg_color)
	#pg.display.flip()
	display_text(f"LEVEL No.{ai_settings.level_number}",screen,
	ai_settings.screen_width/2,ai_settings.screen_height/2,150,
	(54,146,50)) # 墨绿
	pg.display.flip()
	sleep(1)
	stats.game_active = True
	# 清空外星人列表和子弹列表，重置得分等级，飞船图像
	sb.prep_score()
	sb.prep_level()
	sb.prep_ship()
	aliens.empty()
	bullets.empty()
	# 创建一群新的外星人，并让飞船居中
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()
				
def check_keydown_events(event,ai_settings,sb,stats,
	screen,ship,bullets,aliens,play_button):
	"""响应按键"""
	if event.key == pg.K_RIGHT or event.key == 100: # D=100
		ship.moving_right = True
	elif event.key == pg.K_LEFT or event.key == 97: # A=97
		ship.moving_left = True
	elif event.key == pg.K_UP or event.key == 119: # W=119
		ship.moving_up = True
	elif event.key == pg.K_DOWN or event.key == 115: # S=115
		ship.moving_down = True
	elif event.key == pg.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == 27: # esc键=27
		save_file(stats) # 退出游戏储存文件
		sys.exit()
	elif event.key == pg.K_p and not stats.game_resume: 
		# 如果没暂停，按了p开始游戏
		start_game(ai_settings,stats,sb,screen,ship,bullets,aliens,
		play_button)
	elif event.key == pg.K_r: # 按了R键重新开始游戏
		stats.game_active = False
		stats.game_resume = True
		screen.fill(ai_settings.bg_color)
		pg.mouse.set_visible(True)
	elif event.key == pg.K_u: # 按了u键继续
		stats.game_active = True
		stats.game_resume = False
		#screen.fill(ai_settings.bg_color)
		pg.mouse.set_visible(False)
		
def check_keyup_events(event,ship):
	"""响应松键"""		
	if event.key == pg.K_RIGHT or event.key == 100:
		ship.moving_right = False
	elif event.key == pg.K_LEFT or event.key == 97:
		ship.moving_left = False
	elif event.key == pg.K_UP or event.key == 119:
		ship.moving_up = False
	elif event.key == pg.K_DOWN or event.key == 115:
			ship.moving_down = False
			
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	"""检查是否有外星人到达了屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样进行处理
			display_text("Alien hit!!!",
			screen,ai_settings.screen_width/2,
			ai_settings.screen_height/2,150,
			(226,4,27)) # 猩红色
			pg.display.flip()
			sleep(1)
			ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
			break

def fire_bullet(ai_settings,screen,ship,bullets):
	"""如果还没到达数量限制，就发射一颗子弹"""
	# 创建新子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed: 
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
	
def update_bulltes(ai_settings,sb,screen,ship,aliens,bullets):
	"""更新子弹位置，并删除已消失的子弹"""
	# 更新子弹位置
	bullets.update()
		
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)	
	#print(len(bullets))
	check_bullet_alien_collisions(ai_settings,sb,screen,
	ship,aliens,bullets)


def check_bullet_alien_collisions(ai_settings,sb,screen,ship,aliens,
	bullets):
	"""响应子弹和外星人的碰撞，并更新得分"""
	# 检查是否有子弹击中了外星人
	# 如果击中了，就删除相应的外星人和子弹
	collisions = pg.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values(): # 确保所有被击落的外星人计入分数
			sb.stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
			check_high_score(sb.stats, sb)
	# false,true的话，子弹不会消失
	if len(aliens) == 0:
		# 加快游戏速度，删除现有的子弹并新建一群外星人
		ai_settings.increase_speed()
		screen.fill(ai_settings.bg_color)
		sb.prep_level() # 更新级数图像
		if ai_settings.level_number < ai_settings.level_deadline:
			display_text(f"LEVEL No.{ai_settings.level_number}",screen,
			ai_settings.screen_width/2,ai_settings.screen_height/2,150,
			(54,146,50)) # 墨绿
		else:
			display_text(f"LEVEL No.{ai_settings.level_number}",screen,
			ai_settings.screen_width/2,ai_settings.screen_height/2,150,
			(215,49,59)) # 红			
		bullets.empty()
		ship.center_ship()
		create_fleet(ai_settings, screen, ship, aliens)
		pg.display.flip()
		sleep(1.5)			
		
							
def update_screen(ai_settings,stats,sb,screen,ship,aliens,bullets,
	play_button,resume_button,restart_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	# 填充背景色
	#screen.fill(ai_settings.bg_color)
	
	if stats.game_active and not stats.game_resume:
		# 如果游戏活动且没有暂停
		screen.fill(ai_settings.bg_color)
		sb.show_score()
			#在飞船和外星人前重绘所有子弹
		for bullet in bullets.sprites():
			bullet.draw_bullet()
		# 绘制飞船和外星人
		ship.blitme()
		aliens.draw(screen)
	elif not stats.game_active and not stats.game_resume: 
		# 如果游戏处于非活动状态且没有暂停，就绘制Play按钮，显示最高分
		if not stats.mouse_click: # 鼠标没按下就画原来的按键
			play_button.draw_button()
		else: # 鼠标按下就画按下的按键
			draw_clicked_buttons(ai_settings,stats,screen,
			play_button,resume_button,restart_button)
		display_text("外 星 人 入 侵",screen,
		ai_settings.screen_width/2,ai_settings.screen_height/2-250,102,
		(150,150,150)) # 标题黑色边框
		display_text("外 星 人 入 侵",screen,
		ai_settings.screen_width/2,ai_settings.screen_height/2-250,100,
		sb.title_color) # 橘黄
		# 读取最高分文件
		read_file(ai_settings,stats,sb,screen)
		# 显示操作说明
		show_control(ai_settings,sb,screen)
	elif not stats.game_active and stats.game_resume:
		# 如果游戏处于暂停，就绘制重新开始和继续按钮，显示最高分
		if not stats.mouse_click: # 鼠标没按下就画原来的按键
			resume_button.draw_button()
			restart_button.draw_button()
		# 读取最高分文件
		read_file(ai_settings,stats,sb,screen)
		# 显示当前得分
		display_text(f"当前得分: {'{:,}'.format(round(stats.score,-1))}",
		screen,ai_settings.screen_width/2,ai_settings.screen_height/2-200,25,
		(0,0,0)) # 黑色
		# 显示操作说明
		show_control(ai_settings,sb,screen)
	#让最近绘制的屏幕可见
	pg.display.flip() 

def show_control(ai_settings,sb,screen):
	"""显示操作说明"""
	display_text("操作说明",screen,
	ai_settings.screen_width/2,ai_settings.screen_height/2+110,30,
	(0,0,0)) # 黑色
	display_text("R: 暂停  U: 继续  P: 开始  esc: 退出游戏",screen,
	ai_settings.screen_width/2,ai_settings.screen_height/2+160,25,
	(0,0,0)) # 黑色
	display_text("方向控制：W S A D or 方向键  射击：空格",screen,
	ai_settings.screen_width/2,ai_settings.screen_height/2+200,25,
	(0,0,0)) # 黑色	
		
def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行有多少个外星人"""
	# 创建一个外星人，并计算一行可以容纳多少外星人
	# 外星人间距为外星人宽度
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_aliens_y(ai_settings,ship_height,alien_height):
	"""计算屏幕可以容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - 
	(3*alien_height) - ship_height)
	number_aliens_y = int(available_space_y/(2*alien_height))
	return number_aliens_y

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""创建外星人并放在当前行"""
	# 创建一个外星人并将其加入当前行
	alien = Alien(ai_settings, screen)
	alien.x = alien.rect.width + 2*alien.rect.width*alien_number
	alien.y = alien.rect.height + 2*alien.rect.height*row_number
	alien.rect.x = alien.x
	alien.rect.y = alien.y
	aliens.add(alien)
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_aliens_y = get_number_aliens_y(ai_settings,ship.rect.height,
	alien.rect.height)
	# 创建第一行外星人
	aliens_matrix = []
	for i in range(number_aliens_x):
		for k in range(number_aliens_y):
			aliens_matrix.append([i,k])
	#aliens_matrix = asarray(aliens_matrix) # 坐标矩阵
	while True: # 如果将要创建的外星人数量过多或还未到达deadline等级，则继续删除
		random_delet = randint(0,len(aliens_matrix)-1)
		# 随机删除某个外星人
		level_fact = (len(aliens_matrix) <=
		int(number_aliens_y*number_aliens_x*ai_settings.level_number/
		ai_settings.level_deadline))
		if level_fact:
			break
		# 最后再随机删除外星人
		del aliens_matrix[random_delet]
	for alien_number,row_number in aliens_matrix:
		create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取相应措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			alien.edge_distance += ai_settings.drop_speed_factor*1
			#ai_settings.fleet_direction)
			#print(alien.edge_distance)
			#print(ai_settings.fleet_direction)
			change_fleet_direction(ai_settings,aliens,alien)
			# 如果边上的alien移动距离超过指定距离，移动距离清零
			#if alien.edge_distance >= ai_settings.drop_distance:
				#alien.edge_distance = 0
			break		

def change_fleet_direction(ai_settings,aliens,alien_edge):
	for alien in aliens.sprites():
		alien.y += ai_settings.drop_speed_factor 
		alien.rect.y = alien.y 
	if alien_edge.edge_distance >= ai_settings.drop_distance:
	#or alien_edge.edge_distance <= -ai_settings.drop_distance):
		ai_settings.fleet_direction *= -1
		alien_edge.edge_distance = 0
		#print(alien_edge.edge_distance)
		#print(ai_settings.fleet_direction)
		#for alien in aliens.sprites(): 
			#alien.rect.x += ai_settings.fleet_direction*5			
				
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
	"""
	检查是否有外星人到达屏幕边缘
	更新外星人群中所有外星人的位置
	"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	#for alien in aliens.sprites():
		#alien.random_update()
	# 检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
	# 检测外星人和飞船之间的碰撞
	if pg.sprite.spritecollideany(ship,aliens):
		display_text("Ship hit!!!",
		screen,ai_settings.screen_width/2,
		ai_settings.screen_height/2,150,
		(226,4,27)) # 猩红色
		pg.display.flip()
		# 暂停
		sleep(1)
		ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
		
def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
	"""响应被外星人撞到的飞船和外星人到达屏幕底端"""
	if stats.ships_left > 0:
		# 将ship_left减1，并更新飞船剩余图像
		stats.ships_left -= 1
		sb.prep_ship()
		# 清空外星人和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新外星人，并将飞船放到屏幕底端中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

	else:
		screen.fill(ai_settings.bg_color)
		stats.game_active = False
		pg.mouse.set_visible(True)
		display_text("请按esc退出",
		screen,ai_settings.screen_width/2,60,32,
		(226,4,27)) # 猩红色	
		if ai_settings.level_number <= ai_settings.level_deadline*(3/4):
			display_text(
			f"您的手速需要锻炼，只达到了第{ai_settings.level_number}级",
			screen,ai_settings.screen_width/2,20,40,
			(56,180,139)) # 鹦鹉绿
			pg.display.flip()
		elif ai_settings.level_number <= ai_settings.level_deadline:
			display_text(
			f"哎呦不错哦小伙汁，你达到了第{ai_settings.level_number}级",
			screen,ai_settings.screen_width/2,20,40,
			(56,180,139)) # 鹦鹉绿
			pg.display.flip()
		elif ai_settings.level_number > ai_settings.level_deadline:
			display_text(
			f"您的手速已逆天，达到了第{ai_settings.level_number}级",
			screen,ai_settings.screen_width/2,20,40,
			(56,180,139)) # 鹦鹉绿
			pg.display.flip()

def save_file(stats): # 写入
	try:
		with open("highest_score.json", 'r')as highest_score: # 读取
			file_high_score = round(load(highest_score))
	except FileNotFoundError:
		file_high_score = 0
	# 是否等于零，并且对比是否有区别，有区别且不等于零就写入
	if (stats.high_score != 0 and stats.high_score != file_high_score):
		with open("highest_score.json", 'w')as highest_score: # 写入
			dump(round(stats.high_score,-1),highest_score)
		
def read_file(ai_settings,stats,sb,screen): # 读取
	try:
		if stats.high_score == 0: # 没有最高得分才要读取
			with open("highest_score.json", 'r')as highest_score: # 读取
				stats.high_score = round(load(highest_score))
	except FileNotFoundError:
		if stats.high_score == 0:
			display_text("你还未创造过最高分",screen,
			ai_settings.screen_width/2,
			ai_settings.screen_height/2-150,40,
			sb.text_color)
		else:
			display_text("当前最高得分: " + 
			"{:,}".format(round(stats.high_score,-1)),screen,
			ai_settings.screen_width/2,
			ai_settings.screen_height/2-150,40,
			sb.text_color)
	else: # 如果有文件就显示当前最高分
		display_text("当前最高得分: " + 
		"{:,}".format(round(stats.high_score,-1)),screen,
		ai_settings.screen_width/2,
		ai_settings.screen_height/2-150,40,
		sb.text_color)			

