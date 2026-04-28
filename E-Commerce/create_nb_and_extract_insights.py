import json
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

markdown_intro = """# E-Commerce Data Analysis & Insights
This notebook explores the E-Commerce dataset using Visualization, Clustering, Association Rules, and Classification.

### Goals:
1. **EDA & Visualization**: Understand sales trends, top products, and geography.
2. **Clustering (Customer Segmentation)**: RFM Analysis + K-Means.
3. **Association Rules**: Market Basket Analysis using Apriori.
4. **Classification**: Predict High-Value Customers.
"""

code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import warnings
warnings.filterwarnings('ignore')

# Set plot style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
"""

markdown_data = """## 1. Data Loading & Preprocessing"""

code_data = """# Load Data
df = pd.read_csv('data.csv', encoding='ISO-8859-1')

# Basic Overview
print(f"Data shape: {df.shape}")
display(df.head())

# Preprocessing
# 1. Drop missing CustomerID
df.dropna(subset=['CustomerID'], inplace=True)
df['CustomerID'] = df['CustomerID'].astype(int)

# 2. Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 3. Remove canceled orders and negative quantities
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# 4. Create Revenue column
df['Revenue'] = df['Quantity'] * df['UnitPrice']

print(f"Data shape after cleaning: {df.shape}")
"""

markdown_eda = """## 2. Exploratory Data Analysis & Visualization"""

code_eda = """# Top 10 Bestselling Products
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
plt.title('Top 10 Bestselling Products by Quantity')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Description')
plt.show()

# Top 10 Countries by Revenue
top_countries = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma')
plt.title('Top 10 Countries by Total Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Country')
plt.show()

# Monthly Revenue trend
df['MonthYear'] = df['InvoiceDate'].dt.to_period('M')
monthly_rev = df.groupby('MonthYear')['Revenue'].sum()
plt.figure(figsize=(14, 6))
monthly_rev.plot(kind='line', marker='o')
plt.title('Monthly Sales Revenue')
plt.xlabel('Month-Year')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""

markdown_clustering = """## 3. Clustering: Customer Segmentation (RFM + K-Means)"""

code_clustering = """# Create RFM Features
snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Revenue': 'sum'
})

rfm.rename(columns={'InvoiceDate': 'Recency',
                    'InvoiceNo': 'Frequency',
                    'Revenue': 'MonetaryValue'}, inplace=True)

# Remove outliers for better clustering
q = rfm['MonetaryValue'].quantile(0.99)
rfm = rfm[rfm['MonetaryValue'] < q]

# Scale features
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

# Apply KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# Assign meaningful names
cluster_means = rfm.groupby('Cluster').mean()
print("Cluster Centers (Mean Values):")
display(cluster_means)

# Plotting Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm, x='Recency', y='MonetaryValue', hue='Cluster', palette='Set1', alpha=0.6)
plt.title('Customer Segments: Recency vs Monetary Value')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm, x='Frequency', y='MonetaryValue', hue='Cluster', palette='Set1', alpha=0.6)
plt.title('Customer Segments: Frequency vs Monetary Value')
plt.show()
"""

markdown_ar = """## 4. Association Rules: Market Basket Analysis"""

code_ar = """# We will analyze transactions from the UK (the largest market) to avoid memory issues
basket = (df[df['Country'] =="United Kingdom"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

# Binarize the data (1 if item present, 0 otherwise)
def encode_units(x):
    if x <= 0: return 0
    if x >= 1: return 1

basket_sets = basket.applymap(encode_units)

# Find Frequent Itemsets using Apriori
frequent_itemsets = apriori(basket_sets, min_support=0.02, use_colnames=True)

# Generate Rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values('lift', ascending=False)

print("Top 10 Association Rules:")
display(rules.head(10))
"""

markdown_cls = """## 5. Classification: Predicting High-Value Customers"""

code_cls = """# Target Definition: High-Value Customer (Top 25% by Monetary Value)
threshold = rfm['MonetaryValue'].quantile(0.75)
rfm['HighValue'] = (rfm['MonetaryValue'] >= threshold).astype(int)

# Features and Target
# To make it interesting, let's pretend we only have Recency and Frequency to predict Monetary Value class
X = rfm[['Recency', 'Frequency']]
y = rfm['HighValue']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Classifier
clf = RandomForestClassifier(random_state=42, n_estimators=100)
clf.fit(X_train, y_train)

# Predictions
y_pred = clf.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Regular', 'High-Value'], yticklabels=['Regular', 'High-Value'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Feature Importance
importances = clf.feature_importances_
sns.barplot(x=importances, y=['Recency', 'Frequency'])
plt.title('Feature Importance in Predicting High-Value Customers')
plt.show()
"""

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\\n" for line in source.split('\\n')]
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\\n" for line in source.split('\\n')]
    }

notebook = {
    "cells": [
        create_markdown_cell(markdown_intro),
        create_code_cell(code_imports),
        create_markdown_cell(markdown_data),
        create_code_cell(code_data),
        create_markdown_cell(markdown_eda),
        create_code_cell(code_eda),
        create_markdown_cell(markdown_clustering),
        create_code_cell(code_clustering),
        create_markdown_cell(markdown_ar),
        create_code_cell(code_ar),
        create_markdown_cell(markdown_cls),
        create_code_cell(code_cls),
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('E_Commerce_Analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4)

print("Jupyter Notebook 'E_Commerce_Analysis.ipynb' generated successfully!")


# -------------------------------------------------------------------------------------------------
# Real Analysis run to extract insights for the user
print("Running analytical extraction for insights...")

df = pd.read_csv('data.csv', encoding='ISO-8859-1')
df.dropna(subset=['CustomerID'], inplace=True)
df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df['Revenue'] = df['Quantity'] * df['UnitPrice']

print("\\n--- EDA Insights ---")
top_product = df.groupby('Description')['Quantity'].sum().idxmax()
top_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
print(f"Top Product: {top_product}")
print(f"Top Country: {top_country.index[0]} with ${top_country.iloc[0]:.2f}")
if len(top_country) > 1:
    print(f"Second Top Country: {top_country.index[1]} with ${top_country.iloc[1]:.2f}")

print("\\n--- Clustering Insights ---")
snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Revenue': 'sum'
})
rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Revenue': 'MonetaryValue'}, inplace=True)
q = rfm['MonetaryValue'].quantile(0.99)
rfm_c = rfm[rfm['MonetaryValue'] < q]

rfm_scaled = StandardScaler().fit_transform(rfm_c)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
rfm_c['Cluster'] = kmeans.fit_predict(rfm_scaled)
print("Cluster Profiles (Mean):")
print(rfm_c.groupby('Cluster').mean().round(2))

print("\\n--- Association Rules (sample) ---")
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    df_uk = df[df['Country'] == 'United Kingdom']
    df_uk_sample = df_uk.sample(frac=0.1, random_state=42)
    basket = (df_uk_sample.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))
    basket_sets = basket.applymap(lambda x: 1 if x >= 1 else 0)
    
    freq_items = apriori(basket_sets, min_support=0.03, use_colnames=True)
    if not freq_items.empty:
        rules = association_rules(freq_items, metric="lift", min_threshold=1)
        if not rules.empty:
            best_rule = rules.sort_values('lift', ascending=False).iloc[0]
            print(f"Strongest assoc rule sampled: {list(best_rule['antecedents'])} -> {list(best_rule['consequents'])} (Lift: {best_rule['lift']:.2f})")
        else:
            print("No strong association rules found in this sample.")
    else:
        print("No frequent items found in this support threshold.")
except Exception as e:
    print(f"Could not calculate association rules: {type(e).__name__} - {str(e)}")

print("\\n--- Classification Insights ---")
threshold = rfm['MonetaryValue'].quantile(0.75)
rfm['HighValue'] = (rfm['MonetaryValue'] >= threshold).astype(int)
X = rfm[['Recency', 'Frequency']]
y = rfm['HighValue']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(random_state=42, n_estimators=50)
clf.fit(X_train, y_train)
acc = accuracy_score(y_test, clf.predict(X_test))
print(f"Accuracy of predicting top 25% High-Value Customers using only Recency & Frequency: {acc*100:.2f}%")
print("Process completed.")
