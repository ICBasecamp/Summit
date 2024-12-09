import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error
from calculations import main as calculate_metrics, convert_to_number
from EarningsReports import dataframes
import concurrent.futures

# Set random seed for reproducibility
np.random.seed(42)

# Load the calculated values from calculations.py
calculated_values = calculate_metrics()

# Load the raw data from EarningsReports.py
earnings_df = dataframes['earnings_df']
revenue_df = dataframes['revenue_df']
earnings_history_df = dataframes['earnings_history']
eps_trend_df = dataframes['eps_trend_df']
analyst_price_targets_df = dataframes['analyst_price_targets_df']

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

# Combine calculations into a DataFrame
calculations_df = pd.DataFrame({
    'EPS Growth': [calculated_values['eps_growth']],
    'Revenue Growth': [calculated_values['revenue_growth']],
    'Profit Margin': [calculated_values['profit_margin']],
    'EPS Estimate Spread': [calculated_values['eps_estimate_spread']],
    'Revenue Estimate Spread': [calculated_values['revenue_estimate_spread']],
    'P/E Ratio': [calculated_values['pe_ratio']]
})

# Function to preprocess and analyze the combined dataframe
def preprocess_and_analyze(df, name):
    results = []
    
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
        results.append(f"No numeric features found in {name}. Skipping.")
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
        results.append(f"Preprocessed DataFrame for {name} is empty after preprocessing. Skipping.")
        return results
    
    # Check for NaNs and Infinities
    if X_df.isnull().values.any() or np.isinf(X_df.values).any():
        results.append(f"NaNs or Infinities found in {name}. Skipping.")
        return results
    
    # Print data summary for debugging
    results.append(f"Data summary for {name}:\n{X_df.describe()}")
    
    # Random Forest Feature Importance with GridSearchCV
    def random_forest_feature_importance(X_df, target_variable):
        if target_variable in X_df:
            y = X_df[target_variable]
            X = X_df.drop(columns=[target_variable], errors='ignore')
        else:
            results.append(f"No target variable '{target_variable}' found in the DataFrame. Skipping.")
            return pd.DataFrame()
        
        results.append(f"Target variable '{target_variable}' found. Proceeding with GridSearchCV.")
        results.append(f"Features: {X.columns.tolist()}")
        results.append(f"Target: {y.name}")
        
        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error')
        grid_search.fit(X, y)
        
        best_rf = grid_search.best_estimator_
        feature_importances = pd.DataFrame(best_rf.feature_importances_, index=X.columns, columns=['Importance'])
        return feature_importances.sort_values('Importance', ascending=False)
    
    # PCA for Dimensionality Reduction
    def pca_dimensionality_reduction(X_df, n_components=3):
        X = X_df.select_dtypes(include=[np.number])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(X_scaled)
        
        pca_df = pd.DataFrame(pca.components_.T, index=X.columns, columns=[f'PC{i+1}' for i in range(n_components)])
        
        return pca_df
    
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
        results.append(f"Skipping PCA and cross-validation for {name} due to empty feature importances.")
        return results
    
    if name == 'earnings_df' or name == 'eps_trend_df' or name == 'revenue_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 3)
    elif name == 'earnings_history_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 2)
    
    results.append(f"Random Forest Feature Importances for {name}:\n{rf_importances}")
    results.append(f"PCA DataFrame for {name}:\n{pca_df}")

    # Cross-Validation for Model Evaluation
    def cross_validate_model(model, X, y):
        n_splits = min(5, len(X))  # Ensure n_splits is not greater than the number of samples
        if n_splits < 2:
            results.append("Not enough samples for cross-validation. Skipping.")
            return float('nan'), float('nan')  # Return NaN if not enough samples for cross-validation
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, cv=kf, scoring=make_scorer(mean_squared_error))
        return scores.mean(), scores.std()

    # Cross-validate models
    X = preprocessed_df
    y = X_df[target_variable] if target_variable in X_df else np.random.rand(len(preprocessed_df))  # Dummy target variable for cross-validation
    rf_mean, rf_std = cross_validate_model(RandomForestRegressor(n_estimators=100, random_state=42), X, y)
    
    if not np.isnan(rf_mean):
        results.append(f"Random Forest CV Mean MSE: {rf_mean:.4f}, Std: {rf_std:.4f}")
    
    return results

# Analyze each dataframe separately in parallel
all_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(preprocess_and_analyze, df, name) for df, name in dataframes_list]
    for future in concurrent.futures.as_completed(futures):
        all_results.extend(future.result())

# Print all results sequentially
for result in all_results:
    print(result)