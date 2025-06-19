import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


NUM_ROWS = 3000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 9, 30)
OUTPUT_FILENAME = 'data.csv'


ADVISORS = ['Adam', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace']
REGIONS_CITIES_MAP = {
    'Europe': ['London', 'Paris', 'Berlin', 'Madrid', 'Rome'],
    'Asia': ['Tokyo', 'Singapore', 'Hong Kong', 'Shanghai'],
    'America': ['New York', 'Toronto', 'Los Angeles', 'Buenos Aires'],
    'Africa': ['Cairo', 'Lagos', 'Johannesburg']
}

CITIES = [city for cities in REGIONS_CITIES_MAP.values() for city in cities]
CITY_TO_REGION = {city: region for region, cities in REGIONS_CITIES_MAP.items() for city in cities}

data = {
    'Advisor': np.random.choice(ADVISORS, NUM_ROWS),
    'Location': np.random.choice(CITIES, NUM_ROWS)
}
df = pd.DataFrame(data)
df['Region'] = df['Location'].map(CITY_TO_REGION)

print(f"Generated {len(df)} rows of categorical data.")

# --- 4. Generate Numerical Monthly Columns ---
# Create a date range for all months from Jan 2022 to Sep 2024
month_range = pd.to_datetime(pd.date_range(start=START_DATE, end=END_DATE, freq='MS'))

for month_start in month_range:
    month_name = month_start.strftime('%b %y') # e.g., Jan 22
    sales_col_name = f'Sales {month_name}'
    trades_col_name = f'Trades {month_name}'
    potential_sales = np.random.uniform(0, 999999.99, NUM_ROWS).round(2)
    potential_trades = np.random.randint(0, 100, NUM_ROWS)
    df[sales_col_name] = potential_sales
    df[trades_col_name] = potential_trades

print(f"Generated monthly Sales and Trades columns from {month_range[0].strftime('%b %Y')} to {month_range[-1].strftime('%b %Y')}.")


# Save the DataFrame to a CSV file
df.to_csv(OUTPUT_FILENAME, index=False)

print("\n--- Process Complete ---")
print(f"DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns.")
print(f"Data successfully saved to '{OUTPUT_FILENAME}'.")

# Display a sample of the final data
print("\nSample of the generated data:")
print(df.head())
