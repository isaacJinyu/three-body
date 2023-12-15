# 导入pygame库
import pygame
import numpy as np
# 初始化pygame
pygame.init()
# 设置窗口大小和标题
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Three-body problem')
# 设置时钟
clock = pygame.time.Clock()
# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
# 设置字体
font = pygame.font.SysFont('Arial', 32)
# 定义万有引力常数
G = 6.6743e-11 # m^3 kg^-1 s^-2
# 定义缩放比例
scale = 5e10 # m/px
# 定义星体类
class Star:
    def __init__(self, m, r, v, color):
        self.m = m # 质量
        self.r = r # 位置
        self.v = v # 速度
        self.color = color # 颜色
        self.trail = [] # 轨迹
        self.max_trail = 100 # 最大轨迹长度
    def update(self, dt):
        # 更新位置
        self.r += self.v * dt
        # 添加轨迹点
        self.trail.append(self.r.copy())
        # 限制轨迹长度
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
    def draw(self):
        # 绘制星体
        pygame.draw.circle(screen, self.color, (self.r[0] / scale + 400, self.r[1] / scale + 300), 5)
        # 绘制轨迹
        for i in range(len(self.trail) - 1):
            pygame.draw.line(screen, self.color, (self.trail[i][0] / scale + 400, self.trail[i][1] / scale + 300), (self.trail[i+1][0] / scale + 400, self.trail[i+1][1] / scale + 300))
    def apply_force(self, f):
        # 应用力，计算加速度
        a = f / self.m
        # 更新速度
        self.v += a * dt
# 创建三个星体对象
star1 = Star(2e30, np.array([1.0, 0.0, 0.0]) * 1.5e11, np.array([0.0, 1.0, 0.0]) * 3e4, red)
star2 = Star(2e30, np.array([-0.5, np.sqrt(3)/2, 0.0]) * 1.5e11, np.array([-np.sqrt(3)/2, -0.5, 0.0]) * 3e4, blue)
star3 = Star(2e30, np.array([-0.5, -np.sqrt(3)/2, 0.0]) * 1.5e11, np.array([np.sqrt(3)/2, -0.5, 0.0]) * 3e4, green)
# 定义一个函数，计算两个星体之间的引力
def gravity(s1, s2):
    # 计算相对位置和距离
    r = s2.r - s1.r
    d = np.linalg.norm(r)
    # 计算引力
    f = G * s1.m * s2.m * r / d**3
    # 返回结果
    return f
# 定义一个函数，计算所有星体之间的引力，并更新速度和位置
def update_system(dt):
    # 计算星体1和星体2之间的引力
    f12 = gravity(star1, star2)
    # 计算星体1和星体3之间的引力
    f13 = gravity(star1, star3)
    # 计算星体2和星体3之间的引力
    f23 = gravity(star2, star3)
    # 应用引力，更新速度和位置
    star1.apply_force(f12 + f13)
    star2.apply_force(-f12 + f23)
    star3.apply_force(-f13 - f23)
    star1.update(dt)
    star2.update(dt)
    star3.update(dt)
# 定义一个函数，绘制所有星体和文字
def draw_system():
    # 填充背景色
    screen.fill(black)
    # 绘制星体
    star1.draw()
    star2.draw()
    star3.draw()
    # 绘制文字
    text = font.render('Press WASD to control star 1', True, white)
    screen.blit(text, (10, 10))
    # 更新屏幕
    pygame.display.flip()
# 定义一个函数，处理键盘事件
def handle_key(event):
    # 定义键盘控制的加速度
    acc = 5e-3 # m/s^2
    # 判断按下的键
    if event.key == pygame.K_w:
        # 按下W键，给星体1施加向上的加速度
        star1.apply_force(np.array([0.0, -acc, 0.0]) * star1.m)
    elif event.key == pygame.K_s:
        # 按下S键，给星体1施加向下的加速度
        star1.apply_force(np.array([0.0, acc, 0.0]) * star1.m)
    elif event.key == pygame.K_a:
        # 按下A键，给星体1施加向左的加速度
        star1.apply_force(np.array([-acc, 0.0, 0.0]) * star1.m)
    elif event.key == pygame.K_d:
        # 按下D键，给星体1施加向右的加速度
        star1.apply_force(np.array([acc, 0.0, 0.0]) * star1.m)
    elif event.key == pygame.K_i:
        # 按下I键，给星体1施加向前的加速度
        star1.apply_force(np.array([0.0, 0.0, acc]) * star1.m)
    elif event.key == pygame.K_k:
        # 按下K键，给星体1施加向后的加速度
        star1.apply_force(np.array([0.0, 0.0, -acc]) * star1.m)
# 定义一个循环，主要逻辑
running = True
while running:
    # 设置时间步长
    dt = clock.tick(60)*1e5 # s
    # 处理事件
    for event in pygame.event.get():
        # 判断事件类型
        if event.type == pygame.QUIT:
            # 点击关闭按钮，退出循环
            running = False
        elif event.type == pygame.KEYDOWN:
            # 按下键盘，处理键盘事件
            handle_key(event)
    # 更新系统
    update_system(dt)
    # 绘制系统
    draw_system()
# 退出pygame
pygame.quit()
