import pygame as pg

def display_text(text,screen,centerx,centery,text_size,text_color):
	"""显示一段文字"""
	ZiTiDuiXiang=pg.font.SysFont('SimHei',text_size)
	WenBenKuangDuiXiang=ZiTiDuiXiang.render(text, True,text_color)
	KuangDuiXiang=WenBenKuangDuiXiang.get_rect()
	KuangDuiXiang.center=(centerx,centery)
	screen.blit(WenBenKuangDuiXiang,KuangDuiXiang)
	#pg.display.update()
