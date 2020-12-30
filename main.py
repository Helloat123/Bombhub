from player import *
from mapediter import *
from bomb import *
from properties_panel import PropertiesPanel
from button import *
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600


# 初始化 pygame
pygame.init()
# 游戏界面像素大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 游戏界面标题
pygame.display.set_caption('SuperBomb')

# 测试音乐
music_pleayer = MusicPlayer(pygame.mixer)
music_pleayer.play_music()

# 暂停按钮
btn_pause = Button('resources/image/btn_pause.png',
                   (730, 560), screen, PAUSE, True)
# 继续按钮
btn_continue = Button('resources/image/resume.png',
                      (210, 160), screen, CONTINUE, False)
# 重新开始
btn_restart = Button('resources/image/restart.png',
                     (210, 260), screen, RESTART, False)
# 回到主菜单
btn_backmenu = Button('resources/image/exit.png',
                      (210, 360), screen, BACKMENU, False)

# 开始游戏
btn_start = Button('resources/image/play.png', (180, 460), screen, START, True)
# 帮助
btn_help = Button('resources/image/help.png', (410, 460), screen, HELP, True)


is_pause = False
is_start = True
is_restart = False
need_show_help = False
need_show_close = False
players = []
bombs = None
(x, y, w) = PropertiesPanel.showHelp(screen)
clock = pygame.time.Clock()
clock.tick(60)
while True:
    # 暂停后事件处理就停止，但必须到里面的pygame.key.get_pressed()之后再停止，否则会卡死
    handle_event(players, bombs, is_pause, is_start)
    if is_start or is_restart:

        background = pygame.image.load(
            'resources/image/start_panel.png').convert()
        screen.blit(background, (0, 0))
        # 主界面LOGO
        logo = pygame.image.load('resources/image/logo1.png').convert()
        screen.blit(logo, (90, 30))
        if is_restart or btn_start.render():
            is_start = False
            if is_restart:
                is_restart = False
            is_pause = False
            need_show_help = False
            need_show_close = False
            background = pygame.image.load(
                'resources/image/background.png').convert()
            PropertiesPanel.draw_items(screen)
            mymap = MapEditer.instance()
            mymap.empty()
            mymap.BuildMap(screen)
            blocks = mymap.GetBlocks()
            bombs = pygame.sprite.Group()
            player1, player2, players = Player.playerInit(screen, blocks)

        if not is_restart:
            if btn_help.render():
                btn_close = Button('resources/image/btn_close.png',
                                   (x + w, y), screen, CLOSE, True)
                need_show_close = True
                need_show_help = True
        if need_show_close:
            if btn_close.render():
                need_show_help = False
                need_show_close = False
            else:
                need_show_help = True
        if need_show_help:
            PropertiesPanel.showHelp(screen)

    else:
        screen.blit(background, (0, 0))
        blocks.draw(screen)
        if not is_pause:
            bombs.update(bombs)
        bombs.draw(screen)
        for player in players:
            if player:
                player.show()
        is_pause, is_start, is_restart = Button.btn_deal(screen=screen, is_pause=is_pause, btn_pause=btn_pause,
                                                         btn_continue=btn_continue, btn_backmenu=btn_backmenu, btn_restart=btn_restart)
        if len(players) == 1:
            is_start = True
            if players[0].id == 1:
                screen.blit(pygame.image.load(
                    'resources/image/player1_win.png').convert_alpha(), (100, 60))
            else:
                screen.blit(pygame.image.load(
                    'resources/image/player2_win.png').convert_alpha(), (100, 60))
            pygame.display.flip()
            time.sleep(2)
    pygame.display.flip()
