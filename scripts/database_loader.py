import pandas as pd
import os
import glob
import sqlite3

# SETUP THE DATABASE FILE PATH
# This creates a file named 'nifty50.db' on your Desktop
db_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/nifty50.db'
conn = sqlite3.connect(db_path)

# SOURCE DATA PATH
processed_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/data/processed'

# UPLOAD SECTOR MAPPING
print("--- Phase 1: Uploading Sector Data ---")
try:
    sector_df = pd.read_csv(os.path.join(processed_path, 'cleaned_sectors.csv'))
    # 'replace' ensures we have a fresh table every time we run the script
    sector_df.to_sql('stock_sectors', conn, if_exists='replace', index=False)
    print("Sector Mapping table created in SQLite.")
except Exception as e:
    print(f"Error uploading sectors: {e}")

# UPLOAD 50 STOCK PRICE FILES
print("\n--- Phase 2: Uploading Stock Price Files ---")
csv_files = glob.glob(os.path.join(processed_path, '*.csv'))
upload_count = 0

for file in csv_files:
    # We only want the individual stock files, not the sector file again
    if 'cleaned_sectors' in file: 
        continue
    
    ticker = os.path.basename(file).replace('.csv', '')
    df = pd.read_csv(file)
    
    # We add a 'Ticker' column so we can tell stocks apart in one big table
    df['Ticker'] = ticker
    
    # We 'append' so all 50 files end up in the SAME table named 'stock_prices'
    df.to_sql('stock_prices', conn, if_exists='append', index=False)
    upload_count += 1
    print(f"[{upload_count}/50] Loaded: {ticker}")

conn.close()
print(f"\n SUCCESS! Database ready at: {db_path}")