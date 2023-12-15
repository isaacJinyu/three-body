# 导入numpy和matplotlib库
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import matplotlib
matplotlib.use('TkAgg')

# 定义万有引力常数
G = 6.6743e-11 # m^3 kg^-1 s^-2

# 参考《三体》中的设定，假设三颗星的质量相等，初始位置在一个正三角形的顶点，初始速度垂直于位置矢量
m1 = m2 = m3 = 2e30 # kg
r1 = np.array([1.0, 0.0, 0.0]) * 1.5e11 # m
r2 = np.array([-0.5, np.sqrt(3)/2, 0.0]) * 1.5e11 # m
r3 = np.array([-0.5, -np.sqrt(3)/2, 0.0]) * 1.5e11 # m
v1 = np.array([0.0, 1.02, 0.05]) * 3e4 # m/s
v2 = np.array([-np.sqrt(3)/2, -0.5, 0.0]) * 3e4 # m/s
v3 = np.array([np.sqrt(3)/2, -0.5, 0.0]) * 3e4 # m/s

# 定义模拟的时间参数
t_start = 0 # s
t_end = 3e10 # s
dt = 1e5 # s
t = np.arange(t_start, t_end, dt) # 时间数组
n = len(t) # 时间步数

# 定义一个函数，根据当前的位置和速度，计算下一时刻的位置和速度
def update_system(r1, r2, r3, v1, v2, v3, dt):
    # 计算三颗星之间的相对位置和距离
    r12 = r2 - r1
    r13 = r3 - r1
    r23 = r3 - r2
    d12 = np.linalg.norm(r12)
    d13 = np.linalg.norm(r13)
    d23 = np.linalg.norm(r23)
    # 计算三颗星之间的引力
    f12 = G * m1 * m2 * r12 / d12**3
    f13 = G * m1 * m3 * r13 / d13**3
    f23 = G * m2 * m3 * r23 / d23**3
    # 计算三颗星的加速度
    a1 = (f12 + f13) / m1
    a2 = (-f12 + f23) / m2
    a3 = (-f13 - f23) / m3
    # 计算下一时刻的速度
    v1_next = v1 + a1 * dt
    v2_next = v2 + a2 * dt
    v3_next = v3 + a3 * dt
    # 计算下一时刻的位置
    r1_next = r1 + v1_next * dt
    r2_next = r2 + v2_next * dt
    r3_next = r3 + v3_next * dt
    # 返回结果
    return r1_next, r2_next, r3_next, v1_next, v2_next, v3_next

# 定义一个数组，用来存储每一时刻的位置和速度
r = np.zeros((n, 3, 3)) # 第一维是时间，第二维是星体，第三维是坐标
r[0, 0, :] = r1
r[0, 1, :] = r2
r[0, 2, :] = r3

# 循环计算每一时刻的位置和速度
for i in range(n-1):
    # 使用返回值来更新位置和速度
    r1, r2, r3, v1, v2, v3 = update_system(r1, r2, r3, v1, v2, v3, dt)
    r[i+1, 0, :] = r1
    r[i+1, 1, :] = r2
    r[i+1, 2, :] = r3

# 绘制三维动画
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# 去掉坐标轴
ax.set_axis_off()
# 设置坐标轴比例
ax.set_box_aspect((1, 1, 1))
ax.set_xlim(-1e12, 1e12)
ax.set_ylim(-1e12, 1e12)
ax.set_zlim(-1e12, 1e12)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Three-body problem')
line1, = ax.plot([], [], [], 'r-')
line2, = ax.plot([], [], [], 'b-')
line3, = ax.plot([], [], [], 'g-')
point1, = ax.plot([], [], [], 'ro')
point2, = ax.plot([], [], [], 'bo')
point3, = ax.plot([], [], [], 'go')


def animate(i):
    line1.set_data(r[:i+1, 0, 0], r[:i+1, 0, 1])
    line1.set_3d_properties(r[:i+1, 0, 2])
    line2.set_data(r[:i+1, 1, 0], r[:i+1, 1, 1])
    line2.set_3d_properties(r[:i+1, 1, 2])
    line3.set_data(r[:i+1, 2, 0], r[:i+1, 2, 1])
    line3.set_3d_properties(r[:i+1, 2, 2])
    point1.set_data([r[i, 0, 0]], [r[i, 0, 1]])
    point1.set_3d_properties([r[i, 0, 2]])
    point2.set_data([r[i, 1, 0]], [r[i, 1, 1]])
    point2.set_3d_properties([r[i, 1, 2]])
    point3.set_data([r[i, 2, 0]], [r[i, 2, 1]])
    point3.set_3d_properties([r[i, 2, 2]])



    # 返回结果
    return line1, line2, line3, point1, point2, point3

anim = animation.FuncAnimation(fig, animate, frames=n, interval=0.5)
plt.show()
