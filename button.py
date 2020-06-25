import pygame as pg

class Button():
	
	def __init__(self,ai_settings,screen,msg,button_color,x,y):
		"""初始化按钮属性"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.msg = msg
		self.x = x
		self.y = y
		
		# 设置按钮的尺寸和其他属性
		self.width, self.height = 200, 50
		self.button_color = button_color
		self.text_color = (0,0,0) # 黑色
		self.font = pg.font.SysFont('SimHei', 40) # None让其用默认字体

		# 创建按钮的rect对象，并使其居中
		self.rect = pg.Rect(0,0,self.width,self.height)
		self.rect.centerx = self.x
		self.rect.centery = self.y
		
		# 设置被按到的play按钮
		self.button_color_clicked = [i-20 for i in button_color]
		# 看起来暗一点
		self.font_clicked = pg.font.SysFont('SimHei', 40-2)
		self.width_clicked, self.height_clicked = 190, 40
		
		self.rect_clicked = pg.Rect(0,0,self.width_clicked,
		self.height_clicked)
		self.rect_clicked.centerx = self.x
		self.rect_clicked.centery = self.y
		
		# 按钮的标签只需创建一次
		self.prep_msg()
		"""
		pygame通过将你要显示的字符串渲染为图像来处理文本，
		调用prep_msg()来处理这样的渲染
		"""
		
	def prep_msg(self):
		"""将msg渲染为图像，并使其在按钮上居中"""
		self.msg_image = self.font.render(self.msg, True, self.text_color)
		#(255,255,255)) 
		# True开启反锯齿功能，使文本边缘更平滑，后面是文字颜色和背景色
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
		
	def draw_button(self):
		"""绘制一个用颜色填充的按钮，再绘制文本"""
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.msg_image,self.msg_image_rect)

	def draw_button_clicked(self):
		"""绘制被按的按钮和文字"""
		# 文字
		self.msg_image_clicked = self.font_clicked.render(self.msg,
		True,self.text_color)
		self.msg_image_clicked_rect = self.msg_image_clicked.get_rect()
		self.msg_image_clicked_rect.center = self.rect_clicked.center
		
		# 绘制被按的按钮
		#pg.display.update()
		self.screen.fill(self.button_color_clicked,self.rect_clicked)
		self.screen.blit(self.msg_image_clicked,
		self.msg_image_clicked_rect)
		
		
