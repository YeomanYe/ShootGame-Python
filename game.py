# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random

#设置游戏屏幕大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

#子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self,bullet_img,init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 10

	def move(self):
		self.rect.top -= self.speed

#玩家飞机类
class Player(pygame.sprite.Sprite):
	def __init__(self,plane_img,player_rect,init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = [] 
		for i in range(len(player_rect)):
			self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
		self.rect = player_rect[0]
		self.rect.topleft = init_pos
		self.speed = 8
		#初始化玩家飞机速度
		self.bullets = pygame.sprite.Group()
		self.img_index = 0
		self.is_hit = False

	#发射子弹
	def shoot(self,bullet_img):
		bullet = Bullet(bullet_img,self.rect.midtop)
		self.bullets.add(bullet)

	#向上移动
	def moveUp(self):
		#判断边界
		if self.rect.top <= 0:
			self.rect.top = 0
		else:
			self.rect.top -= self.speed

	def moveDown(self):
		if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top += self.speed

	def moveLeft(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed

	def moveRight(self):
		if self.rect.left >= SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
	def __init__(self,enemy_img,enemy_down_imgs,init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_down_imgs
		self.speed = 2
		self.down_index = 0

	def move(self):
		self.rect.top += self.speed

#初始化游戏
pygame.init()

#环境属性设置
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#游戏界面标题
pygame.display.set_caption('飞机大战')
#游戏背景图
background = pygame.image.load('resources/image/background.png').convert()
#gameover背景图
game_over = pygame.image.load('resources/image/gameover.png')
#飞机及子弹图片集合
plane_img = pygame.image.load('resources/image/shoot.png')

#设置玩家及飞机不同状态的图片列表,多张图片动画效果
player_rect = []
player_rect.append(pygame.Rect(0,99,102,126)) 
player_rect.append(pygame.Rect(165,360,102,126))
#飞机爆炸图片
player_rect.append(pygame.Rect(165,234,102,126))
player_rect.append(pygame.Rect(330,624,102,126))
player_rect.append(pygame.Rect(330,498,102,126))
player_rect.append(pygame.Rect(432,624,102,126))
player_pos = [200,600]
player = Player(plane_img,player_rect,player_pos)

#子弹图片
bullet_rect = pygame.Rect(1004,987,9,21)
bullet_img = plane_img.subsurface(bullet_rect)

#敌机不同状态的图片列表
enemy1_rect = pygame.Rect(534,612,57,43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267,347,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873,697,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267,296,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930,697,57,43)))

enemies1 = pygame.sprite.Group()

# 存储被击落的飞机
enemies_down = pygame.sprite.Group()

#初始化射击及敌人移动频率
shoot_frequency = 0
enemy_frequency = 0

#玩家被击中效果处理
player_down_index = 16

#初始化分数
score = 0

#游戏循环帧率设置
clock = pygame.time.Clock()

#判断游戏循环退出的参数
running  = True

#游戏主循环
while running:
	clock.tick(60)

	#生成子弹，需要控制发射频率
	#首先判断玩家飞机没有被击中
	if not player.is_hit:
		if shoot_frequency % 15 == 0:
			player.shoot(bullet_img)
		shoot_frequency += 1
		if shoot_frequency >= 15:
			shoot_frequency = 0

	#生成敌机,需要控制生成频率
	if enemy_frequency % 50 == 0:
		enemy1_pos = [random.randint(0,SCREEN_WIDTH - enemy1_rect.width),0]
		enemy1 = Enemy(enemy1_img,enemy1_down_imgs,enemy1_pos)
		enemies1.add(enemy1)
	enemy_frequency += 1
	if enemy_frequency >= 100:
		enemy_frequency = 0

	for bullet in player.bullets:
		#以固定速度移动子弹
		bullet.move()
		#移动出屏幕后删除子弹
		if bullet.rect.bottom < 0:
			player.bullets.remove(bullet)

	for enemy in enemies1:
		enemy.move()
		if pygame.sprite.collide_circle(enemy,player):
			enemies_down.add(enemy)
			enemies1.remove(enemy)
			player.is_hit = True
			break
		if enemy.rect.top < 0:
			enemies1.remove(enemy)

	#敌机被子弹击中效果处理
	enemies1_down = pygame.sprite.groupcollide(enemies1,player.bullets,1,1)
	for enemy_down in enemies1_down:
		enemies_down.add(enemy_down)

	#绘制背景
	screen.fill(0)
	screen.blit(background,(0,0))

	if not player.is_hit:
		#绘制玩家飞机
		screen.blit(player.image[int(player.img_index)],player.rect)
		player.img_index = shoot_frequency / 8
	else:
		#玩家被击中效果处理
		player.img_index = player_down_index / 8
		screen.blit(player.image[int(player.img_index)],player.rect)
		player_down_index += 1
		if player_down_index > 47:
			#击中效果处理后，游戏结束
			running = False

	#敌机被子弹击中效果显示
	for enemy_down in enemies_down:
		if enemy_down.down_index == 0:
			pass
		if enemy_down.down_index > 7:
			enemies_down.remove(enemy_down)
			score += 1000
			continue
		screen.blit(enemy_down.down_imgs[int(enemy_down.down_index / 2)],enemy_down.rect)
		enemy_down.down_index += 1

	#显示子弹
	player.bullets.draw(screen)
	#显示敌框
	enemies1.draw(screen)

	#绘制得分
	score_font = pygame.font.Font(None,36)
	score_text = score_font.render(str(score),True,(128,128,128))
	text_rect = score_text.get_rect()
	text_rect.topleft = [10,10]
	screen.blit(score_text,text_rect)

	#更新屏幕
	pygame.display.update()

	#处理游戏退出
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	#获取键盘事件
	key_pressed = pygame.key.get_pressed()

	#处理键盘事件
	if key_pressed[K_w] or key_pressed[K_UP]:
		player.moveUp()
	if key_pressed[K_s] or key_pressed[K_DOWN]:
		player.moveDown()
	if key_pressed[K_a] or key_pressed[K_LEFT]:
		player.moveLeft()
	if key_pressed[K_d] or key_pressed[K_RIGHT]:
		player.moveRight()

#游戏Game Over后显示最终得分
font = pygame.font.Font(None,48)
text = font.render('Score: ' + str(score),True,(255,0,0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over,(0,0))
screen.blit(text,text_rect)

#显示得分并处理游戏退出
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	pygame.display.update()