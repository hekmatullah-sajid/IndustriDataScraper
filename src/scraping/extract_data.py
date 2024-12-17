from scraping_functions import get_company_list  # Import the function for scraping company data
import pandas as pd

# Scrape company data from the specified URL
company_data = get_company_list("https://industrie.de/firmenverzeichnis", "infoservice-entry-holder", "meta-small")

# Filename for the CSV file to store the extracted data
filename = "../../data/raw/companies_data.csv"

# Create a Pandas DataFrame from the scraped company data
df = pd.DataFrame(company_data)

# Create a dictionary to map an icon's CSS class name to a human-readable filed name.
icon_name_dict = {
    'fa-globe': 'website',
    'fa-envelope': 'email',
    'fa-phone': 'phone',
    'fa-fax': 'fax',
    'fa-group': 'employees',
    'fa-flag': 'year_founded',
    'fa-money': 'net_assets',
    'fa-map-pin': 'address'
}

# Rename DataFrame columns using the icon_name_dict
df.rename(columns=icon_name_dict, inplace=True)

# Save the DataFrame to a CSV file, excluding the index column
df.to_csv(filename, index=False)

print("Data successfully extracted and saved to the output CSV file.")
