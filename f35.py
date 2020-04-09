import pygame
from pygame.sprite import Sprite
class F35(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化外星人并设置初始位置"""
        super(F35,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #加载外星人图像，并设置rect属性
        self.image = pygame.image.load('images/f35.jpg')
        self.rect = self.image.get_rect()
        #每个f35最初在屏幕在左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height


        #存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    def update(self):
        """向左或向右移动f35"""
        self.x += (self.ai_settings.f35_speed_factor *
                    self.ai_settings.fleet_direction)
        self.rect.x = self.x
