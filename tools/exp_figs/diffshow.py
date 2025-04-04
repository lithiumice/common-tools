import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import PercentFormatter

# Set the font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Data preparation
methods = ['DiffSHOW', 'LS3DCG', 'GT']

# Realism rankings data (in percentage)
realism_first = [20, 5, 75]
realism_second = [65, 20, 15]
realism_third = [15, 75, 10]

# Synchronization rankings data (in percentage)
sync_first = [25, 5, 70]
sync_second = [60, 20, 20]
sync_third = [15, 75, 10]

# Create a figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.subplots_adjust(wspace=0.3)

# Set the width of bars
width = 0.6

# Positions for the bars
positions = np.arange(len(methods))

# Colors for each ranking
colors = ['#4472C4', '#ED7D31', '#FFC000', '#A5A5A5']  # Blue, Orange, Yellow, Gray

# Plot for Realism
ax1.bar(positions, realism_first, width, label='1st', color=colors[0])
ax1.bar(positions, realism_second, width, bottom=realism_first, label='2nd', color=colors[1])
ax1.bar(positions, realism_third, width, bottom=np.array(realism_first) + np.array(realism_second), 
        label='3rd', color=colors[2])

# Plot for Synchronization
ax2.bar(positions, sync_first, width, label='1st', color=colors[0])
ax2.bar(positions, sync_second, width, bottom=sync_first, label='2nd', color=colors[1])
ax2.bar(positions, sync_third, width, bottom=np.array(sync_first) + np.array(sync_second), 
        label='3rd', color=colors[2])

# Customize the first subplot (Realism)
ax1.set_title('(1) Realism', fontsize=12, pad=10)
ax1.set_xticks(positions)
ax1.set_xticklabels(methods)
ax1.set_ylabel('Ranking Proportion', fontsize=11)
ax1.set_ylim(0, 100)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
ax1.yaxis.set_major_formatter(PercentFormatter())

# Customize the second subplot (Synchronization)
ax2.set_title('(2) Synchronization', fontsize=12, pad=10)
ax2.set_xticks(positions)
ax2.set_xticklabels(methods)
ax2.set_ylim(0, 100)
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
ax2.yaxis.set_major_formatter(PercentFormatter())

# Add a common legend
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.5, +0.0), fontsize=10)

# # Add a common title
# fig.suptitle('Subjective Evaluation Results of DiffSHOW (Based on 40 Video Samples)', 
#              fontsize=14, y=0.98)

# Layout adjustments
fig.tight_layout()
plt.subplots_adjust(bottom=0.15)

# Save the figure in high resolution
plt.savefig('diffshow_evaluation_results.png', dpi=300, bbox_inches='tight')
plt.savefig('diffshow_evaluation_results.pdf', bbox_inches='tight', format='pdf')  # 同时保存PDF格式以保持矢量质量

# Show the plot
# plt.show()