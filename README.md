# Multi-Stock Performance Analysis Dashboard

## Project Overview
This project focuses on extracting, transforming, and visualizing time-series stock market data from multiple disparate sources. The goal is to provide a unified dashboard that allows users to analyze historical price trends and compare market performance across different tickers.

## Features
* **Dynamic Time-Series Chart:** Visualizes closing prices for multiple stocks over a 2-year period.
* **Interactive Slicer:** Allows users to filter specific stock symbols for isolated analysis.
* **Key Metric Card:** Displays the Average Closing Price dynamically based on the user's selection.
* **Data Integration:** Combines individual YAML-based stock records into a consolidated Power BI dataset.

## Technical Workflow
1. **Data Extraction:** Raw stock data was extracted from multiple YAML/CSV files.
2. **Data Cleaning:** Handled missing values and ensured the "Close" price columns were formatted as Decimal Numbers for calculation.
3. **Visualization:** Built using Power BI Desktop, utilizing Line Charts for trend analysis and Slicers for interactivity.

## Key Insights
* The dashboard identifies the most volatile stocks based on price fluctuations.
* Users can compare the growth of high-cap stocks versus mid-cap stocks within the same timeframe.