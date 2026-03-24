import yaml
import pandas as pd
import os
from glob import glob

# 1. SETUP PATHS
raw_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/data/raw'
processed_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/data/processed'

# 2. FILE DISCOVERY
# This finds every .yaml file inside any subfolder (like 2023-10)
yaml_files = glob(os.path.join(raw_path, '**/*.yaml'), recursive=True)
all_rows = []

print(f"Starting Extraction: Found {len(yaml_files)} files.")

# 3. EXTRACTION LOOP
for file_path in yaml_files:
    # INSIGHT: Data Cleaning at the source
    # We slice the first 10 characters of the filename to get 'YYYY-MM-DD'
    filename = os.path.basename(file_path)
    clean_date = filename[:10] 
    
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            if data:
                for entry in data:
                    # Adding the clean date back into each stock's record
                    entry['date'] = clean_date
                    all_rows.append(entry)
    except Exception as e:
        print(f"Error in {filename}: {e}")

# 4. TRANSFORMATION TO DATAFRAME
df = pd.DataFrame(all_rows)

# 5. ORGANIZATION BY SYMBOL
# We find every unique Ticker (Reliance, Axis, etc.)
tickers = df['Ticker'].unique()

for ticker in tickers:
    # Filter data for just this ticker and sort it chronologically
    ticker_df = df[df['Ticker'] == ticker].sort_values(by='date')
    
    # INSIGHT: Saving as individual CSVs for 'Maintainability'
    ticker_df.to_csv(f"{processed_path}/{ticker}.csv", index=False)

print(f"Step 1 Complete: 50 CSV files generated.")