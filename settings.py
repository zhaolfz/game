class Settings():
    """存储外星人入侵的所有设置的类"""

    def __init__(self):

        #初始化游戏设置
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (118,153,253)
        #飞船的设置

        self.ship_limit = 3
        #子弹设置

        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5
        #外星人设置


        self.fleet_drop_speed = 10
        #fleet_direction 为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        # 'skyblue3': (108, 166, 205, 255),
        # 'skyblue2': (126, 192, 238, 255)
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.f35_speed_factor = 2
        #fleet_direction为1表示向右；为-1表示向左
        #fleet_direction = 1

        #计分
        self.f35_points = 50
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.f35_speed_factor *= self.speedup_scale

        self.f35_points = int(self.f35_points * self.score_scale)
        print(self.f35_points)