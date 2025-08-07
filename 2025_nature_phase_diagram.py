# High-field superconducting halo in UTe2: https://www.science.org/doi/10.1126/science.adn7673

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.optimize import fsolve

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# 定义角度范围
theta = np.linspace(-20, 20, 100)

# 定义相边界曲线函数
def upper_boundary(theta):
    """上边界 - FP/SC相边界"""
    return 40 + 0.1 * theta**2

def lower_left_boundary(theta):
    """下左边界"""
    return 52 + 7 * np.cos(np.pi * theta / 20) + 0.3 * theta

def lower_right_boundary(theta):
    """下右边界"""
    return 52 + 7 * np.cos(np.pi * theta / 20) - 0.3 * theta

def middle_left_peak(theta):
    """左侧峰"""
    center = -12
    width = 4
    height = 59
    base = 52
    return base + (height - base) * np.exp(-0.5 * ((theta - center) / width)**2)

def middle_right_peak(theta):
    """右侧峰"""
    center = 12
    width = 4
    height = 59
    base = 52
    return base + (height - base) * np.exp(-0.5 * ((theta - center) / width)**2)

# 生成边界点
theta_fine = np.linspace(-20, 20, 200)
upper_curve = upper_boundary(theta_fine)

# 生成下边界（包含两个峰）
lower_curve = np.maximum(
    np.maximum(lower_left_boundary(theta_fine), lower_right_boundary(theta_fine)),
    np.maximum(middle_left_peak(theta_fine), middle_right_peak(theta_fine))
)

# 计算上下边界的交点
def find_intersections(x_range, upper_func, lower_func, num_points=1000):
    """找到两条曲线的所有交点"""
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    intersections = []
    
    # 检查函数值差异的符号变化
    diffs = upper_func(x_vals) - lower_func(x_vals)
    sign_changes = np.where(np.diff(np.sign(diffs)))[0]
    
    # 对每个符号变化区间求解交点
    for i in sign_changes:
        x_left = x_vals[i]
        x_right = x_vals[i+1]
        
        # 定义求解函数：upper(x) - lower(x) = 0
        def equation(x):
            return upper_func(x) - lower_func(x)
        
        # 使用fsolve求解
        x_sol = fsolve(equation, (x_left + x_right) / 2)[0]
        
        # 检查解是否在区间内
        if x_left <= x_sol <= x_right:
            y_sol = upper_func(x_sol)
            intersections.append((x_sol, y_sol))
    
    return np.array(intersections)

# 寻找交点
intersections = find_intersections([-20, 20], upper_boundary, 
                                   lambda x: np.maximum(
                                       np.maximum(lower_left_boundary(x), lower_right_boundary(x)),
                                       np.maximum(middle_left_peak(x), middle_right_peak(x))
                                   ))

# 按x坐标排序交点
if len(intersections) > 0:
    intersections = intersections[np.argsort(intersections[:, 0])]
    print("找到的交点：")
    for i, (x, y) in enumerate(intersections):
        print(f"交点 {i+1}: θ = {x:.2f}°, t = {y:.2f}°C")
else:
    print("未找到交点")

# 创建填充区域
# FP区域 (红色/粉色区域)
ymax = max(upper_curve)
fp_vertices = list(zip(theta_fine, upper_curve)) + [(20, ymax), (-20, ymax)]
fp_polygon = Polygon(fp_vertices, facecolor='#FF6B7A', alpha=0.8, edgecolor='none')
ax.add_patch(fp_polygon)

# SC区域 (蓝色区域)
# sc_vertices = list(zip(theta_fine, lower_curve)) + [(20, 30), (-20, 30)]
# sc_polygon = Polygon(sc_vertices, facecolor='#4A90E2', alpha=0.8, edgecolor='none')
# ax.add_patch(sc_polygon)

# 绘制重叠区域（如果有交点）
if len(intersections) >= 2:
    # 创建重叠区域的顶点列表
    overlap_vertices = []
    
    # 从第一个交点到最后一个交点，添加上边界点
    mask = (theta_fine >= intersections[0, 0]) & (theta_fine <= intersections[-1, 0])
    overlap_vertices.extend(zip(theta_fine[mask], upper_curve[mask]))
    
    # 从最后一个交点到第一个交点，添加下边界点（反向）
    overlap_vertices.extend(reversed(list(zip(theta_fine[mask], lower_curve[mask]))))
    
    # 创建重叠区域多边形
    overlap_polygon = Polygon(overlap_vertices, facecolor='#9B59B6', alpha=0.6, 
                             edgecolor='black', linewidth=2)
    ax.add_patch(overlap_polygon)
    
    # 标记交点
    ax.scatter(intersections[:, 0], intersections[:, 1], c='black', s=100, 
               zorder=10, label='Intersections')
    ax.legend()

# 绘制相边界线上的数据点
theta_points = np.linspace(-13.59, 13.59, 30)
upper_points = upper_boundary(theta_points)
# lower_points = np.maximum(
#     np.maximum(lower_left_boundary(theta_points), lower_right_boundary(theta_points)),
#     np.maximum(middle_left_peak(theta_points), middle_right_peak(theta_points))
# )

lower_points = np.maximum(
    np.maximum(lower_left_boundary(theta_points), lower_right_boundary(theta_points)),
    np.maximum(middle_left_peak(theta_points), middle_right_peak(theta_points))
)

# 绘制上边界的数据点
ax.scatter(theta_points, upper_points, c='darkblue', s=30, alpha=0.8, zorder=5)
ax.scatter(theta_points[::2], upper_points[::2], c='lightblue', s=25, alpha=0.9, zorder=6)

# 绘制下边界的数据点
ax.scatter(theta_points, lower_points, c='darkblue', s=30, alpha=0.8, zorder=5)
ax.scatter(theta_points[::2], lower_points[::2], c='lightgray', s=25, alpha=0.9, zorder=6)

# 添加相态标签
ax.text(0, 65, 'FP', fontsize=20, fontweight='bold', ha='center', va='center')
ax.text(0, 45, 'SC', fontsize=20, fontweight='bold', ha='center', va='center', color='white')

# 添加左下角的参数标签
ax.text(-18, 37, r'$\theta_{bc} = 30°$', fontsize=12, fontweight='bold')
ax.text(-18, 35, 'P1', fontsize=12, fontweight='bold')

# 设置坐标轴
ax.set_xlim(-20, 20)
ax.set_ylim(30, 75)
ax.set_xlabel(r'$\theta_a$ (°)', fontsize=14)
ax.set_ylabel(r'$t_{LC}$ (°C)', fontsize=14)

# 添加网格
ax.grid(True, alpha=0.3)

# 设置刻度
ax.set_xticks(np.arange(-20, 21, 5))
ax.set_yticks(np.arange(30, 76, 5))

# 设置图形边框
ax.spines['top'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

plt.tight_layout()
plt.savefig('phase_diagram_with_intersections.png', dpi=300)
plt.savefig('phase_diagram_with_intersections.svg', dpi=300)
plt.savefig('phase_diagram_with_intersections.pdf', dpi=300)
plt.show()

# 保存交点数据
if len(intersections) > 0:
    np.savetxt('intersection_points.csv', intersections, 
               header='theta_a,temperature', 
               delimiter=',', fmt='%.4f')
    print("\n交点数据已保存到 'intersection_points.csv' 文件")
