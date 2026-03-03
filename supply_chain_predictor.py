import pandas as pd
import numpy as np
from datetime import timedelta
import os

# Try to import prophet for actual time-series analysis
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False
    print("Warning: facebook 'prophet' module is not installed. Falling back to simple moving average for forecasting.")

def execute_forecast(orders_file='orders_dataset.csv', products_file='products_dataset.csv'):
    if not os.path.exists(orders_file) or not os.path.exists(products_file):
        print(f"Error: Required datasets missing. Please run generate_mock_data.py first.")
        return
        
    print("Loading data...")
    orders = pd.read_csv(orders_file)
    products = pd.read_csv(products_file)
    
    # Cleaning
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders = orders[orders['order_status'] == 'delivered']
    
    min_date = orders['order_purchase_timestamp'].min()
    max_date = orders['order_purchase_timestamp'].max()
    total_days = (max_date - min_date).days
    
    # Calculate Velocity
    print(f"Calculating velocity across {total_days} days...")
    product_sales = orders.groupby('product_id').agg(
        total_orders=('order_id', 'count')
    ).reset_index()
    product_sales['total_quantity'] = product_sales['total_orders']  # Assume 1 item per order
    product_sales['daily_velocity'] = product_sales['total_quantity'] / total_days
    
    # Join category and price
    product_sales = product_sales.merge(products[['product_id', 'product_category_name', 'price']], on='product_id')
    
    inventory_data = []
    
    print(f"Starting 30-day forecast for top {len(product_sales)} products...")

    # Forecasting & Risk
    for _, row in product_sales.iterrows():
        product_id = row['product_id']
        daily_vel = row['daily_velocity']
        avg_price = row['price']
        
        # Get orders for this product
        product_df = orders[orders['product_id'] == product_id].copy()
        
        # Aggregate by date
        product_df['date'] = product_df['order_purchase_timestamp'].dt.date
        daily_sales = product_df.groupby('date').size().reset_index()
        daily_sales.columns = ['ds', 'y']
        
        predicted_30day_sales = 0
        
        if HAS_PROPHET:
            # fill missing dates with 0
            date_range = pd.date_range(daily_sales['ds'].min(), daily_sales['ds'].max())
            daily_sales['ds'] = pd.to_datetime(daily_sales['ds'])
            full_data = pd.DataFrame({'ds': date_range})
            full_data = full_data.merge(daily_sales, on='ds', how='left').fillna(0)
            
            # Use Prophet
            model = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
            model.fit(full_data)
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)
            predicted_30day_sales = forecast.tail(30)['yhat'].sum()
        else:
            # Fallback naive 30 day forecast just based on average velocity
            predicted_30day_sales = daily_vel * 30.0
            
        # Simulate current stock (let's randomly assign current stock based on daily velocity)
        # Some are fully stocked, some are low
        current_stock = daily_vel * np.random.uniform(10, 60)
        
        days_until_stockout = current_stock / daily_vel if daily_vel > 0 else 999
        
        if days_until_stockout < 30:
            risk = "HIGH RISK"
        elif days_until_stockout < 60:
            risk = "MEDIUM RISK"
        else:
            risk = "LOW RISK"
            
        # Lost revenue if stockout in < 30 days
        lost_revenue = 0
        if days_until_stockout < 30:
            days_of_lost_sales = 30 - days_until_stockout
            lost_quantity = daily_vel * days_of_lost_sales
            lost_revenue = lost_quantity * avg_price
            
        inventory_data.append({
            'product_id': product_id,
            'category': row['product_category_name'],
            'price': row['price'],
            'current_stock': round(current_stock),
            'predicted_30day_sales': round(predicted_30day_sales),
            'days_until_stockout': round(days_until_stockout),
            'risk_level': risk,
            'potential_lost_revenue': round(lost_revenue, 2)
        })
        
    df_inventory = pd.DataFrame(inventory_data)
    total_risk_revenue = df_inventory['potential_lost_revenue'].sum()
    
    print(f"\n--- Forecast Summary ---")
    print(f"Total at-risk revenue: ${total_risk_revenue:,.2f}")
    
    high_risk_count = len(df_inventory[df_inventory['risk_level'] == 'HIGH RISK'])
    print(f"High risk products (Stockout < 30 days): {high_risk_count}")
    
    # Output to CSV for Power BI Dashboard
    csv_out = 'inventory_risk_dashboard.csv'
    df_inventory.to_csv(csv_out, index=False)
    print(f"\nSaved dashboard input to '{csv_out}'. Load this into Power BI/Tableau for the visualizations.")
    
if __name__ == '__main__':
    execute_forecast()
