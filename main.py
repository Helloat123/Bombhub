import pygame
from pygame.locals import *
from sys import exit
SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
BG_COLOR=pygame.Color(0,0,0)
#游戏类
class MainGame():
	window=None
	def __init__(self):
		pass
	def startGame(self):
		pygame.display.init()
		window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
		pygame.display.set_caption('Untitled')
		while True:
			window.fill(BG_COLOR)
			pygame.display.flip()
			eventList = pygame.event.get()
			for event in eventList:
				if event.type == pygame.QUIT:
					print('感谢支持')
					exit()
if __name__ == '__main__':
	MainGame().startGame()