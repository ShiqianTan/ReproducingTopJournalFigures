import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体风格，使其接近学术期刊风格 (Arial/Helvetica)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def draw_plots():
    # === 1. 数据准备 (基于目测估算) ===
    
    # X轴数据 (电位 V vs Ag/AgCl)
    x_labels = ['1.1', '1.15', '1.2', '1.25', '1.3', '1.35', '1.4']
    x = np.arange(len(x_labels))
    width = 0.5  # 柱状图宽度

    # --- 图 e (Amo-MnO2) 数据 ---
    # 左轴 FE (%) - 堆叠柱状图
    e_fe_fa   = np.array([10, 18, 20, 24, 30, 31, 32])
    e_fe_hms  = np.array([68, 72, 70, 58, 60, 52, 51])
    e_fe_meoh = np.array([0.5, 0.5, 0.8, 1.0, 1.2, 1.5, 1.0]) # 顶部很小的一条
    
    # 右轴 Yield (mmol cm-2 h-1) - 折线图
    # 注意：原图右轴有断轴处理(0.002到0.05之间有跳跃)，这里为了保持线性比例主要展示0.05-0.3区间
    e_yld_fa   = np.array([0.05, 0.06, 0.065, 0.075, 0.085, 0.095, 0.10])
    e_yld_hms  = np.array([0.12, 0.16, 0.18, 0.21, 0.25, 0.26, 0.25])
    e_yld_meoh = np.array([0.002, 0.002, 0.003, 0.004, 0.005, 0.008, 0.006]) # 数值很低

    # --- 图 f (L-Cry-MnO2) 数据 ---
    # 左轴 FE (%)
    f_fe_fa   = np.array([20, 22, 25, 42, 42, 40, 40])
    f_fe_hms  = np.array([68, 62, 43, 30, 20, 20, 19])
    f_fe_meoh = np.array([0.5, 0.5, 0.5, 0.8, 1.0, 1.0, 0.8])
    
    # 右轴 Yield
    f_yld_fa   = np.array([0.07, 0.08, 0.09, 0.13, 0.16, 0.19, 0.21])
    f_yld_hms  = np.array([0.17, 0.19, 0.21, 0.21, 0.26, 0.26, 0.26])
    f_yld_meoh = np.array([0.002, 0.002, 0.010, 0.025, 0.040, 0.042, 0.038])

    # === 2. 颜色定义 (吸取自原图) ===
    c_bar_fa   = '#A3D999'  # 浅绿
    c_bar_hms  = '#76B3D6'  # 浅蓝
    c_bar_meoh = '#EBCB6E'  # 浅黄/土黄
    
    c_line_fa   = '#815FC4' # 紫色
    c_line_hms  = '#DE5777' # 玫红
    c_line_meoh = '#C9A436' # 深黄/褐

    # === 3. 绘图 ===
    fig, (ax1_left, ax2_left) = plt.subplots(1, 2, figsize=(14, 5.5))
    plt.subplots_adjust(wspace=0.3, top=0.85, bottom=0.15)

    # 辅助函数：绘制单个子图
    def plot_single(ax, fe_fa, fe_hms, fe_meoh, yld_fa, yld_hms, yld_meoh, title, label_char):
        # --- 左侧 Y 轴 (FE %) ---
        ax.bar(x, fe_fa, width, color=c_bar_fa, label='FA', zorder=10)
        ax.bar(x, fe_hms, width, bottom=fe_fa, color=c_bar_hms, label='HMS', zorder=10)
        ax.bar(x, fe_meoh, width, bottom=fe_fa+fe_hms, color=c_bar_meoh, label='MeOH', zorder=10)
        
        ax.set_ylim(0, 110)
        ax.set_ylabel('FE (%)', fontsize=12, color='black')
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels)
        ax.set_xlabel('$E$ (V vs. Ag/AgCl)', fontsize=12)
        
        # 添加标题 (内部)
        ax.text(0.03, 0.95, title, transform=ax.transAxes, fontsize=12, va='top')
        
        # 添加左上角的大号标签 (e/f)
        ax.text(-0.15, 1.05, label_char, transform=ax.transAxes, fontsize=18, fontweight='bold', va='bottom')

        # 添加左Y轴的蓝色箭头指示
        # ax.annotate('', xy=(-0.15, 0.8), xytext=(-0.05, 0.8), xycoords='axes fraction', 
        #             arrowprops=dict(arrowstyle='->', color='#5D9BC9', lw=2))
        # 原图中是在 FE (%) 文字旁边有一个蓝色折线箭头，这里用简单的文本颜色区分或保持黑色

        # --- 右侧 Y 轴 (Yield) ---
        ax_r = ax.twinx()
        
        # 绘制折线
        ax_r.plot(x, yld_fa, color=c_line_fa, marker='o', markersize=5, linestyle='--', linewidth=1, label='FA (Yield)')
        ax_r.plot(x, yld_hms, color=c_line_hms, marker='o', markersize=5, linestyle='--', linewidth=1, label='HMS (Yield)')
        ax_r.plot(x, yld_meoh, color=c_line_meoh, marker='o', markersize=5, linestyle='--', linewidth=1, label='MeOH (Yield)')
        
        ax_r.set_ylim(0, 0.30)
        ax_r.set_ylabel('Yield (mmol cm$^{-2}$ h$^{-1}$)', fontsize=12, color=c_line_hms)
        
        # 设置右轴刻度和颜色
        ax_r.tick_params(axis='y', colors=c_line_hms, labelcolor=c_line_hms)
        ax_r.spines['right'].set_color(c_line_hms)
        ax_r.spines['left'].set_color('black')
        
        # 为了模拟原图的右轴刻度 (原图有些特殊的低数值刻度)，这里使用标准线性刻度
        # 原图刻度：0.000, 0.005 ... 0.30
        ticks = np.linspace(0, 0.30, 7)
        ax_r.set_yticks(ticks)
        
        return ax, ax_r

    # 绘制子图 e
    ax_e, ax_e_r = plot_single(ax1_left, e_fe_fa, e_fe_hms, e_fe_meoh, e_yld_fa, e_yld_hms, e_yld_meoh, 'Amo-MnO$_2$', 'e')
    # 绘制子图 f
    ax_f, ax_f_r = plot_single(ax2_left, f_fe_fa, f_fe_hms, f_fe_meoh, f_yld_fa, f_yld_hms, f_yld_meoh, 'L-Cry-MnO$_2$', 'f')

    # === 4. 创建统一图例 (Legend) ===
    # 这是一个比较复杂的图例，混合了 Patch (Bar) 和 Line2D
    from matplotlib.lines import Line2D
    import matplotlib.patches as mpatches

    # 定义图例句柄
    legend_elements = [
        # Bar color blocks
        mpatches.Patch(facecolor=c_bar_fa, label='FA'),
        mpatches.Patch(facecolor=c_bar_hms, label='HMS'),
        mpatches.Patch(facecolor=c_bar_meoh, label='MeOH'),
        # Spacer (optional, or just gap in layout)
        # Lines
        Line2D([0], [0], color=c_line_fa, lw=1, linestyle='--', marker='o', label='FA'),
        Line2D([0], [0], color=c_line_hms, lw=1, linestyle='--', marker='o', label='HMS'),
        Line2D([0], [0], color=c_line_meoh, lw=1, linestyle='--', marker='o', label='MeOH'),
    ]

    # 将图例放置在两个图的上方中央
    # 使用 fig.legend 而不是 ax.legend
    fig.legend(handles=legend_elements, 
               loc='upper center', 
               bbox_to_anchor=(0.5, 0.98), 
               ncol=6, 
               frameon=False, 
               columnspacing=1.5,
               handletextpad=0.4)

    # 添加额外的装饰（如左图左侧的蓝色箭头，原图中在 FE 标签旁）
    # 这里用文字注释模拟
    ax1_left.annotate('', xy=(-0.16, 0.8), xytext=(-0.08, 0.8), xycoords='axes fraction',
                      arrowprops=dict(arrowstyle='->', color='#5D9BC9', lw=1.5))
    ax2_left.annotate('', xy=(-0.16, 0.8), xytext=(-0.08, 0.8), xycoords='axes fraction',
                      arrowprops=dict(arrowstyle='->', color='#5D9BC9', lw=1.5))


    plt.tight_layout(rect=[0, 0, 1, 0.92]) # 留出顶部给图例
    plt.savefig('reproduced_plot.png', dpi=300, bbox_inches='tight')
    # plt.show()

if __name__ == "__main__":
    draw_plots()
