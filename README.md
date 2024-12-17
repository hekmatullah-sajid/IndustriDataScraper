# IndustriDataScraper

# Data Extraction and Analysis Project

## Overview

This project focuses on extracting and analyzing company data from the website [industrie.de Firmenverzeichnis](https://industrie.de/firmenverzeichnis/). The main goal is to collect details about companies listed under the "Daten und Kontakte" section, including company names, URLs, cities, and contact information.

## Data Extraction

### Webpage Structure
- Company data is extracted from pages containing the "Daten und Kontakte" section.
- Information is gathered from the div with the class `infoservice-entry-holder`, which includes the company name, city, and the URL to the detailed page.

### Key Extraction Steps
1. **Initial Extraction**: Extract company name, URL, and city from the `infoservice-entry-holder`.
2. **Detailed Data**: Extract contact details from `dl`, `dt`, and `dd` HTML elements in the "Daten und Kontakte" section.
3. **Address Handling**: Address parts are concatenated with spaces.
4. **Data Storage**: Results are saved in a CSV file (`companies_data.csv`).

## Data Preprocessing

### Key Steps:
- **Handling Sparse Data**: The preprocessing function skips columns with null values.
- **Duplicate Removal**: Duplicates are removed for data accuracy.
- **Address Cleanup**: Company names are removed from address fields.
- **Phone Number Formatting**: Non-numeric characters are cleaned, and German numbers are prefixed with `+49`.
- **Year and Employee Data**: Extract and clean number of employees and year of foundation.
- **Website Standardization**: Protocols are removed, and missing "www" is added.
- **Net Assets Cleanup**: Extract financial data, handle currency, and store year-specific information.

## Data Analysis

### Analysis Scripts:
1. **Summary Statistics**: Calculate statistics for columns like `year_founded`, `employees`, and `net_assets` using `summary_stats.py`.
2. **Company Distribution**: The number of companies per domain is visualized with `count_per_domain_visual.py`.
3. **Additional Visualizations**: 
   - Cities with many companies.
   - Company founding years.
   - Large companies (over 1,000 employees).
   - Companies with billion-dollar and million-dollar assets.
   - Global distribution of companies on a map.

These insights are visualized using Power BI and Matplotlib, stored as PDFs.

## Running the Project

1. **Install Libraries**:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Extract Data**:
Run the following command to extract the data and create `companies_data.csv`:

```bash
python extract_data.py
```

3. **Clean Data**:
Run the following command to clean the data and generate `cleaned_companies_data.csv`:

```bash
python preprocess_data.py
```

## File Structure

- **`data/`**: Contains the raw and cleaned data files.
  - **`raw/companies_data.csv`**: Raw extracted data.
  - **`cleaned/cleaned_companies_data.csv`**: Processed and cleaned data.

- **`src/`**: Source code for scraping, preprocessing, and analysis.
  - **`src/scraping/`**: Contains scripts for scraping company data.
    - **`scraping_functions.py`**: Functions for extracting data from webpages.
    - **`extract_data.py`**: Extracts raw data and stores it in `data/raw/companies_data.csv`.
  
  - **`src/preprocessing/`**: Contains scripts for cleaning and preparing the data.
    - **`preprocess_functions.py`**: Functions for data preprocessing.
    - **`preprocess_data.py`**: Cleans the data and stores it in `data/cleaned/cleaned_companies_data.csv`.

  - **`src/analysis/`**: Contains scripts for data analysis and visualizations.
    - **`summary_stats.py`**: Generates summary statistics and saves them in `summary_statistics.csv`.
    - **`count_per_domain_visual.py`**: Analyzes companies by domain and generates visualizations.

- **`visual/`**: Stores all generated visual outputs (e.g., `companies_per_domain.pdf`, Power BI visuals).
  
- **`requirements.txt`**: Lists required Python libraries.
- **`README.md`**: Project documentation with setup and usage instructions.
- **`.gitignore`**: Git ignore file for excluding unnecessary files.

## Conclusion

This project provides a thorough method for extracting, cleaning, and analyzing company data. The visualizations and statistics generated offer valuable insights into the distribution and characteristics of companies, supporting decision-making processes.


## Important Notice: Website Structure Change

**The structure of the target website ([industrie.de Firmenverzeichnis](https://industrie.de/firmenverzeichnis/)) has changed.**  
This change has impacted the functionality of the data extraction script (`extract_data.py`), as the code is based on the previous website structure. The key differences in the new structure may include:

- Changes in the HTML elements, CSS classes, or IDs used to identify company data.
- Reorganized or removed sections, including the "Daten und Kontakte" section that the scraper relies on.

### What You Need to Do

- **Update the scraping functions**: You will need to modify the `scraping_functions.py` script to adapt to the new website structure. Specifically:
  - Inspect the new HTML layout of the website.
  - Identify the new HTML tags, CSS classes, or IDs that contain the relevant company data.
  - Modify the extraction logic accordingly (e.g., `find()` and `find_all()` functions, or any CSS selectors).
  
- **Test the updated code**: After updating the scraping functions, run the extraction script (`extract_data.py`) to verify that the new structure is correctly handled and data is properly extracted.

### How to Debug

If you're unsure how to adapt the script to the new structure, follow these steps:
1. Open the website in a browser and inspect the HTML structure (right-click -> Inspect or use developer tools).
2. Look for the company data sections and compare them with the previous structure.
3. Update the relevant selectors in your code based on the new HTML structure.
4. If the `Daten und Kontakte` section has been moved or renamed, update the extraction logic to account for that.

If you need further assistance, feel free to contact.