import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from earnings.FinancialStats import main as calculate_metrics
from utilities import convert_to_number
from earnings.AnalysisStats import main as calculate_stats
import concurrent.futures
import asyncio

async def getDataframes(ticker):
    dataframes = await calculate_stats(ticker)
    np.random.seed(42)

    await calculate_metrics(ticker)

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

    return dataframes_list

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
    
    # Ensure all dataframes have matching dimensions
    if preprocessed_df.shape[1] != len(feature_names):
        return results
    
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
    
    # Reduced parameter grid for smaller datasets
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 15],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 5],
        'max_features': ['sqrt', 'log2'],
        'bootstrap': [True, False]
    }
        
    def random_forest_feature_importance(X_df, target_variable):
        if target_variable in X_df:
            y = X_df[target_variable]
            X = X_df.drop(columns=[target_variable], errors='ignore')
        else:
            return pd.DataFrame()
        
        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error')
        grid_search.fit(X, y)
        
        best_rf = grid_search.best_estimator_
        feature_importances = pd.DataFrame(best_rf.feature_importances_, index=X.columns, columns=['Importance'])
        return feature_importances.sort_values('Importance', ascending=False)
    
    rf_importances = random_forest_feature_importance(X_df, target_variable)
    
    if rf_importances.empty:
        return results
    
    # PCA for Dimensionality Reduction
    def pca_dimensionality_reduction(X_df, n_components=3):
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(X_df)
        pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)], index=X_df.index)
        return pca_df
    
    if name == 'earnings_df' or name == 'eps_trend_df' or name == 'revenue_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 3)
    elif name == 'earnings_history_df':
        pca_df = pca_dimensionality_reduction(preprocessed_df, 2)
    
    results['random_forest_importances'] = rf_importances.to_dict()
    results['pca_components'] = pca_df.to_dict()
    
    return results

async def main(ticker):
    dataframes_list = await getDataframes(ticker)    
    all_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(preprocess_and_analyze, df, name) for df, name in dataframes_list]
        for future in concurrent.futures.as_completed(futures):
            all_results.append(future.result())

    # Save the results to a dictionary
    statistical_results = {
        'results': all_results
    }

    return statistical_results