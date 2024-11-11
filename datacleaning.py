import pandas as pd
import glob

# Function to load and combine CSV files
def load_and_combine_csvs(csv_path_pattern='*.csv'):
    # Get all CSV file paths matching the pattern
    csv_files = glob.glob(csv_path_pattern)
    
    if not csv_files:
        raise FileNotFoundError("No CSV files found with the given pattern.")
    
    # Read and combine all CSV files into one DataFrame
    df_list = []
    for file in csv_files:
        try:
            df_list.append(pd.read_csv(file, encoding='ISO-8859-1'))  # Specify encoding here
        except UnicodeDecodeError as e:
            print(f"Error reading file {file}: {e}")
            continue
    
    if not df_list:
        raise ValueError("No files were successfully read.")
    
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df


# Function to preprocess the DataFrame
def preprocess_data(df):
    # Ensure 'Sent Date' is parsed as datetime
    df['Sent Date'] = pd.to_datetime(df['Sent Date'], errors='coerce')
    
    # Drop rows where 'Sent Date' could not be parsed (NaT)
    df = df.dropna(subset=['Sent Date'])
    
    # Calculate Item Counts and Percentages
    item_counts = df['Parent Menu Selection'].value_counts()
    item_percentages = (item_counts / item_counts.sum()) * 100
    df['Item Count'] = df['Parent Menu Selection'].map(item_counts)
    df['Item Percentage'] = df['Parent Menu Selection'].map(item_percentages)

    # Extract date-related features
    df['Day of Week'] = df['Sent Date'].dt.dayofweek
    df['Weekday Name'] = df['Sent Date'].dt.day_name()
    df['Month'] = df['Sent Date'].dt.month
    df['Month Name'] = df['Sent Date'].dt.month_name()
    df['Hour of Day'] = df['Sent Date'].dt.hour
    
    # Define cheese categories based on the Modifier column (handle missing values)
    df['Cheese Category'] = df['Modifier'].fillna('').apply(lambda modifier: 'Cheddar' if 'Cheddar' in modifier else 
                                                 'Pepper Jack' if 'Pepper Jack' in modifier else 
                                                 'Alfredo' if 'Alfredo' in modifier else 'Other')

    return df

# Define menu and modifier prices
menu_prices = {
    "Mac and Cheese": 8.99,
    "Grilled Cheese Sandwich": 8.99
}
modifier_prices = {
    "Regular": 0, "No Drink": 0, "Water Bottle": 1.49, "Apple Juice": 2.49,
    "Coke": 1.99, "Dr. Pepper": 1.99, "Sprite": 1.99, "Diet Coke": 1.99,
    "Powerade (Blue Mountain Berry Blast)": 1.99, "Minute Maid Lemonade": 1.99,
    "No Side": 0, "Garlic Bread": 1.99, "Cheesy Garlic Bread": 1.99,
    "Large Chocolate Chunk Cookie": 4.99, "Cheesecake": 4.99, "Doritos": 1.99,
    "Cheetos": 1.99, "Lays Barbecue": 1.99, "Lays Classic": 1.99,
    "Cheddar Mac": 1.99, "Pepper Jack Mac": 1.99, "Alfredo Mac": 1.99,
    "No Meat": 0, "Grilled Chicken (Contains Gluten)": 1.99,
    "Pulled Pork": 1.99, "Brisket": 1.99, "Bacon": 1.99, "Ham": 1.99
}

# Function to calculate cost-related columns
def calculate_costs(df):
    # Add the cost of the Parent Menu Selection, handle missing menu item cases
    df['Base Cost'] = df['Parent Menu Selection'].map(menu_prices).fillna(0)

    # Add the cost for the Modifier, if it exists
    df['Modifier Cost'] = df['Modifier'].map(modifier_prices).fillna(0)

    # Calculate total cost by adding base cost and modifier cost
    df['Total Cost'] = df['Base Cost'] + df['Modifier Cost']
    
    return df

# Function to save the cleaned data to a new CSV
def save_to_csv(df, filename='Combinedata.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main script execution
if __name__ == "__main__":
    try:
        # Step 1: Load and combine the CSV files
        combined_df = load_and_combine_csvs()
        
        # Step 2: Preprocess the data
        preprocessed_df = preprocess_data(combined_df)
        
        # Step 3: Calculate cost-related columns
        final_df = calculate_costs(preprocessed_df)
        
        # Step 4: Save the cleaned DataFrame to a CSV file
        save_to_csv(final_df)
    
    except Exception as e:
        print(f"Error occurred: {e}")
