import pygame
import sys
from pygame.locals import *
from mapediter import *
from bomb import *
from properties_panel import *
# 设置游戏屏幕大小

BORDER_UP_LEFT=15
BORDER_DOWN_RIGHT=585
player_num=0


class Player(pygame.sprite.Sprite):

	def __init__(self, screen, position, blocks, number):
		super().__init__()
		global player_num
		self.screen=screen
		self.blocks=blocks
		self.image={}
		self.speed=0.45
		self.shoes=0
		self.scope=1
		self.bombs=1
		self.HP=1
		player_num+=1
		self.id=player_num
		if player_num==2: player_num=0
		self.pasted_bombs=0
		directions=['up','down','left','right']
		for i in directions:
			self.image[i]=pygame.image.load('resources/image/player'+str(number)+'_{}.png'.format(i)).convert_alpha()
		self.current_image=self.image['down']
		self.dir='down'
		self.rect=self.current_image.get_rect()
		# self.rect=pygame.Rect(position[0],position[1],30,30)
		self.rect.topleft=position
		self.top=position[0]
		self.left=position[1]
		self.show()
		self.tools=[]
		PropertiesPanel.draw_panel(self.screen,self.id,self.HP,self.shoes,self.scope,self.bombs)

	def check_position(self, state, collision):
		c_left=collision.rect.left #障碍物的左边界
		c_top=collision.rect.top #障碍物的上边界
		top=self.rect.top #角色的上边界
		bottom=self.rect.bottom #角色的下边界
		left=self.rect.left #角色的左边界
		right=self.rect.right #角色的右边界
		#障碍物的中心坐标
		x=collision.rect.centerx
		y=collision.rect.centery
		#碰撞检测的距离
		width=self.rect.width//3-1
		if state=='up' and (x>left-width and x<right+width): return top>c_top
		elif state=='down' and (x>left-width and x<right+width): return top<c_top
		elif state=='left' and (y>top-width and y<bottom+width): return left>c_left
		elif state=='right' and (y>top-width and y<bottom+width): return left<c_left
		else: return False

	def move(self, direction):
		self.dir=direction
		self.current_image=self.image[direction]
		if direction=='up':
			if self.rect.top<=BORDER_UP_LEFT:
				self.rect.top=BORDER_UP_LEFT
			else:
				self.top-=self.speed
		elif direction=='down':
			if self.rect.top>=BORDER_DOWN_RIGHT-self.rect.height:
				self.rect.top=BORDER_DOWN_RIGHT-self.rect.height
			else:
				self.top+=self.speed
		elif direction=='left':
			if self.rect.left<=BORDER_UP_LEFT:
				self.rect.left=BORDER_UP_LEFT
			else:
				self.left-=self.speed
		else:
			if self.rect.left>=BORDER_DOWN_RIGHT-self.rect.width:
				self.rect.left=BORDER_DOWN_RIGHT-self.rect.width
			else:
				self.left+=self.speed
		self.rect.top=int(self.top)
		self.rect.left=int(self.left)

		collisions = pygame.sprite.spritecollide(self, self.blocks, False)
		collision = None
		flag = False
		if collisions:
			for collision in collisions:
				if self.check_position(direction,collision):
					flag = True
					break
		if collisions and flag:
			if collision.category in TOOL:
				self.eat_tool(collision)
			else:
				print(collision.category)
				if direction=='up': self.top+=self.speed
				elif direction=='down': self.top-=self.speed
				elif direction=='left': self.left+=self.speed
				elif direction=='right': self.left-=self.speed
		self.rect.top=int(self.top)
		self.rect.left=int(self.left)
		print(self.rect.top,self.rect.left)

	def eat_tool(self, tool):
		mymap = MapEditer.instance()
		mymap.blocks.remove(tool)
		mymap.refresh()
		if tool.category==TOOL_SPEED_UP and self.speed<1:
			self.speed+=0.08
			self.shoes+=1
		elif tool.category==TOOL_SCOPE_UP:
			self.scope+=1
		elif tool.category==TOOL_BOMBS_UP:
			self.bombs+=1
		else:
			self.HP+=1
		self.tools.append(tool)
		PropertiesPanel.draw_panel(self.screen,self.id,self.HP,self.shoes,self.scope,self.bombs)

	def show(self):
		self.screen.blit(self.current_image, self.rect)

	def PasteBomb(self, bombs):
		if self.pasted_bombs>=self.bombs: return
		# 炸弹出现在自身坐标
		col=self.rect.left//30+1
		row=self.rect.top//30+1
		init_pos=(col,row)
		block=Bomb(init_pos)
		for bomb in bombs:
			if bomb.rect.topleft==block.rect.topleft: return
		self.pasted_bombs+=1
		block.setHost(self)
		block.setPlayers(self.players)
		block.setScope(self.scope)
		return block

	def recover(self):
		self.pasted_bombs-=1

	def HP_reduce(self):
		self.HP-=1
		PropertiesPanel.draw_panel(self.screen,self.id,self.HP,self.shoes,self.scope,self.bombs)
		return self.HP==0

	def setPlayers(self,players):
		self.players=players

	@staticmethod
	def playerInit(screen,blocks):
		player1=Player(screen,(15,15),blocks,1)
		player2=Player(screen,(555,555),blocks,2)
		players=[]
		players.append(player1)
		players.append(player2)
		player1.setPlayers(players)
		player2.setPlayers(players)
		return (player1,player2,players)


class MusicPlayer():

	def __init__(self, mixer, path='resources/music/bg_music.mp3'):
		self.mixer=mixer
		self.mixer.pre_init(44100,16,2,1024*4)
		self.path=path
		TRACK_END=USEREVENT + 1
		pygame.mixer.music.set_endevent(TRACK_END)

	def play_music(self):
		self.mixer.music.load(self.path)
		self.mixer.music.play(-1)


def handle_event(players, bombs, is_pause, is_start):
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
	key_p1={K_w:'up',K_s:'down',K_a:'left',K_d:'right'}
	key_p2={K_UP:'up',K_DOWN:'down',K_LEFT:'left',K_RIGHT:'right'}
	key_pressed=pygame.key.get_pressed()
	# 处理键盘事件（移动位置）
	# 放炸弹
	if is_pause or is_start: return
	if key_pressed[K_SPACE] and players[0]:
		bomb = players[0].PasteBomb(bombs)
		if bomb: bombs.add(bomb)
	if key_pressed[K_KP0] and players[1]:
		bomb = players[1].PasteBomb(bombs)
		if bomb: bombs.add(bomb)
	if players[0]:
		if ((players[0].rect.top-15)%30!=0) or ((players[0].rect.left-15)%30!=0):
			players[0].move(players[0].dir)
		else:
			for key in key_p1:
				if key_pressed[key]:
					players[0].move(key_p1[key])
					break
	if players[1]:
		if ((players[1].rect.top-15)%30!=0) or ((players[1].rect.left-15)%30!=0):
			players[1].move(players[1].dir)
		else:
			for key in key_p2:
				if key_pressed[key]:
					players[1].move(key_p2[key])
					break