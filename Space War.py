#coding=utf-8
import pygame
import random
from os import path

#檔案夾
img_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

#參數規格
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

#顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

###############################
#初始化 & 創建視窗
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空戰爭")
clock = pygame.time.Clock()	 ## For syncing the FPS
###############################

#遊戲主畫面
def main_menu():
	global screen

	menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.mp3"))
	pygame.mixer.music.play(-1)

	title = pygame.image.load(path.join(img_folder, "main.png")).convert()
	title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)#縮放

	screen.blit(title, (0,0))

	draw_text(screen, "按下 [ENTER] 開始遊戲", 30, WIDTH/2, HEIGHT/2)
	draw_text(screen, "or [Q] 離開", 30, WIDTH/2, (HEIGHT/2)+40)
	pygame.display.update()
	while True:
		event = pygame.event.poll() # 取一個事件
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:#進入遊戲
				break
			elif event.key == pygame.K_q:#離開
				pygame.quit()
				quit()
		elif event.type == pygame.QUIT:
				pygame.quit()
				quit() 
			

	#pygame.mixer.music.stop()
	ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
	ready.play()
	screen.fill(BLACK)
	draw_text(screen, "倒數三秒鐘!", 40, WIDTH/2, HEIGHT/2)
	pygame.display.update()

#顯示 文字
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font("msjh.ttf", size)
	text_surface = font.render(text, False, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

#顯示 護甲
def draw_shield_bar(surf, x, y, pct):
	pct = max(pct, 0) 

	shield_NUM = (pct / 100) * BAR_LENGTH
	total_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	shield_rect = pygame.Rect(x, y, shield_NUM, BAR_HEIGHT)
	
	pygame.draw.rect(surf, BLUE, shield_rect)
	pygame.draw.rect(surf, WHITE, total_rect, 2)

#顯示 
def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect= img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img, img_rect)

#############################
## Game loop
running = True
menu_display = True
while running:
	if menu_display:
		main_menu()
		pygame.time.wait(1000)

	clock.tick(FPS)
	for event in pygame.event.get():
		#關閉視窗
		if event.type == pygame.QUIT:
			running = False

		#ESC離開遊戲
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
	draw_shield_bar(screen, 10, 10, 50)#test
	pygame.display.flip()	
	pygame.time.wait(1000)


pygame.quit()