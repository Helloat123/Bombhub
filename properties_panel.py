import pygame


class PropertiesPanel():

    def __init__(self):
        pass

    @staticmethod
    def build_text(content):
        my_font = pygame.font.SysFont("fangsong", 25)
        return my_font.render(content, True, (0, 0, 0))

    @staticmethod
    def draw_panel(screen, player_id, HP, speed, scope, bombs):
        text_surfaces = []
        text_surfaces.append(PropertiesPanel.build_text(str(HP)))
        text_surfaces.append(PropertiesPanel.build_text(str(speed)))
        text_surfaces.append(PropertiesPanel.build_text(str(scope)))
        text_surfaces.append(PropertiesPanel.build_text(str(bombs)))
        y = 70 if player_id == 1 else 350
        screen.blit(pygame.image.load(
            'resources/image/numback_2.png').convert_alpha(), (730, y))
        for i in range(len(text_surfaces)):
            screen.blit(text_surfaces[i], (735, y))
            y += 57
        pygame.display.flip()

    @staticmethod
    def draw_items(screen):
        # pictures = ['resources/image/tool3.png', 'resources/image/tool0.png',
        #             'resources/image/bomb_center.png', 'resources/image/bomb.png']
        # 画框
        screen.blit(pygame.image.load(
            'resources/image/state.png').convert_alpha(), (600, 0))
        # screen.blit(pygame.image.load(
        #     'resources/image/kuang.png').convert_alpha(), (600, 300))

        # # 玩家logo
        # screen.blit(pygame.image.load(
        #     'resources/image/player1_down.png').convert_alpha(), (660, 20))
        # screen.blit(pygame.image.load(
        #     'resources/image/player2_down.png').convert_alpha(), (660, 320))

        # # 属性logo
        # y = 80
        # for i in pictures:
        #     screen.blit(pygame.image.load(i).convert_alpha(), (640, y))
        #     y += 40

        # y = 380
        # for i in pictures:
        #     screen.blit(pygame.image.load(i).convert_alpha(), (640, y))
        #     y += 40

    @staticmethod
    def showHelp(screen):
        tips_board = pygame.image.load('resources/image/tips_boardhelp2.png')
        x, y = (80, 260)
        screen.blit(tips_board, (x, y))
        # 关闭帮助面板
        w, h = tips_board.get_size()
        first_y = 20
        screen.blit(PropertiesPanel.build_text(
            'Instruction'), (x + 230, y + first_y))
        screen.blit(PropertiesPanel.build_text(
            'Player1:'), (x + 30, y + first_y + 30))
        screen.blit(PropertiesPanel.build_text(
            'W:up A:left S:down D:right Space:bomb'), (x + 30, y + first_y + 30 + 30))
        screen.blit(PropertiesPanel.build_text(
            'Player2:'), (x + 30, y + first_y + 30 + 30 + 30))
        screen.blit(PropertiesPanel.build_text(
            '↑:up ←:left ↓:down →:right Num0:bomb'), (x + 30, y + first_y + 30 + 30 + 30 + 30))
        screen.blit(PropertiesPanel.build_text(
            'Developers(Ordered by Pinin):'), (x + 30, y + first_y + 30 + 30 + 30 + 30 + 60))
        screen.blit(PropertiesPanel.build_text(
            '刘子琦 杨曜铭 张天麟 朱睿诚'), (x + 30, y + first_y + 30 + 30 + 30 + 30 + 60 + 30))
        return x, y, w
