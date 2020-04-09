import sys
import pygame
from settings import Settings
from bullet import Bullet
from f35 import F35
import sys
from time import sleep
"""
我们将首先把管理事件的代码移到一个名为check_events() 的函数中， 以简化run_game() 并隔离事件管理循环。 通过隔离事件循环， 可将事件管理与游戏的其他方面（如
更新屏幕） 分离。
将check_events() 放在一个名为game_functions 的模块中

分离管理事件

"""
def check_keydown_events(event,ai_settings,screen,ship,bullets):

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        # if len(bullets) < ai_settings.bullets_allowed:
        #     new_bullet = Bullet(ai_settings,screen,ship)
        #     bullets.add(new_bullet)

        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

#子弹数量控制
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        pygame.mixer.init()
        pygame.mixer.music.load("./sound/biu.mp3")
        pygame.mixer.music.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

#     new_bullet = Bullet(ai_settings,screen,ship)
#     bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,f35s,bullets):


    """响应鼠标和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
                #向右移动飞船
                # ship.rect.centerx += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,f35s,bullets,mouse_x,mouse_y)
def  check_play_button(ai_settings,screen,stats,sb,play_button,ship,f35s,bullets,mouse_x,mouse_y):
    """在玩家单机play按钮时开始新游戏"""
    button_clikced = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clikced and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息

        stats.reset_stats()
        stats.game_active = True
        #23:18 修改
        # fire_bullet(ai_settings, screen, ship, bullets)
        #重置记分牌图象
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        # sb.prep_dj()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        f35s.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,f35s)
        ship.center_ship()



def update_screen(ai_settings,screen,stats,sb,ship,f35s,bullets,play_button):
    """更新屏幕上的图像并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    f35s.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,f35s,bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #检查是否有子弹击中了外星人
    #如果是这样，就删除相应的子弹和外星人
    check_bullet_f35_collisions(ai_settings,screen,stats,sb,ship,f35s,bullets)

def check_bullet_f35_collisions(ai_settings,screen,stats,sb,ship,f35s,bullets):
    """响应子弹和外星人发生碰撞"""
    collisions = pygame.sprite.groupcollide(bullets,f35s,True,True)
    if collisions:
        for f35s in collisions.values():
            stats.score += ai_settings.f35_points * len(f35s)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(f35s) == 0:
        #删除现有的子弹并新建一群外星人
        #如果整群外形人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        # sb.prep_dj
        create_fleet(ai_settings,screen,ship,f35s)
def get_number__f35s_x(ai_settings,f35_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * f35_width
    number_f35s_x = int(available_space_x / (2 * f35_width))
    return number_f35s_x
def get_number_rows(ai_settings,ship_height,f35_height):
    available_space_y = (ai_settings.screen_height -
                         (3*f35_height)-ship_height)
    number_rows = int(available_space_y/(2*f35_height))
    return number_rows

def create_f35(ai_settings,screen,f35s,f35_number,row_number):
    """创建一个外星人并将其放到当前行"""

    f35 = F35(ai_settings, screen)
    f35_width = f35.rect.width
    f35.x = f35_width + 2 * f35_width * f35_number
    f35.rect.x = f35.x
    f35.rect.y = f35.rect.height + 2*f35.rect.height*row_number

    f35s.add(f35)

def create_fleet(ai_settings,screen,ship,f35s):
    """创建f35群"""
    #创建一个外星人，并计算一行可以容纳多少个外星人
    #外星人间距为外形人宽度
    f35 = F35(ai_settings,screen)
    number_f35s_x = get_number__f35s_x(ai_settings,f35.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,f35.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for f35_number in range(number_f35s_x):
            #创建一个外行人并将其加入当前行
            create_f35(ai_settings,screen,f35s,f35_number,
                       row_number)
def check_fleet_edges(ai_settings,f35s):
    """有外星人到达边缘时采取相应的措施"""
    for f35 in f35s.sprites():
        if f35.check_edges():
            change_fleet_direction(ai_settings,f35s)
            break
def change_fleet_direction(ai_settings,f35s):
    """将整群外星人下移，并改变它们的方向"""
    for f35 in f35s.sprites():
        f35.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_f35s_bottom(ai_settings,stats,sb,screen,ship,f35s,bullets):
    """检查是否有外星人到达了屏幕低端"""
    screen_rect = screen.get_rect()
    for f35 in f35s.sprites():
        if f35.rect.bottom >= screen_rect.bottom:
            #像飞船被撞倒一样处理
            ship_hit(ai_settings,stats,sb,screen,ship,f35s,bullets)
            break
def update_f35s(ai_settings,stats,sb,screen,ship,f35s,bullets):
    """

    检查是否有外星人位于屏幕边缘，
    更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,f35s)
    f35s.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,f35s):
        ship_hit(ai_settings,stats,sb,screen,ship,f35s,bullets)
    #检查是否有外星人到达屏幕底端
    check_f35s_bottom(ai_settings,stats,sb,screen,ship,f35s,bullets)
def ship_hit(ai_settings,stats,sb,screen,ship,f35s,bullets):
    """响应到外星人撞到飞船"""

    #将ships_left减1
    if stats.ship_left > 0 :
        stats.ship_left -= 1
        # 更新记分牌
        sb.prep_ships()

        #清空外星人和子弹列表
        f35s.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕中央
        print(stats.ship_left)
        create_fleet(ai_settings, screen, ship, f35s)
        ship.center_ship()

        #暂停
        sleep(0.5)

    else:
        stats.game_active =False
        pygame.mouse.set_visible(True)
def check_high_score(stats,sb):
    """检查是否诞生了新的最高得分"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()




