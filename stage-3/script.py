import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
 
# Load dataset
url = "https://raw.githubusercontent.com/HackBio-Internship/2025_project_collection/refs/heads/main/Python/Dataset/drug_class_struct.txt"
 
try:
   data = pd.read_csv(url, delimiter='\t')
   print("Dataset loaded successfully!")
except Exception as e:
   print(f"Error loading dataset: {e}")
   exit()
 
# Ensure 'score' column exists
if 'score' not in data.columns:
   raise ValueError("Column 'score' not found in dataset. Check column names.")
 
# Handle missing values
data.fillna(data.mean(numeric_only=True), inplace=True)
 
# Separate features and docking scores
features = data.drop(columns=['score']).select_dtypes(include=[np.number])
docking_scores = data['score']
 
# Standardize features (important for PCA & Regression)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
 
# Apply PCA (reduce dimensions to 2 for visualization)
pca = PCA(n_components=2)
principal_components = pca.fit_transform(features_scaled)
 
# Convert PCA results to a DataFrame
pca_df = pd.DataFrame(principal_components, columns=['PC1', 'PC2'])
pca_df['score'] = docking_scores
 
# Perform K-means clustering (set k to 5, can be adjusted)
optimal_clusters = 5  
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
pca_df['cluster'] = kmeans.fit_predict(principal_components)
 
# Chemical Space Representation (Without Clusters)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['score'], cmap='plasma', alpha=0.8)
plt.colorbar(scatter, label='Docking Score')  
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Chemical Space Representation')
plt.grid()
plt.show()
 
# Chemical Space with Clustering
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PC1', y='PC2', hue=pca_df['cluster'], palette='viridis', data=pca_df, alpha=0.8)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Chemical Space Clustering')
plt.legend(title="Cluster")
plt.grid()
plt.show()
 
# Chemical Space Colored by Docking Score
plt.figure(figsize=(10, 6))
scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['score'], cmap='coolwarm', alpha=0.8)
plt.colorbar(scatter, label='Docking Score')  
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Chemical Space Colored by Docking Score')
plt.grid()
plt.show()
 
# Regression Model to Predict Docking Score
 
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_scaled, docking_scores, test_size=0.2, random_state=42)
 
# Train a **Random Forest Regressor**
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
 
# Predict on the test set
y_pred = rf.predict(X_test)
 
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'\n Mean Squared Error (MSE): {mse:.4f}')
print(f' R² Score: {r2:.4f}')
 
# Feature importance analysis
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
 
# Debugging: Check indices and feature names
print("\nFeature indices:", indices)
print("Feature names:", list(features.columns))
 
# Plot feature importances
plt.figure(figsize=(12, 6))
plt.title('Feature Importances (Top 20)')
plt.bar(range(min(20, features.shape[1])), importances[indices[:20]], align='center', color='royalblue')
plt.xticks(range(min(20, features.shape[1])), np.array(features.columns)[indices[:20]], rotation=90)
plt.xlabel('Chemical Descriptors')
plt.ylabel('Importance')
plt.grid()
plt.show()
