import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from FinancialStats import main as calculate_metrics
from utilities import convert_to_number, random_forest_feature_importance, pca_dimensionality_reduction
from AnalysisStats import dataframes
import concurrent.futures
import json
import asyncio

# Set random seed for reproducibility
np.random.seed(42)

# Load the calculated values from calculations.py
calculated_values = asyncio.run(calculate_metrics())

# Load the raw data from EarningsReports.py
earnings_df = dataframes['earnings_df']
revenue_df = dataframes['revenue_df']
earnings_history_df = dataframes['earnings_history']
eps_trend_df = dataframes['eps_trend_df']

# Drop rows with all NaN values
earnings_history_df = earnings_history_df.dropna(how='all')

# Reset indices to ensure proper stacking
earnings_df = earnings_df.reset_index(drop=True)
revenue_df = revenue_df.reset_index(drop=True)
earnings_history_df = earnings_history_df.reset_index(drop=True)
eps_trend_df = eps_trend_df.reset_index(drop=True)

# List of dataframes
dataframes_list = [
    (earnings_df, 'earnings_df'),
    (revenue_df, 'revenue_df'),
    (earnings_history_df, 'earnings_history_df'),
    (eps_trend_df, 'eps_trend_df')
]

# Reduced parameter grid for smaller datasets
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 5],
    'max_features': ['sqrt', 'log2'],
    'bootstrap': [True, False]
}

# Function to preprocess and analyze the combined dataframe
def preprocess_and_analyze(df, name):
    results = {
        'name': name,
        'random_forest_importances': None,
        'pca_components': None
    }
    
    # Transpose the dataframe to analyze rows
    df = df.transpose()
    
    # Set the first row as the header
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    # Convert all column names to strings
    df.columns = df.columns.astype(str)

    # Convert relevant columns to numeric using convert_to_number
    for col in df.columns:
        df[col] = df[col].apply(lambda x: convert_to_number(x) if isinstance(x, str) else x)
    
    # Identify numeric and categorical features
    numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df.select_dtypes(include=[object]).columns.tolist()
    
    # Skip if there are no numeric features
    if not numeric_features:
        return results
    
    # Define the preprocessing pipeline
    transformers = [
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ]), numeric_features)
    ]
    if categorical_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features))
    
    preprocessor = ColumnTransformer(transformers=transformers)
    
    # Apply the preprocessing pipeline
    X = preprocessor.fit_transform(df)
    
    # Create a DataFrame from the preprocessed data
    feature_names = numeric_features
    if categorical_features:
        feature_names += list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features))
    preprocessed_df = pd.DataFrame(X, columns=feature_names, index=df.index)
    
    X_df = pd.DataFrame(X, columns=feature_names, index=df.index)
    if X_df.empty:
        return results
    
    # Check for NaNs and Infinities
    if X_df.isnull().values.any() or np.isinf(X_df.values).any():
        return results
    
    # Define target variables for each dataset
    target_variable = None
    if name == 'earnings_df':
        target_variable = 'Avg. Estimate'
    elif name == 'revenue_df':
        target_variable = 'Avg. Estimate'
    elif name == 'earnings_history_df':
        target_variable = 'EPS Actual'
    elif name == 'eps_trend_df':
        target_variable = 'Current Estimate'
    
    rf_importances = random_forest_feature_importance(X_df, target_variable)
    
    if rf_importances.empty:
        return results
    
    if name == 'earnings_df' or name == 'eps_trend_df' or name == 'revenue_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 3)
    elif name == 'earnings_history_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 2)
    
    results['random_forest_importances'] = rf_importances.to_dict()
    results['pca_components'] = pca_df.to_dict()
    
    return results

# Analyze each dataframe separately in parallel
all_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(preprocess_and_analyze, df, name) for df, name in dataframes_list]
    for future in concurrent.futures.as_completed(futures):
        all_results.append(future.result())

# Save the results to a dictionary
statistical_results = {
    'results': all_results
}

# Function to handle NaN values in JSON
def handle_nan(value):
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

# Save to JSON file
with open('Earnings/results/statistical_results.json', 'w') as f:
    json.dump(statistical_results, f, indent=4, default=handle_nan)