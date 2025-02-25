import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import math  # For subplot grid calculation
 
# Load growth curve data
url_data = 'https://raw.githubusercontent.com/HackBio-Internship/2025_project_collection/refs/heads/main/Python/Dataset/mcgc.tsv'
data = pd.read_csv(url_data, sep='\t')
 
# Load metadata
url_metadata = 'https://raw.githubusercontent.com/HackBio-Internship/2025_project_collection/main/Python/Dataset/mcgc_METADATA.txt'
metadata = pd.read_csv(url_metadata, sep='\t', engine='python')
 
# Print metadata to verify structure
print("Metadata Columns:", metadata.columns)
 
# Melt metadata to long format
metadata_melted = metadata.melt(id_vars=['Strain'], var_name='Type', value_name='Well')
 
# Correct condition assignment: 'MUT' (mutant) = Knock-out (-), 'WT' (wild-type) = Knock-in (+)
metadata_melted['Condition'] = np.where(metadata_melted['Type'].str.startswith('MUT'), 'MUT', 'WT')
 
data_melted = data.melt(id_vars=['time'], var_name='Well', value_name='OD600')
 
# Merge growth data with metadata
merged_data = pd.merge(data_melted, metadata_melted, on='Well')
 
# Function to determine time to carrying capacity
def time_to_carrying_capacity(time, od_values):
   max_od = max(od_values)  # Carrying capacity (max OD600)
   threshold = 0.99 * max_od  # 99% of carrying capacity
   
   # Find the earliest time where OD reaches 99% of max
   reaching_time = time[od_values >= threshold]
   
   if not reaching_time.empty:
       return reaching_time.iloc[0]  
   return np.nan  
# Prepare a DataFrame to store carrying capacity times
carrying_capacity_times = []
 
# Determine subplot grid size dynamically
num_strains = merged_data['Strain'].nunique()
num_cols = 3  # Fix columns to 3 for better visualization
num_rows = math.ceil(num_strains / num_cols)
 
# Create a figure for growth curves
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axes = axes.flatten()  # Flatten for easier iteration
 
# Plot growth curves for each strain
for i, strain in enumerate(merged_data['Strain'].unique()):
   ax = axes[i]  # Get corresponding subplot
   strain_data = merged_data[merged_data['Strain'] == strain]
   
   for condition in ['MUT', 'WT']:
       condition_data = strain_data[strain_data['Condition'] == condition]
       
       for well in condition_data['Well'].unique():
           well_data = condition_data[condition_data['Well'] == well]
           
           # Convert to NumPy arrays for efficiency
           time_array = well_data['time'].values
           od_array = well_data['OD600'].values
           
           ax.plot(time_array, od_array, label=f'{condition} {well}')
           
           # Calculate time to carrying capacity
           carrying_time = time_to_carrying_capacity(pd.Series(time_array), pd.Series(od_array))
           carrying_capacity_times.append({'Strain': strain, 'Condition': condition, 'Well': well, 'CarryingCapacityTime': carrying_time})
   
   ax.set_title(f'Growth Curve: {strain}')
   ax.set_xlabel('Time (minutes)')
   ax.set_ylabel('OD600')
   ax.legend()
   ax.grid(True)
 
# Hide empty subplots
for j in range(i + 1, len(axes)):
   fig.delaxes(axes[j])
 
plt.tight_layout()
plt.show()
 
# Convert carrying capacity times to DataFrame
carrying_capacity_df = pd.DataFrame(carrying_capacity_times)
 
# Scatter plot of carrying capacity times
plt.figure(figsize=(10, 6))
sns.scatterplot(data=carrying_capacity_df, x='Strain', y='CarryingCapacityTime', hue='Condition', style='Condition', s=100)
plt.title('Time to Reach Carrying Capacity for WT and MUT Strains')
plt.xlabel('Strain')
plt.ylabel('Time to Carrying Capacity (minutes)')
plt.grid(True)
plt.show()
 
# Box plot of carrying capacity times
plt.figure(figsize=(10, 6))
sns.boxplot(data=carrying_capacity_df, x='Condition', y='CarryingCapacityTime')
plt.title('Distribution of Time to Carrying Capacity by Condition (WT vs. MUT)')
plt.xlabel('Condition')
plt.ylabel('Time to Carrying Capacity (minutes)')
plt.grid(True)
plt.show()
 
# Statistical analysis
mut_times = carrying_capacity_df[carrying_capacity_df['Condition'] == 'MUT']['CarryingCapacityTime'].dropna()
wt_times = carrying_capacity_df[carrying_capacity_df['Condition'] == 'WT']['CarryingCapacityTime'].dropna()
 
# Perform t-test
t_stat, p_value = ttest_ind(mut_times, wt_times, equal_var=False)
 
print(f'T-test statistic: {t_stat:.4f}')
print(f'P-value: {p_value:.4f}')
 
# Interpretation
alpha = 0.05
if p_value < alpha:
   print("There is a statistically significant difference in the time to reach carrying capacity between WT and MUT strains.")
else:
   print("There is no statistically significant difference in the time to reach carrying capacity between WT and MUT strains.")

# Observations 

# 1. Growth Curve Trends:
#    - Knock-out (MUT) and knock-in (WT) strains show distinct growth patterns.
#    - Variations are observed in the time taken to reach maximum OD600.

# 2. Variability in Carrying Capacity Time:
#    - The scatter plot and box plot highlight differences in carrying capacity times.
#    - MUT strains generally display more variability in reaching carrying capacity.

# 3. Effect of Gene Knockout:
#    - If MUT strains take significantly longer to reach carrying capacity, 
#      it suggests the deleted gene may influence growth regulation.

# 4. Statistical Significance:
#    - A t-test is performed to compare the carrying capacity times of MUT and WT strains.
#    - A p-value < 0.05 indicates a statistically significant difference, 
#      while p ≥ 0.05 suggests no significant effect.

# 5. Biological Implications:
#    - A significant difference implies that gene knockout affects metabolic efficiency, 
#      stress response, or resource utilization.
#    - If no difference is found, the gene may not play a crucial role under these conditions.

