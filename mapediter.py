import pygame
import random

BOMB = 1
BARRIER = 2
BOX = 3
FIRE = 4
TOOL_SPEED_UP = 5
TOOL_SCOPE_UP = 6
TOOL_BOMBS_UP = 7
TOOL_HP_UP = 8
TOOL = [TOOL_SPEED_UP, TOOL_SCOPE_UP, TOOL_BOMBS_UP, TOOL_HP_UP]


class Block(pygame.sprite.Sprite):

    def __init__(self, block_img, init_pos, category):
        pygame.sprite.Sprite.__init__(self)
        self.image = block_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.category = category


class Box(Block):

    def __init__(self, box_img, init_pos, has_tool):
        super(Box, self).__init__(box_img, init_pos, BOX)
        self.pos = init_pos
        self._has_tool = has_tool


class MapEditer(object):
    """docstring for MapEditer"""
    _instance = None

    def __init__(self):
        self.blocks = pygame.sprite.Group()
        self.blocks.empty()

    @staticmethod
    def instance():
        if MapEditer._instance is None:
            MapEditer._instance = MapEditer()
        return MapEditer._instance

    @staticmethod
    def to_map_coordinate(xy):
        return (15 + 30 * (xy[0] - 1), 15 + 30 * (xy[1] - 1))

    @staticmethod
    def to_real_coordinate(cor):
        return ((cor[0] - 15) // 30 + 1, (cor[1] - 15) // 30 + 1)

    @staticmethod
    def Paste(pair, img, category):
        col, row = MapEditer.to_map_coordinate(pair)
        block_img = pygame.image.load(img)
        if category == BOX:
            block = Box(block_img, (col, row), img.endswith("box0.png")
                        or img.endswith("box3.png") and random.random() > 0.5)
        else:
            block = Block(block_img, (col, row), category)
        return block

    def refresh(self):
        self.blocks.draw(self.screen)

    def empty(self):
        self.blocks.empty()

    def BuildMap(self, screen):
        self.screen = screen

        # 不能生成箱子的地方
        corner = [(1, 1), (1, 2), (2, 1), (1, 19), (1, 18), (2, 19),
                  (18, 1), (19, 1), (19, 2), (19, 19), (18, 19), (19, 18)]
        # 四个区域的边界
        border = [(1, 10), (1, 11), (10, 20), (1, 11),
                  (1, 10), (11, 20), (10, 20), (11, 20)]
        # 箱子的坐标列表
        boxs = []
        barriers = []
        random.seed()

        # 随机产生宝箱位置
        total = 0
        index = 0

        while index < 7:
            for col in range(border[index][0], border[index][1]):
                num = 3 if col % 2 != 0 else 2
                increament = 1 if col % 2 != 0 else 2
                total = 0
                while total < num:
                    row = random.randrange(
                        border[index + 1][0], border[index + 1][1], increament)
                    if (col, row) not in boxs and (col, row) not in corner:
                        boxs.append((col, row))
                        total += 1
            index += 2

        # block = self.Paste((3, 1), "resources/image/box" +
        #                    str(random.randint(0, 3)) + ".png", BOX)
        # print('box ', ((block.rect.top - 15) / 30 +
        #                1, (block.rect.left - 15) / 30 + 1))
        # self.blocks.add(block)
        # 放置宝箱
        for pair in boxs:
            block = self.Paste(pair, "resources/image/box" +
                               str(random.randint(0, 3)) + ".png", BOX)
            self.blocks.add(block)

        for col in range(2, 19, 4):
            for row in range(2, 19, 4):
                barriers.append((col, row))

        for pair in barriers:
            block = self.Paste(pair, "resources/image/barrier.png", BARRIER)
            self.blocks.add(block)
        self.refresh()

    def GetBlocks(self):
        return self.blocks
