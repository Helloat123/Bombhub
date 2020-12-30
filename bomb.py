from mapediter import *
import time
import pygame


class Bomb(Block):
    """docstring for Bomb"""

    def __init__(self, init_pos):
        Block.__init__(self, pygame.image.load('resources/image/bomb.png'),
                       (15 + 30 * (init_pos[0] - 1), 15 + 30 * (init_pos[1] - 1)), BOMB)
        self.scope = 0
        self.fire_list = pygame.sprite.Group()
        self.has_bomb = False
        self.current_time = 0

    def setHost(self, host):
        self.host = host

    def setScope(self, scope):
        self.scope = scope

    def setPlayers(self, players):
        self.players = players

    def bombed(self):
        self.image = pygame.image.load('resources/image/bomb_center.png')
        self.has_bomb = True
        self.onCenter()
        self.onRight()
        self.onDown()
        self.onUp()
        self.onLeft()

    def hasPlayer(self, pos, player):
        col = player.rect.left // 30 + 1
        row = player.rect.top // 30 + 1
        col, row = 15 + 30 * (col - 1), 15 + 30 * (row - 1)
        if (col, row) == pos:
            return True
        else:
            return None

    def hasBox(self, pos):
        for block in self.host.blocks:
            if block.category != BOMB and block.rect.topleft == pos:
                return block  # 障碍物或箱子
        return None  # 空气

    def generateTool(self, obj):
        if obj._has_tool:
            mymap = MapEditer.instance()
            pos = MapEditer.to_real_coordinate(obj.pos)
            num = random.randint(0, 3)
            tmp = MapEditer.Paste(
                pos, "resources/image/tool" + str(num) + ".png", TOOL[num])
            mymap.blocks.add(tmp)
            mymap.refresh()

    def onCenter(self):
        pos = (self.rect.left, self.rect.top)
        for i in range(len(self.players)):
            if self.players[i] and self.hasPlayer(pos, self.players[i]):
                if self.players[i].HP_reduce():
                    self.players.remove(self.players[i])
                    break

    def onRight(self):
        for x in range(1, self.scope + 1):
            pos = (self.rect.left + x * 30, self.rect.top)
            obj = self.hasBox(pos)

            for i in range(len(self.players)):
                if self.players[i] and self.hasPlayer(pos, self.players[i]):
                    if self.players[i].HP_reduce():
                        self.players.remove(self.players[i])
                        break

            if obj is None:
                if pos[0] <= 570:
                    if x == self.scope:
                        block_img = pygame.image.load(
                            "resources/image/bomb_right.png")
                    else:
                        block_img = pygame.image.load(
                            "resources/image/bomb_x.png")
                    fire = Block(block_img, pos, FIRE)
                    self.fire_list.add(fire)
            elif obj.category == BOX:
                self.generateTool(obj)
                self.host.blocks.remove(obj)
                return
            elif obj.category == BARRIER:
                return

    def onDown(self):
        for x in range(1, self.scope + 1):
            pos = (self.rect.left, self.rect.top + x * 30)
            obj = self.hasBox(pos)

            for i in range(len(self.players)):
                if self.players[i] and self.hasPlayer(pos, self.players[i]):
                    if self.players[i].HP_reduce():
                        self.players.remove(self.players[i])
                        break

            if obj is None:
                if pos[1] <= 570:
                    if x == self.scope:
                        block_img = pygame.image.load(
                            "resources/image/bomb_down.png")
                    else:
                        block_img = pygame.image.load(
                            "resources/image/bomb_y.png")
                    fire = Block(block_img, pos, FIRE)
                    self.fire_list.add(fire)
            elif obj.category == BOX:
                self.generateTool(obj)
                self.host.blocks.remove(obj)
                return
            elif obj.category == BARRIER:
                return

    def onUp(self):
        for x in range(1, self.scope + 1):
            pos = (self.rect.left, self.rect.top - x * 30)
            obj = self.hasBox(pos)

            for i in range(len(self.players)):
                if self.players[i] and self.hasPlayer(pos, self.players[i]):
                    if self.players[i].HP_reduce():
                        self.players.remove(self.players[i])
                        break

            if obj is None:
                if pos[1] >= 0:
                    if x == self.scope:
                        block_img = pygame.image.load(
                            "resources/image/bomb_up.png")
                    else:
                        block_img = pygame.image.load(
                            "resources/image/bomb_y.png")
                    fire = Block(block_img, pos, FIRE)
                    self.fire_list.add(fire)
            elif obj.category == BOX:
                self.generateTool(obj)
                self.host.blocks.remove(obj)
                return
            elif obj.category == BARRIER:
                return

    def onLeft(self):
        for x in range(1, self.scope + 1):
            pos = (self.rect.left - x * 30, self.rect.top)
            obj = self.hasBox(pos)

            for i in range(len(self.players)):
                if self.players[i] and self.hasPlayer(pos, self.players[i]):
                    if self.players[i].HP_reduce():
                        self.players.remove(self.players[i])
                        break

            if obj is None:
                if pos[0] >= 0:
                    if x == self.scope:
                        block_img = pygame.image.load(
                            "resources/image/bomb_left.png")
                    else:
                        block_img = pygame.image.load(
                            "resources/image/bomb_x.png")
                    fire = Block(block_img, pos, FIRE)
                    self.fire_list.add(fire)
            elif obj.category == BOX:
                self.generateTool(obj)
                self.host.blocks.remove(obj)
                return
            elif obj.category == BARRIER:
                return

    def update(self, bombs):
        self.current_time += 0.01
        if self.current_time >= 6 and self.current_time <= 6.2:
            if self.has_bomb is False:
                self.bombed()
        elif self.current_time > 6 and self.current_time < 7:
            self.fire_list.draw(self.host.screen)
        elif self.current_time >= 7:
            bombs.remove(self)
            self.host.recover()
