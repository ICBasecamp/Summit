import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import json

# Load economic indicators data
with open('economic_indicators.json', 'r') as f:
    economic_indicators = json.load(f)

# Convert economic indicators to DataFrame
econ_df = pd.DataFrame(economic_indicators)

# Load earnings data (replace with actual data loading code)
earnings_df = pd.read_csv('earnings_data.csv')

# Merge economic indicators with earnings data
merged_df = pd.merge(earnings_df, econ_df, left_on='date', right_on='date', how='left')

# Define the target variable and predictor variables
target_variable = 'target_metric'
predictor_variables = econ_df.columns

# Perform Granger Causality test
max_lag = 4
results = {}
for predictor in predictor_variables:
    test_result = grangercausalitytests(merged_df[[target_variable, predictor]], max_lag, verbose=False)
    results[predictor] = test_result

# Save Granger Causality test results to a JSON file
with open('granger_causality_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Granger Causality test completed.")