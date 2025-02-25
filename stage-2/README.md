# Growth Curve Analysis: Knock-in vs. Knock-out Strains  

## Overview  
This project analyzes microbial growth curves to determine if there is a **statistical difference** in the time it takes knock-out (MUT) and knock-in (WT) strains to reach their **maximum carrying capacity** (OD600). The analysis involves data visualization, statistical testing, and biological interpretation.  

## Data Sources  
- **Growth Curve Data:** Optical density (OD600) values over time for different strains.  
- **Metadata:** Mapping of wells to strain types (MUT/WT).  

## Methodology  
1. **Data Processing:**  
   - Load growth curve and metadata files.  
   - Merge metadata with OD600 readings.  

2. **Growth Curve Visualization:**  
   - Plot OD600 values over time for each strain.  
   - Highlight differences between MUT and WT strains.  

3. **Time to Carrying Capacity Calculation:**  
   - Determine the time at which OD600 reaches 99% of its maximum value.  
   - Store this data for comparison.  

4. **Statistical Analysis:**  
   - Perform an **independent t-test** to check for significant differences.  
   - Interpret results based on the **p-value** (threshold: 0.05).  

## Key Observations  
- **Growth Curve Trends:** WT and MUT strains show distinct growth patterns.  
- **Variability in Carrying Capacity Time:** MUT strains often display more variation.  
- **Effect of Gene Knockout:** A longer time to carrying capacity in MUT strains may suggest a role in growth regulation.  
- **Statistical Significance:** The t-test determines whether the observed differences are meaningful.  
- **Biological Implications:** Significant differences may indicate that gene knockout affects metabolic efficiency, stress response, or resource utilization.  

## Results Interpretation  
- **p < 0.05:** The difference is **statistically significant** → The gene knockout **impacts growth**.  
- **p ≥ 0.05:** No significant difference → The gene may not play a major role under these conditions.  

## Requirements  
Install the necessary Python libraries before running the script:  
```bash
pip install pandas numpy matplotlib seaborn scipy

