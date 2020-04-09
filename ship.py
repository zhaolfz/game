import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化飞船并设置初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/J20.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx#要将游戏元素居中， 可设置相应rect 对象的属性center 、 centerx 或centery
        self.rect.bottom = self.screen_rect.bottom #要让游戏元素与屏幕边缘对齐， 可使用属性top 、 bottom 、 left 或right

        #在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        #允许不断移动
        self.moving_right = False
        self.moving_left = False
    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船的center值，而不是rect

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0:
            self.center -= self.ai_settings.ship_speed_factor
        #根据self.centerx更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
    def center_ship(self):

        self.blitme()