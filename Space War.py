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
clock = pygame.time.Clock()     ## For syncing the FPS
###############################
#遊戲主畫面
def main_menu():
    global screen

    # 載入主畫面音樂
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.mp3"))
    # pygame.mixer.music.play(-1)

    # 背景圖片
    background = pygame.image.load(path.join(img_folder, "main.png")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT), screen)#縮放
    screen.blit(background, (0,0))

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
#********************* 物件 ***********************
# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        ## time out for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        # 速度歸零
        self.speedx = 0
        self.speedy = 0

        # 偵測方向鍵
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5


        # 空白建發射
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # 移動
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # 保持 左右界線
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < HEIGHT *0.75:
            self.rect.top = HEIGHT *0.75

        

    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        # 設定發射間距
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # 攻擊level 1
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            # 攻擊level 2
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            # 攻擊level 3
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# 子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()

        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        # 往前飛 飛到頂部外 消除
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# 導彈
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.rect = self.image.get_rect()

        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
#**************************************************

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

#顯示生命數
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


###################################################
# 載入圖片

#背景
background = pygame.image.load(path.join(img_folder, 'starfield.png')).convert()
background_rect = background.get_rect()

#玩家
player_img = pygame.image.load(path.join(img_folder, 'playerShip1_orange.png')).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

#飛彈
bullet_img = pygame.image.load(path.join(img_folder, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_folder, 'missile.png')).convert_alpha()
###################################################
#載入音樂

shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))

###################################################
## Game loop
running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(1000)
        menu_display = False

        bullets = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

    clock.tick(FPS)
    for event in pygame.event.get():
        #關閉視窗
        if event.type == pygame.QUIT:
            running = False

        #ESC離開遊戲
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    draw_shield_bar(screen, 10, 10, 50)#test
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip() 
    pygame.display.set_caption("Space Shooter " + str(int(clock.get_fps())) + " fps")    


pygame.quit()