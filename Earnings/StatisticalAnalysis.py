import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from calculations import main as calculate_metrics, convert_to_number
from EarningsReports import dataframes

# Calculated values from calculations.py
calculated_values = calculate_metrics()

# Raw data from EarningsReports.py for the RF and PCA analysis
earnings_df = dataframes['earnings_df']
revenue_df = dataframes['revenue_df']
earnings_history_df = dataframes['earnings_history']
eps_trend_df = dataframes['eps_trend_df']
growth_estimate_df = dataframes['growth_estimate_df']

# Raw data that is not used in the analysis due to lack of numeric features
top_analysts_df = dataframes['top_analysts_df']
revenue_earnings_df = dataframes['revenue_earnings_df']
analyst_price_targets_df = dataframes['analyst_price_targets_df']

# List of dataframes
dataframes_list = [
    (earnings_df, 'earnings_df'),
    (revenue_df, 'revenue_df'),
    (earnings_history_df, 'earnings_history_df'),
    (eps_trend_df, 'eps_trend_df'),
    (growth_estimate_df, 'growth_estimate_df'),
]

# Combine all dataframes into one
combined_df = pd.concat([earnings_df, revenue_df, earnings_history_df, eps_trend_df, growth_estimate_df], axis=1)

# Function to preprocess and analyze the combined dataframe
def preprocess_and_analyze(df, name):
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
        print(f"No numeric features found in {name}. Skipping.")
        return
    
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
    preprocessed_df = pd.DataFrame(X, columns=feature_names)
    
    # Check if preprocessed_df is empty after preprocessing
    if preprocessed_df.empty:
        print(f"Preprocessed DataFrame for {name} is empty after preprocessing. Skipping.")
        return
    
    # Random Forest for Feature Importance and Correlations
    def random_forest_feature_importance(df):
        X = df
        y = np.random.rand(len(df))  # Dummy target variable for feature importance
        
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        feature_importances = pd.DataFrame(rf.feature_importances_, index=X.columns, columns=['Importance']).sort_values('Importance', ascending=False)
        
        return feature_importances

    # Gradient Boosting for Feature Importance
    def gradient_boosting_feature_importance(df):
        X = df
        y = np.random.rand(len(df))  # Dummy target variable for feature importance
        
        gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
        gb.fit(X, y)
        
        feature_importances = pd.DataFrame(gb.feature_importances_, index=X.columns, columns=['Importance']).sort_values('Importance', ascending=False)
        
        return feature_importances

    # Principal Component Analysis (PCA) for Dimensionality Reduction
    def pca_dimensionality_reduction(df, n_components):
        X = df
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(X_scaled)
        
        pca_df = pd.DataFrame(pca.components_.T, columns=[f'PC{i+1}' for i in range(n_components)], index=df.columns)
        
        return pca_df

    rf_importances = random_forest_feature_importance(preprocessed_df)
    gb_importances = gradient_boosting_feature_importance(preprocessed_df)
    
    if name == 'earnings_df' or name == 'eps_trend_df' or name == 'revenue_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 3)
    elif name == 'earnings_history_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 2)
    elif name == 'growth_estimate_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 1)
    
    print(f"Random Forest Feature Importances for {name}:\n", rf_importances)
    print(f"Gradient Boosting Feature Importances for {name}:\n", gb_importances)
    print(f"PCA DataFrame for {name}:\n", pca_df)

# Analyze each dataframe separately
for df, name in dataframes_list:
    print(f"\nAnalyzing {name}...")
    preprocess_and_analyze(df, name)

# # Analyze calculated data separately
# print("\nAnalyzing calculated_df...")
# preprocess_and_analyze(calculated_df, 'calculated_df')