import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. 数据准备 (Data Preparation)
# ==========================================
# X轴类别
categories = ['Anatase', 'P25', 'Rutile']

# 左轴数据：选择性 (Selectivity %) - 堆叠柱状图
# 从下到上依次为: Gas, Liquid, Wax
# 数据来源于图中标签
data_gas = np.array([0.6, 1.5, 8.8])
data_liquid = np.array([25.4, 44.9, 60.7])
data_wax = np.array([73.9, 53.5, 30.6])

# 右轴数据：转化率 (Conversion %) - 折线图
# 根据红星位置估算
data_conversion = [20, 45, 91]

# ==========================================
# 2. 绘图设置 (Plot Settings)
# ==========================================
# 设置全局字体为无衬线字体 (类似 Arial/Helvetica)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

fig, ax1 = plt.subplots(figsize=(7, 6), dpi=300)

# 定义颜色 (近似原图的 Hex 颜色)
color_gas = '#FDBF7D'    # 浅橙色
color_liquid = '#8AD68A' # 浅绿色
color_wax = '#BFA6D4'    # 浅紫色
color_line = 'red'       # 红色线条

bar_width = 0.65

# ==========================================
# 3. 绘制堆叠柱状图 (Stacked Bar Chart)
# ==========================================
# 绘制 Gas (底层)
p1 = ax1.bar(categories, data_gas, width=bar_width, color=color_gas, 
             edgecolor='grey', linewidth=0.8, label='Gas')

# 绘制 Liquid (中间层，bottom=Gas)
p2 = ax1.bar(categories, data_liquid, width=bar_width, bottom=data_gas, 
             color=color_liquid, edgecolor='grey', linewidth=0.8, label='Liquid')

# 绘制 Wax (顶层，bottom=Gas+Liquid)
p3 = ax1.bar(categories, data_wax, width=bar_width, bottom=data_gas+data_liquid, 
             color=color_wax, edgecolor='grey', linewidth=0.8, label='Wax')

# ==========================================
# 4. 添加数值标签 (Data Labels)
# ==========================================
def add_labels(ax, data, bottom_data=None):
    for i, val in enumerate(data):
        # 计算标签显示的垂直位置 (柱子中心)
        if bottom_data is not None:
            height = bottom_data[i] + val / 2
        else:
            height = val / 2
            
        # 特殊处理：如果数值太小（如0.6%），稍微向上偏移以免遮挡
        if val < 2:
            height += 1.5 
            
        ax.text(i, height, f'{val}%', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='#333333')

# 添加三层标签
add_labels(ax1, data_gas) # Gas
add_labels(ax1, data_liquid, bottom_data=data_gas) # Liquid
add_labels(ax1, data_wax, bottom_data=data_gas+data_liquid) # Wax

# ==========================================
# 5. 绘制右轴折线图 (Right Axis Line Chart)
# ==========================================
ax2 = ax1.twinx() # 创建共享X轴的第二个Y轴

ax2.plot(categories, data_conversion, color=color_line, marker='*', 
         markersize=14, linestyle='--', linewidth=1.5, label='Conversion')

# ==========================================
# 6. 坐标轴与样式调整 (Axis & Styling)
# ==========================================

# --- 设置 Y 轴范围 ---
ax1.set_ylim(0, 100)
ax2.set_ylim(0, 100)

# --- 设置标签 ---
# 左 Y 轴
ax1.set_ylabel('Selectivity (%)', fontsize=14, fontweight='bold', color='black')
# X 轴
ax1.set_xlabel('TiO$_2$ Phase', fontsize=14, fontweight='bold', labelpad=10)
# 右 Y 轴
ax2.set_ylabel('Conversion (%)', fontsize=14, fontweight='bold', color='red')

# --- 设置刻度样式 ---
# 加粗刻度文字
ax1.tick_params(axis='both', which='major', labelsize=11)
ax2.tick_params(axis='y', which='major', labelsize=11, colors='red')

# 让右轴的刻度线也变成红色
ax2.spines['right'].set_color('red')
ax2.spines['right'].set_linewidth(1.5)
ax2.spines['left'].set_linewidth(1.5)
ax2.spines['top'].set_linewidth(1.5)
ax2.spines['bottom'].set_linewidth(1.5)

# 设置 X 轴刻度标签为粗体
for label in ax1.get_xticklabels():
    label.set_fontweight('bold')
    
# 设置 Y 轴刻度标签为粗体
for label in ax1.get_yticklabels():
    label.set_fontweight('bold')
for label in ax2.get_yticklabels():
    label.set_fontweight('bold')

# ==========================================
# 7. 图例 (Legend)
# ==========================================
# 只显示柱状图的图例，位于顶部
# frameon=False 去掉图例边框，ncol=3 横向排列
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), 
           ncol=3, frameon=False, fontsize=11, handlelength=1.5)

# 调整布局以防止标签被截断
plt.tight_layout()

# 保存图片
plt.savefig('reproduced_chart.png', dpi=300, bbox_inches='tight')

# 显示图片
# plt.show()
