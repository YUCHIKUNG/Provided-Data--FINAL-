import pandas as pd
import numpy as np
import glob

# Update path to current directory
csv_files = glob.glob('*.csv')  # Searches for all CSV files in the current directory
df_list = []

# Reading in the CSV files
for file in csv_files:
    try:
        df = pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file, encoding='ISO-8859-1')
    df_list.append(df)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Ensure 'Sent Date' is converted to datetime
df['Sent Date'] = pd.to_datetime(df['Sent Date'])

# Calculate Item Counts and Percentages
item_counts = df['Parent Menu Selection'].value_counts()
item_percentages = (item_counts / item_counts.sum()) * 100

# Map Item Count and Item Percentage back to the DataFrame
df['Item Count'] = df['Parent Menu Selection'].map(item_counts)
df['Item Percentage'] = df['Parent Menu Selection'].map(item_percentages)

# Extract date-related features
df['Day of Week'] = df['Sent Date'].dt.dayofweek  # Monday=0, Sunday=6
df['Month'] = df['Sent Date'].dt.month  # 1=January, 12=December
df['Hour of Day'] = df['Sent Date'].dt.hour  # 0-23 hours
df['Weekday Name'] = df['Sent Date'].dt.day_name()  # Full name of the weekday

# Define cheese categories based on the Modifier or Option Group Name
def cheese_category(modifier):
    if 'Cheddar' in modifier:
        return 'Cheddar'
    elif 'Pepper Jack' in modifier:
        return 'Pepper Jack'
    elif 'Alfredo' in modifier:
        return 'Alfredo'
    else:
        return 'Other'

menu_prices = {
    "Mac and Cheese": 8.99,
    "Grilled Cheese Sandwich":8.99
}
modifier_prices = {
    "Regular": 0,
    "No Drink": 0,
    "Water Bottle": 1.49,
    "Apple Juice": 2.49,
    "Coke": 1.99,
    "Dr. Pepper": 1.99,
    "Sprite": 1.99,
    "Diet Coke": 1.99,
    "Powerade (Blue Mountain Berry Blast)": 1.99,
    "Minute Maid Lemonade": 1.99,
    "No Side": 0,
    "Garlic Bread": 1.99,
    "Cheesy Garlic Bread": 1.99,
    "Large Chocolate Chunk Cookie": 4.99,
    "Cheesecake": 4.99,
    "Doritos": 1.99,
    "Cheetos": 1.99,
    "Lays Barbecue": 1.99,
    "Lays Classic": 1.99,
    "Cheddar Mac": 1.99,
    "Pepper Jack Mac": 1.99,
    "Alfredo Mac": 1.99,
    "No Meat": 0,
    "Grilled Chicken (Contains Gluten)": 1.99,
    "Pulled Pork": 1.99,
    "Brisket": 1.99,
    "Bacon": 1.99,
    "Ham": 1.99
}
df['Cheese Category'] = df['Modifier'].apply(cheese_category)

# Add the cost of the Parent Menu Selection
df['Base Cost'] = df['Parent Menu Selection'].map(menu_prices)

# Add the cost for the Modifier, if it exists (assuming Modifier is a column in your data)
df['Modifier Cost'] = df['Modifier'].map(modifier_prices).fillna(0)

# Calculate total cost by adding base cost and modifier cost
df['Total Cost'] = df['Base Cost'] + df['Modifier Cost']

# Drop any rows with missing values (if applicable)
df_cleaned = df.dropna()

# Save the cleaned DataFrame to a CSV
df_cleaned.to_csv('Combinedata.csv', index=False)
