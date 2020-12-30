import pygame
#from main import *
#from pygame.locals import *
class player():
	def __init__(self,left,top):
		self.images={
			'U':pygame.image.load('img/playerU.png').convert(),
			'D':pygame.image.load('img/playerD.png').convert(),
			'L':pygame.image.load('img/playerL.png').convert(),
			'R':pygame.image.load('img/playerR.png').convert()
		}
		self.direction='L'
		self.image=self.images[self.direction]
		self.rect=self.image.get_rect()#left大概指的是水平方向坐标...
		self.rect.left=left
		self.rect.top=top
		self.speed=5#obvious
		self.stop=True
		self.live=True
		self.oldLeft=self.rect.left#???
		self.oldTop=self.rect.top
	def move(self):
		self.oldLeft=self.rect.left
		self.oldTop=self.rect.top
		if self.direction=='L':
			if self.rect.left>0:
				self.rect.left-=self.speed
		elif self.direction == 'U':
			if self.rect.top>0:
				self.rect.top -=self.speed
		elif self.direction == 'D':
			if self.rect.top+self.rect.height<SCREEN_HEIGHT:
				self.rect.top +=self.speed
		elif self.direction == 'R':
			if self.rect.left+self.rect.height<SCREEN_WIDTH:
				self.rect.left += self.speed
	def deploy(self):
		return Bomb(self) #创建子弹对象
	def stay(self): #保持原来的位置
		self.rect.left = self.oldLeft
		self.rect.top = self.oldTop
	def displayPlayer(self): #画出坦克
		MainGame.window.blit(self.images[self.direction],self.rect)