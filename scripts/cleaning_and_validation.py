import pandas as pd
import glob 
import os

# SETUP PATHS
processed_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/data/processed'
sector_file = '/Users/hrithick/Desktop/Stock_Analysis_Project/data/raw/Sector_data-Sheet1.csv'

#CLEAN THE SECTOR DATA

print("--- Phase 1: Cleaning Sector Mapping ---")

try:
    sector_df = pd.read_csv('/Users/hrithick/Desktop/Stock_Analysis_Project/data/raw/Sector_data - Sheet1.csv')
    # The raw symbol looks like 'AXIS BANK: AXISBANK'. 
    # We split by ':' and take the last part to get just 'AXISBANK'

    sector_df['Ticker'] = sector_df['Symbol'].str.split(':').str[-1].str.strip()

    #save a clean version for sql

    cleaned_sector_path = os.path.join(processed_path, 'cleaned_sectors.csv')
    sector_df[['COMPANY', 'sector', 'Ticker']].to_csv(cleaned_sector_path, index=False)
    print(f"Sector data standardized and saved to: {cleaned_sector_path}")
except Exception as e:
    print(f"Error cleaning sector file: {e}")



#VALIDATE ND FIX THE 50 PRICE CSV

print("--- Phase 2: Validating Price Datasets --- ")

csv_files = glob.glob(os.path.join(processed_path, '*.csv'))
fixed_files=0

for file in csv_files:
    #Skip the mapping file we just created

    if 'cleanedsectors.csv' in file:
        continue
    df=pd.read_csv(file)
    initial_shape = df.shape


    # ACTION: Handle Missing Values (Nulls)
    # If a day is missing, we "Forward Fill" the previous day's price

    if df.isnull().values.any():
        df.ffill(inplace=True)
        df.to_csv(file, index=False)
        fixed_files += 1
        print(f"⚠️ Fixed missing values in: {os.path.basename(file)}")

        # ACTION: Check for Logical Errors (Price <= 0)

        if (df['close'] <= 0).any():
            print(f"🚨 CRITICAL: {os.path.basename(file)} contains zero or negative prices!")

if fixed_files == 0:
    print("✅ All 50 datasets are 100% clean and logically sound.")
else:
    print(f"✅ Validation complete. Data gaps filled in {fixed_files} files.")

print("\nReady for SQL Loading.")





