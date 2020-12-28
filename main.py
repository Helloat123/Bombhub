import pygame
from pygame.locals import *
from sys import exit
from player import *
SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
BG_COLOR=pygame.Color(0,0,0)
NUMBER_OF_PLAYERS=2
POSITION_OF_PLAYERS=[[50,50],[250,250],[50,250],[250,50]]
#游戏类
class MainGame():
	window=None
	died=None
	players=[]
	def __init__(self):
		pass
	def startGame(self):
		pygame.display.init()
		self.window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
		pygame.display.set_caption('Untitled')
		self.createplayer()
		while True:
			self.window.fill(BG_COLOR)
			pygame.display.flip()
			eventList = pygame.event.get()
			for event in eventList:
				if event.type == pygame.QUIT:
					print('感谢支持')
					exit()
			self.blitPlayers()
			pygame.display.update()
	def createplayer(self):
		for i in range(0,NUMBER_OF_PLAYERS):
			self.players.append(player(POSITION_OF_PLAYERS[i][0],POSITION_OF_PLAYERS[i][1]))
	def blitPlayers(self):
		if len(self.players)==0:
			pass
		else:
			for i in self.players:
				self.window.blit(i.images[i.direction],i.rect)

if __name__ == '__main__':
	MainGame().startGame()