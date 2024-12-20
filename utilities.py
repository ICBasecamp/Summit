import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

def convert_to_number(value):
    if isinstance(value, str):
        if 'B' in value:
            return float(value.replace('B', '')) * 1e9
        elif 'T' in value:
            return float(value.replace('T', '')) * 1e12
        elif 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'K' in value:
            return float(value.replace('K', '')) * 1e3
        elif '%' in value:
            return float(value.replace('%', '')) / 100
    return float(value)

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
    
# PCA for Dimensionality Reduction
def pca_dimensionality_reduction(X_df, n_components=3):
    X = X_df.select_dtypes(include=[np.number])
    pca = PCA(n_components=n_components)
    
    pca_df = pd.DataFrame(pca.components_.T, index=X.columns, columns=[f'PC{i+1}' for i in range(n_components)])
    
    return pca_df