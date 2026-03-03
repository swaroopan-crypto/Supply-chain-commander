import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_supply_data(orders_file='orders_dataset.csv', products_file='products_dataset.csv'):
    np.random.seed(42)
    n_days = 365
    n_products = 50
    start_date = datetime(2025, 1, 1)
    
    products_data = []
    # Create some top 50 products
    for i in range(1, n_products + 1):
        cat = np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Toys'])
        price = round(np.random.uniform(10.0, 500.0), 2)
        products_data.append({
            'product_id': f'SKU_{i:03d}',
            'product_category_name': cat,
            'price': price
        })
        
    df_products = pd.DataFrame(products_data)
    df_products.to_csv(products_file, index=False)
    
    # Generate orders over the last 365 days
    orders_data = []
    for product in products_data:
        prod_id = product['product_id']
        # Give each product a base daily demand curve that might be seasonal
        base_demand = np.random.uniform(5, 50)
        trend = np.random.uniform(-0.02, 0.05) # Growth or drop per day
        # Simulate over 365 days
        for day in range(n_days):
            current_date = start_date + timedelta(days=day)
            
            # Simulated demand using a sine wave + trend
            day_seasonality = np.sin(day * (2 * np.pi / 365)) * (base_demand * 0.3)
            current_demand = max(0, base_demand + (day * trend) + day_seasonality + np.random.normal(0, 5))
            
            n_orders_today = int(current_demand)
            for _ in range(n_orders_today):
                orders_data.append({
                    'order_id': f'ORD_{np.random.randint(100000, 999999)}',
                    'product_id': prod_id,
                    'order_purchase_timestamp': current_date + timedelta(hours=np.random.randint(0, 24)),
                    'order_status': 'delivered'
                })
                
    df_orders = pd.DataFrame(orders_data)
    df_orders.to_csv(orders_file, index=False)
    print(f"Generated {products_file} with {n_products} products.")
    print(f"Generated {orders_file} with {len(df_orders)} mock orders.")

if __name__ == '__main__':
    generate_supply_data()
