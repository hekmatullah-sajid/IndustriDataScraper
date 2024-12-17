import pandas as pd

# Load the dataset into a DataFrame
df = pd.read_csv('../../data/cleaned/cleaned_companies_data.csv')

# Define a dictionary for exchange currency rates to Euros (we have only three currencies), as of 05.09.2023
exchange_rates = {
    'USD': 0.93,  # exchange rate for USD to EUR
    'EUR': 1.0,   # EUR to EUR (1:1)
    'CHF': 1.05,  # exchange rate for CHF to EUR
}
# Convert 'net_assets' to Euros based on exchange rates
# If currency not found in the exchange_rates, then no conversion
df['net_assets'] = df.apply(lambda row: row['net_assets'] * exchange_rates.get(row['net_assets_currency'], 1.0), axis=1)

# Calculate the number of null values for each of the 4 columns
null_counts = df[['year_founded', 'employees', 'net_assets', 'net_assets_year']].isnull().sum()

# Create a DataFrame and transpose it, to appened it as a row to statistics
null_counts_df = pd.DataFrame(null_counts, columns=['null values count']).T

# Compute summary statistics for the desired 4 numeric columns
summary_stats = df[['year_founded', 'employees', 'net_assets', 'net_assets_year']].describe()

# Apppend the null counts as a row to summary_stats
summary_stats = pd.concat([summary_stats, null_counts_df])

# Save the summary statistics to a file
summary_stats.to_csv('../../data/cleaned/summary_statistics.csv')

print("summary statistics are ready in 'summary_statistics.csv' file")