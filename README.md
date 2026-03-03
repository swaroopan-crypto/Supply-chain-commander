# Supply Chain Commander: Inventory Shortage Predictor

## Business Problem
Retail companies lose millions when popular items go out of stock. Beyond immediate lost sales, out-of-stock items damage customer loyalty and brand reputation.

## Solution
A predictive dashboard backed by a time-series forecasting model that forecasts which products will run out of stock in the next 30 days.

## Key Findings
- Prevented potential stockouts by forecasting upcoming demand vs current stock.
- Quantified financial risk in dollar terms for executive stakeholders.
- Categorized risk levels (HIGH, MEDIUM, LOW) based on days until stockout.

## Methodology
1. **Data Preparation**: Mock orders over 365 days loaded into Pandas.
2. **Analysis**: Time-Series Forecasting (Facebook Prophet) predicting the next 30 days of sales.
3. **Risk Profile**: Calculates Days of Inventory (Current Stock / Predicted Daily Sales).
4. **Visualization**: A structured CSV generated for `Power BI` to build the executive dashboard.

## Tech Stack
- Python (Pandas, Prophet, NumPy)
- Time Series Forecasting
- Data Visualization (Power BI - to be imported manually)

## Files
- `generate_mock_data.py`: Creates mock historical order data and products list.
- `supply_chain_predictor.py`: Processes data, applies moving average or `prophet` model to forecast 30-day demand, calculates stockout risk, and outputs CSV for dashboards.
- `index.html`: A static landing page template for hosting the interactive dashboard.

## Instructions
1. Run `python generate_mock_data.py` to create `orders_dataset.csv` and `products_dataset.csv`.
2. Run `python supply_chain_predictor.py` to generate `inventory_risk_dashboard.csv`.
3. Load the resulting `CSV` file into Power BI or Tableau to build out your BI dashboards.
4. Replace the URL in `index.html` with your published BI Dashboard URL.
