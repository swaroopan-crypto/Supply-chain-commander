import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('inventory_risk_dashboard.csv')

# Configure seaborn styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.size'] = 10

# Create figure and axes
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Inventory Risk Dashboard', fontsize=26, fontweight='bold', y=0.95)

# Layout setup using GridSpec
grid = plt.GridSpec(3, 3, figure=fig, height_ratios=[1, 3, 4], hspace=0.4, wspace=0.3)

# --- KPIs ---
ax_kpi1 = fig.add_subplot(grid[0, 0])
ax_kpi2 = fig.add_subplot(grid[0, 1])
ax_kpi3 = fig.add_subplot(grid[0, 2])

for ax in [ax_kpi1, ax_kpi2, ax_kpi3]:
    ax.axis('off')

total_lost_revenue = df['potential_lost_revenue'].sum()
high_risk_count = len(df[df['risk_level'] == 'HIGH RISK'])
total_skus = len(df)

# KPI Text settings
ax_kpi1.text(0.5, 0.7, 'Total Potential\nLost Revenue', ha='center', va='center', fontsize=16, color='gray', fontweight='bold')
ax_kpi1.text(0.5, 0.25, f'${total_lost_revenue:,.2f}', ha='center', va='center', fontsize=28, fontweight='bold', color='#d32f2f')

ax_kpi2.text(0.5, 0.7, 'High Risk SKUs', ha='center', va='center', fontsize=16, color='gray', fontweight='bold')
ax_kpi2.text(0.5, 0.25, f'{high_risk_count}', ha='center', va='center', fontsize=28, fontweight='bold', color='#f57c00')

ax_kpi3.text(0.5, 0.7, 'Total SKUs Tracked', ha='center', va='center', fontsize=16, color='gray', fontweight='bold')
ax_kpi3.text(0.5, 0.25, f'{total_skus}', ha='center', va='center', fontsize=28, fontweight='bold', color='#1976d2')

# --- Risk Level Distribution ---
ax_pie = fig.add_subplot(grid[1, 0])
risk_counts = df['risk_level'].value_counts()
colors = ['#e57373' if 'HIGH' in x else '#64b5f6' for x in risk_counts.index]
ax_pie.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', startangle=90, colors=colors, 
           textprops={'fontsize': 12, 'fontweight': 'bold'}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax_pie.set_title('Risk Level Distribution', fontsize=16, fontweight='bold')

# --- Top 5 SKUs by Potential Lost Revenue ---
ax_bar = fig.add_subplot(grid[1, 1:])
top_5 = df.nlargest(5, 'potential_lost_revenue')
sns.barplot(data=top_5, x='potential_lost_revenue', y='product_id', hue='product_id', ax=ax_bar, palette='Reds_r', legend=False)
ax_bar.set_title('Top 5 SKUs by Potential Lost Revenue', fontsize=16, fontweight='bold')
ax_bar.set_xlabel('Lost Revenue ($)', fontsize=12)
ax_bar.set_ylabel('Product ID', fontsize=12)

# Format x-axis for currency
from matplotlib.ticker import FuncFormatter
ax_bar.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'${x:,.0f}'))

# --- Scatter Plot: Current Stock vs Predicted Sales ---
ax_scatter = fig.add_subplot(grid[2, :])
scatter = sns.scatterplot(data=df, x='current_stock', y='predicted_30day_sales', 
                          hue='risk_level', size='potential_lost_revenue', 
                          sizes=(80, 600), alpha=0.8, 
                          palette={'HIGH RISK':'#d32f2f', 'MEDIUM RISK':'#1976d2', 'LOW RISK':'#388e3c'}, 
                          ax=ax_scatter)

# Add line x=y to represent exactly meeting demand
max_val = max(df['current_stock'].max(), df['predicted_30day_sales'].max())
ax_scatter.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Stock = Demand (Equilibrium)')

# Highlight critical area (High demand, low stock)
ax_scatter.fill_between([0, max_val], [0, max_val], max_val, color='#ffebee', alpha=0.3, label='Shortage Risk Area')

ax_scatter.set_title('Current Stock vs Predicted 30-Day Sales', fontsize=16, fontweight='bold')
ax_scatter.set_xlabel('Current Stock (Units)', fontsize=14)
ax_scatter.set_ylabel('Predicted 30-Day Sales (Units)', fontsize=14)
ax_scatter.grid(True, linestyle='--', alpha=0.6)

# Improve legend
handles, labels = ax_scatter.get_legend_handles_labels()
# Attempt to filter out size legend or rename it for clarity
ax_scatter.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., title="Legend")

# Output
plt.savefig('inventory_risk_dashboard.png', dpi=300, bbox_inches='tight')
print("Dashboard saved successfully to inventory_risk_dashboard.png")
