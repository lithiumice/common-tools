import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# 设置英文字体为Times New Roman，中文字体为SimSun
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = ['sans-serif']  # 基础字体类型
plt.rcParams['font.sans-serif'] = ['SimSun', 'Times New Roman']  # 优先使用宋体显示中文，Times New Roman显示英文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建字体对象，用于分别设置英文和中文
english_font = fm.FontProperties(family='Times New Roman')
chinese_font = fm.FontProperties(family='SimSun')

# 定义数据
algorithms = ['SHOW', 'PyMAF-X', 'PIXIE', 'SMPLify-X']
metrics = ['Body Shape', 'Facial Expression', 'Body Motion', 'Hand Motion']

# 定义排名数据 - 格式为 [算法][指标][排名]
# 每个算法在每个指标上的排名分布 (1st, 2nd, 3rd, 4th)
ranking_data = {
    'SHOW': {
        'Body Shape': [90, 10, 0, 0],
        'Facial Expression': [95, 5, 0, 0],
        'Body Motion': [85, 15, 0, 0],
        'Hand Motion': [95, 5, 0, 0]
    },
    'PyMAF-X': {
        'Body Shape': [10, 85, 5, 0],
        'Facial Expression': [5, 90, 5, 0],
        'Body Motion': [15, 80, 5, 0],
        'Hand Motion': [5, 85, 10, 0]
    },
    'PIXIE': {
        'Body Shape': [0, 5, 90, 5],
        'Facial Expression': [0, 5, 90, 5],
        'Body Motion': [0, 5, 85, 10],
        'Hand Motion': [0, 10, 80, 10]
    },
    'SMPLify-X': {
        'Body Shape': [0, 0, 5, 95],
        'Facial Expression': [0, 0, 5, 95],
        'Body Motion': [0, 0, 10, 90],
        'Hand Motion': [0, 0, 10, 90]
    }
}

# 创建一个大图，包含4个子图
fig = plt.figure(figsize=(16, 4.5))
gs = GridSpec(1, 4, figure=fig, wspace=0.15)

# 定义颜色 - 使用更专业的配色方案
colors = ['#4472C4', '#ED7D31', '#FFC000', '#A5A5A5']  # 蓝，橙，黄，灰

# 创建4个子图
axes = []
for i, metric in enumerate(metrics):
    ax = fig.add_subplot(gs[0, i])
    axes.append(ax)
    
    # 为每个算法绘制堆叠柱状图
    bottom = np.zeros(len(algorithms))
    for j, rank in enumerate(['1st', '2nd', '3rd', '4th']):
        values = [ranking_data[alg][metric][j] for alg in algorithms]
        ax.bar(algorithms, values, bottom=bottom, width=0.6, 
               color=colors[j], label=rank if i == 0 else "")
        bottom += values
    
    # 设置标题和坐标轴标签
    if i == 0:
        ax.set_title(f'(1) Body Shape', fontsize=12, fontproperties=english_font)
    elif i == 1:
        ax.set_title(f'(2) Facial Expression', fontsize=12, fontproperties=english_font)
    elif i == 2:
        ax.set_title(f'(3) Body Motion', fontsize=12, fontproperties=english_font)
    else:
        ax.set_title(f'(4) Hand Motion', fontsize=12, fontproperties=english_font)
    
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontproperties=english_font)
    
    # 只在第一个子图显示y轴标签
    if i == 0:
        ax.set_ylabel('Ranking Proportion', fontsize=12, fontproperties=english_font)
    else:
        ax.set_yticklabels([])
    
    # 调整x轴标签的字体大小，应用Times New Roman字体
    ax.set_xticklabels(algorithms, fontsize=10, fontproperties=english_font)
    
    # 添加网格线使图表更清晰
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 调整子图的间距
    ax.margins(x=0.1)

# 在图表下方添加一个共享的图例
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.05), 
           fontsize=10, prop=english_font)

# 添加总标题
# fig.suptitle('Algorithm Ranking Proportion Analysis', fontsize=14, y=0.98, fontproperties=english_font)

# 调整整体布局，确保有足够的空白
plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])

# 保存图片（可选），使用高质量设置
plt.savefig('algorithm_ranking_chart.png', dpi=300, bbox_inches='tight', format='png')
plt.savefig('algorithm_ranking_chart.pdf', bbox_inches='tight', format='pdf')  # 同时保存PDF格式以保持矢量质量

# 显示图表
# plt.show()