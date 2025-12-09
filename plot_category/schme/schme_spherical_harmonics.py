"""
Spherical Harmonics Visualization - Matching Reference Image Style
球谐函数可视化 - 匹配参考图片样式
"""

import numpy as np
from scipy.special import sph_harm
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

def plot_spherical_harmonic(ax, l, m, resolution=80):
    """
    在给定的axes上绘制单个球谐函数
    """
    # 创建角度网格
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2*np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    
    # 计算球谐函数
    Y = sph_harm(m, l, phi, theta)
    
    # 转换为实球谐函数
    if m > 0:
        Y_real = np.sqrt(2) * (-1)**m * np.real(Y)
    elif m < 0:
        Y_real = np.sqrt(2) * (-1)**m * np.imag(Y)
    else:
        Y_real = np.real(Y)
    
    # 半径 = |Y_real|
    r = np.abs(Y_real)
    
    # 转换为笛卡尔坐标
    X = r * np.sin(theta) * np.cos(phi)
    Y_coord = r * np.sin(theta) * np.sin(phi)
    Z = r * np.cos(theta)
    
    # 创建颜色数组
    colors = np.empty(Y_real.shape + (4,))
    positive = Y_real >= 0
    
    # 橙红色（正值）和蓝色（负值）- 匹配参考图片配色
    colors[positive] = [0.90, 0.40, 0.30, 1.0]   # 橙红
    colors[~positive] = [0.30, 0.45, 0.90, 1.0]  # 蓝色
    
    # 绘制3D表面
    ls = LightSource(azdeg=315, altdeg=45)
    ax.plot_surface(X, Y_coord, Z, facecolors=colors,
                   rstride=1, cstride=1,
                   antialiased=True, shade=True, lightsource=ls)
    
    # 设置坐标范围
    max_range = max(np.max(np.abs(X)), np.max(np.abs(Y_coord)), 
                   np.max(np.abs(Z)), 0.3) * 1.2
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # 隐藏坐标轴
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    

def create_grid_visualization():
    """
    创建6行x7列的网格图 - 匹配参考图片布局
    """
    l_max = 5
    n_rows = l_max + 1  # 6行 (l = 0 to 5)
    n_cols = 2 * l_max + 1  # 11列 (m = -5 to 5)
    
    fig = plt.figure(figsize=(20, 12), facecolor='white')
    
    # 创建网格布局
    gs = fig.add_gridspec(n_rows, n_cols, 
                          hspace=-0.1, wspace=-0.1,
                          left=0.02, right=0.98, 
                          top=0.95, bottom=0.02)
    
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            # 计算列位置（居中对齐）
            col = m + l_max
            row = l
            
            ax = fig.add_subplot(gs[row, col], projection='3d', 
                               facecolor='white')
            plot_spherical_harmonic(ax, l, m)
            ax.view_init(elev=20, azim=35)
    
    # 添加标题
    fig.suptitle('Spherical Harmonics $Y_\ell^m(\\theta, \\phi)$\n' + 
                 '$\ell = 0, 1, 2, 3, 4, 5$ (rows)  |  ' +
                 '$m = -\ell, ..., 0, ..., \ell$ (columns)',
                 fontsize=14, y=0.99)
    
    plt.savefig('/mnt/user-data/outputs/spherical_harmonics_grid.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("网格版本已保存!")


def create_compact_visualization():
    """
    创建更紧凑的可视化，类似于上传的参考图片（6x7布局）
    参考图看起来是每行有固定数量的列
    """
    fig = plt.figure(figsize=(14, 12), facecolor='white')
    
    # 根据参考图片，看起来是6行x7列的布局
    # 重新分析：参考图第一行只有1个，第二行3个...
    # 这是标准的金字塔布局
    
    l_max = 5
    plot_positions = []
    
    # 收集所有要绘制的(l, m)对
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            plot_positions.append((l, m))
    
    # 计算总数和布局
    total_plots = len(plot_positions)  # 1+3+5+7+9+11 = 36
    
    # 使用金字塔式布局
    fig, axes = plt.subplots(1, 1, figsize=(14, 14), facecolor='white')
    fig.clf()
    
    # 手动定位每个子图
    idx = 0
    y_positions = [0.88, 0.72, 0.56, 0.40, 0.24, 0.08]  # 6行的y位置
    
    for l in range(l_max + 1):
        m_values = list(range(-l, l + 1))
        n_plots_in_row = len(m_values)
        
        # 计算这一行的水平位置
        total_width = 0.9
        plot_width = total_width / (2 * l_max + 1) * 0.95
        row_width = n_plots_in_row * plot_width
        start_x = (1 - row_width) / 2
        
        for i, m in enumerate(m_values):
            x_pos = start_x + i * plot_width
            y_pos = y_positions[l]
            
            ax = fig.add_axes([x_pos, y_pos, plot_width, 0.12], 
                            projection='3d', facecolor='white')
            plot_spherical_harmonic(ax, l, m, resolution=60)
            ax.view_init(elev=20, azim=35)
            idx += 1
    
    plt.savefig('/mnt/user-data/outputs/spherical_harmonics_pyramid.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("金字塔版本已保存!")


def create_reference_style():
    """
    尝试完全匹配参考图片的样式（看起来是规整的6x7网格）
    """
    # 参考图片分析：6行，每行最多7个
    # 可能是 l=0到5，每行显示 m=-3 到 m=3（或者动态调整）
    
    # 重新查看参考图片结构...
    # 第1行: 1个 (l=0)
    # 第2行: 3个 (l=1)  
    # 等等 - 这是标准金字塔
    
    fig = plt.figure(figsize=(16, 14), facecolor='white')
    
    l_max = 5
    
    # 子图规格
    spec = fig.add_gridspec(6, 11, hspace=0.02, wspace=0.02,
                           left=0.02, right=0.98, top=0.96, bottom=0.02)
    
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            # 居中放置
            col_offset = l_max - l  # 左边空白列数
            col = col_offset + (m + l)  # 实际列位置
            
            ax = fig.add_subplot(spec[l, col], projection='3d')
            ax.set_facecolor('white')
            plot_spherical_harmonic(ax, l, m, resolution=70)
            ax.view_init(elev=18, azim=40)
    
    plt.savefig('/mnt/user-data/outputs/spherical_harmonics_final.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("最终版本已保存!")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    
    print("生成球谐函数可视化...")
    
    create_grid_visualization()
    create_compact_visualization() 
    create_reference_style()
    
    print("\n所有版本已生成完毕！")
    print("=" * 50)
