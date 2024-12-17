import pandas as pd
from preprocess_functions import remove_name, format_clean_phone, get_year, extract_employees_number, process_website, process_net_asset_field

# Load the company data from CSV
df = pd.read_csv("../../data/raw/companies_data.csv")

# Remove duplicate records
df = df.drop_duplicates()

# Fill missing values with default null values based on column datatypes
df.fillna(pd.NA, inplace=True)

# Remove the company name from the address field using the remove_name function (applied row-wise)
df['address'] = df.apply(remove_name, axis= 1)

# Remove records that have 3 or fewer fields; these rows have no data in Daten und Kontake setction
df = df.dropna(thresh=3)

# Clean phone and fax numbers: remove non-digit characters and add "+49" country code if not present
df['phone'] = df['phone'].apply(format_clean_phone)
df['fax'] = df['fax'].apply(format_clean_phone)
df['phone'] = df['phone'].astype('str')
df['fax'] = df['fax'].astype('str')


# Extract the year of foundation from the "year_founded" column and convert it to an integer
df['year_founded'] = df['year_founded'].apply(lambda m: get_year(m) if pd.notna(m) else m)
df['year_founded'] = df['year_founded'].astype('Int64')

# Extract the number of employees from the "employees" column and convert it to an integer
df['employees'] = df['employees'].apply(lambda m: extract_employees_number(m) if pd.notna(m) else m)
df['employees'] = df['employees'].astype('Int64')

# Process the website column to make sure it follows a consistent format
df['website'] = df['website'].apply(process_website)

# Apply the process_net_asset_field function to extract monetary values and move the currency symbol and year of net assets to new column respectively 
df = df.apply(lambda row: process_net_asset_field(row) if pd.notna(row['net_assets']) else row, axis=1)


# Reorder the columns for consistent column order
column_order = [
    'name', 'city', 'address', 'website', 'email', 'phone', 'fax',
    'employees', 'year_founded', 'net_assets', 'net_assets_currency', 'net_assets_year'
]
df = df[column_order]

# Save the cleaned data to a new CSV file
df.to_csv("../../data/clean/cleaned_companies_data.csv", index=False)

print("Clean data file 'cleaned_companies_data.csv' has been generated successfully!")
