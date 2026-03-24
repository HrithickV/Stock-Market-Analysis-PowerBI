import sqlite3
import pandas as pd

# Path to your database
db_path = '/Users/hrithick/Desktop/Stock_Analysis_Project/nifty50.db'
conn = sqlite3.connect(db_path)

# Fetch and Merge
prices_df = pd.read_sql_query("SELECT * FROM stock_prices", conn)
sector_df = pd.read_sql_query("SELECT * FROM stock_sectors", conn)
final_df = prices_df.merge(sector_df, on='Ticker')

# Save to your Desktop for easy finding
final_df.to_excel('/Users/hrithick/Desktop/Stock_Analysis_Project/PowerBI_Data.xlsx', index=False)

conn.close()
print("Check your folder! PowerBI_Data.xlsx is ready.")