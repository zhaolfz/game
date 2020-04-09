import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from f35 import F35
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_gam():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')

    #创建play按钮
    play_button = Button(ai_settings,screen,'Play')





    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个f35编组
    f35s = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,f35s)
    #创建一个计分版，用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

#开始游戏主循环
    while True:

        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,f35s,bullets)
        # for enent in pygame.event.get():
        #     if enent.type == pygame.QUIT:
        #         sys.exit()
        #按按键方向更新飞船位置
        if stats.game_active:
            ship.update()

        # gf.create_fleet(ai_settings,screen,ship,f35s)
        #删除已消失的子弹
            gf.update_bullets(ai_settings,screen,stats,sb,ship,f35s,bullets)
        # #删除已消失的子弹
        # for bullet in bullets.copy():
        #     if bullet.rect.bottom <=0:
        #         bullets.remove(bullet)

        #每次循环时都重绘屏幕

            gf.update_f35s(ai_settings,stats,sb,screen,ship,f35s,bullets)


        gf.update_screen(ai_settings,screen,stats,sb,ship,f35s,bullets,play_button)
        #让最近绘制的屏幕可见




run_gam()

