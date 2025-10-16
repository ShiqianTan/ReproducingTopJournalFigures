# 1	Gao, Y.-C. et al. Accelerating battery innovation: AI-powered molecular discovery. Chemical Society Reviews (2025). https://doi.org:10.1039/D5CS00053J

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
import numpy as np

# 创建布洛芬分子
smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  # 布洛芬
mol = Chem.MolFromSmiles(smiles)

# 生成2D坐标
AllChem.Compute2DCoords(mol)

# 定义元素颜色方案
element_colors = {
    'C': '#404040',   # 碳 - 深灰色
    'H': '#FFFFFF',   # 氢 - 白色
    'O': '#FF0000',   # 氧 - 红色
    'N': '#0000FF',   # 氮 - 蓝色
    'S': '#FFFF00',   # 硫 - 黄色
    'P': '#FFA500',   # 磷 - 橙色
    'F': '#00FF00',   # 氟 - 绿色
    'Cl': '#00FF00',  # 氯 - 绿色
    'Br': '#8B4513',  # 溴 - 棕色
    'I': '#9400D3',   # 碘 - 紫色
}

# 定义环的颜色方案（每种元素对应的渐变色）
ring_colors = {
    'C': ['#E8E8E8', '#C8C8C8', '#A8A8A8', '#888888'],
    'O': ['#FFE8E8', '#FFB8B8', '#FF8888', '#FF5858'],
    'N': ['#E8E8FF', '#B8B8FF', '#8888FF', '#5858FF'],
    'S': ['#FFFFE8', '#FFFFB8', '#FFFF88', '#FFFF58'],
    'P': ['#FFF4E8', '#FFD8B8', '#FFBC88', '#FFA058'],
}

# 获取原子坐标和信息
conf = mol.GetConformer()
atom_info = []
for i in range(mol.GetNumAtoms()):
    pos = conf.GetAtomPosition(i)
    atom = mol.GetAtomWithIdx(i)
    symbol = atom.GetSymbol()
    atom_info.append({
        'pos': (pos.x, pos.y),
        'symbol': symbol,
        'color': element_colors.get(symbol, '#808080')
    })

# 创建图形
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

# 绘制化学键
for bond in mol.GetBonds():
    start_idx = bond.GetBeginAtomIdx()
    end_idx = bond.GetEndAtomIdx()
    start_pos = atom_info[start_idx]['pos']
    end_pos = atom_info[end_idx]['pos']
    
    # 根据键的类型设置线宽
    bond_type = bond.GetBondType()
    if bond_type == Chem.BondType.DOUBLE:
        linewidth = 3
    elif bond_type == Chem.BondType.TRIPLE:
        linewidth = 4
    else:
        linewidth = 2
    
    ax.plot([start_pos[0], end_pos[0]], 
            [start_pos[1], end_pos[1]], 
            'k-', linewidth=linewidth, zorder=2, alpha=0.6)

# 为每个原子绘制同心圆环
for atom in atom_info:
    pos = atom['pos']
    symbol = atom['symbol']
    color = atom['color']
    
    # 获取该元素对应的环颜色，如果没有则使用默认灰色
    colors = ring_colors.get(symbol, ['#E8E8E8', '#C8C8C8', '#A8A8A8', '#888888'])
    
    # 绘制多个同心圆环（指纹效果）
    radii = [0.55, 0.45, 0.35, 0.25]
    for i, (radius, ring_color) in enumerate(zip(radii, colors)):
        circle = patches.Circle(pos, radius, 
                               facecolor=ring_color, 
                               edgecolor=color, 
                               linewidth=1.2,
                               alpha=0.5,
                               zorder=1)
        ax.add_patch(circle)
    
    # 在中心绘制指纹图标（颜色与元素对应）
    circle_center = patches.Circle(pos, 0.18, 
                                  facecolor=color, 
                                  edgecolor='white',
                                  linewidth=2,
                                  zorder=3)
    ax.add_patch(circle_center)
    
    # 添加指纹线条效果（弧形）
    num_lines = 12
    angles = np.linspace(0, 2*np.pi, num_lines, endpoint=False)
    for j, angle in enumerate(angles):
        # 交替长短线条，形成指纹效果
        if j % 2 == 0:
            length = 0.10
        else:
            length = 0.07
        x_end = pos[0] + length * np.cos(angle)
        y_end = pos[1] + length * np.sin(angle)
        ax.plot([pos[0], x_end], [pos[1], y_end], 
               'w-', linewidth=1.5, zorder=4, alpha=0.8)
    
    # 标注原子符号在中心（所有原子都标注）
    ax.text(pos[0], pos[1], symbol, 
           fontsize=11, fontweight='bold',
           ha='center', va='center',
           color='white',
           zorder=5)

# 设置图形属性
all_x = [atom['pos'][0] for atom in atom_info]
all_y = [atom['pos'][1] for atom in atom_info]

ax.set_aspect('equal')
ax.set_xlim(min(all_x) - 1.5, max(all_x) + 1.5)
ax.set_ylim(min(all_y) - 1.5, max(all_y) + 1.5)
ax.axis('off')
ax.set_facecolor('#F8F8F8')

# 添加标题
plt.title('Molecular Fingerprint - Ibuprofen', 
         fontsize=18, fontweight='bold', pad=20, color='#333333')

# 添加图例
legend_elements = []
for element in ['C', 'O', 'N', 'S', 'P']:  # 常见元素
    if any(atom['symbol'] == element for atom in atom_info):
        legend_elements.append(patches.Patch(facecolor=element_colors[element], 
                                            edgecolor='white', 
                                            label=element))

if legend_elements:
    ax.legend(handles=legend_elements, 
             loc='upper right', 
             fontsize=11,
             framealpha=0.9,
             title='Elements')

plt.tight_layout()
plt.savefig("./fingerprint_mol_graph.png", dpi=300)
plt.show()
