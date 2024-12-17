import re

"""
The function 'remove_name' removes the company name from the address field, if present.
it also stips space and comma 

Argumnets:
    record (dict): A dictionary containing address and name fields.

Returns:
    str: The address with the company name removed.
"""
def remove_name(record):
    address = str(record['address'])
    name = str(record['name'])
    result = address.replace(name, '').strip(', ')
    return result

# This function cleans and formats phone numbers.
"""
The function 'format_clean_phone' cleans and formats phone number.
It removes '/' or '-' separators and adds '+49' as the country code if not present

Args:
    phone_number (str): The input phone number.

Returns:
    str: The cleaned and formatted phone number.
"""
def format_clean_phone(phone_number):
    clean_phone = ''.join(char if char.isdigit() or char == '+' else '' for char in str(phone_number))

    if clean_phone and not clean_phone.startswith("+"):
        clean_phone = "+49" + clean_phone
        clean_phone = clean_phone.replace('+490', '+49')  # Removes the leading 0 from the number and adds +49 to it.

    return clean_phone


"""
This function extracts the year from text using regular expressions.
It is used to remove text form field year_founded and keep only year

Argumnets:
text (str): The input text.

Returns:
int: The extracted year.
"""
def get_year(text):
    year_founded = re.search(r'\d{4}', str(text))
    return int(year_founded.group())


"""
This function is used to extract the number of employees from the employee field,
keeping only the numeric values and discarding text.

Argumentss:
    text (str): The input text.

Returns:
    str or None: The extracted numeric value or None if not found.
"""
def extract_employees_number(text):
    match_value = re.search(r'(\d+(?:\.\d+)?)', str(text))
    if match_value:
        numeric_value = match_value.group(1).replace('.', '')
        return numeric_value
    else:
        return None

# This function processes the 'website' column to remove 'http://' or 'https://' 
# and adds 'www.' if it is missing.
"""
This function processes the 'website' column, so, all values have a similar format
it removes 'http://' or 'https://' and adds 'www.' if missing.

Arguments:
    website (str): The input website URL.

Returns:
    str: The processed website URL.
    """
def process_website(website):
    website = str(website).lower()  # Convert to lowercase
    if website == '<na>':
        return ''
    
    if website.startswith('http://'):
        website = website[7:]
    elif website.startswith('https://'):
        website = website[8:]

    if website and not website.startswith('www.'):
        website = 'www.' + website

    return website


"""
The following code is designed to process the 'net_assets' field of the comapnies_data dataset. It performs the following tasks:

1. It removes edge cases where the number of customers is used as the value.
2. For the remaining cases, it converts text-based values like '3 Million' to numeric values (e.g., 3,000,000).
3. It standardizes and uses unique currency representations to avoid inconsistencies and stores it in a new column "net_assets_currency"
4. It creates a new column called 'net_assets_year' to store the year in which the 'net_assets' were calculated.
"""

# The following dictionaries can be extended to handle additional representations as needed.

# This dictionary is used to map text representations to their numeric multipliers
# For example, 'Mrd' represents a Billion (1,000,000,000)
multipliers = {
    'Mrd': 1e9,
    'Billion': 1e12,
    'Millionen': 1e6,
    'Million': 1e6,
    'Mill': 1e6,
    'Mio': 1e6,
    'M': 1e6,
    'million': 1e6
}

# THis dictionary is to map currency representations to their currency codes
# For example, 'Euro' represents '€'
currencies = {
    'Euro': '€',
    '€': '€',
    'Eur': '€',
    'CHF': 'CHF',
    'U.S. Dollars': '$',
    '$': '$',
    'Dollars': '$',
    'dollars': '$',
}

# Default currency code
default_currency = '€'

"""
This fuction extracts year, monetary vlaue (called number here), multiplier, and currency from the given text.

Args:
text (str): Input text containing net assets information.

Returns:
tuple: A tuple containing year (str), number (str), multiplier (str), and currency (str).
"""
def extract_year_money_currency(text):
    # Extract the year from the text (in some cases two years are written like 2020/2021)
    year_match = re.search(r'\b(20[1-2][0-9]|20[1-9][0-9]/20[1-9][0-9])\b', text)
    year = year_match.group() if year_match else None

    # Remove the found year from the text
    text_without_year = re.sub(r'\b(20[1-2][0-9]|20[1-9][0-9]/20[1-9][0-9])\b', '', text)

    # Initialize number, multiplier, and currency
    number = None
    multiplier = None
    currency = None

    # Try to extract a number with optional comma or period as thousands separator
    number_match = re.search(r'(\d+(?:[.,]\d{3})*(?:,\d+)?)\s*(Mrd|Millionen|Million|Mio|Mill|Billion|M|million)?', text_without_year)
    currency_match = re.search(r'(Euro|€|Eur|CHF|U\.S\. Dollars|\$|Dollars|dollars)', text_without_year)
    if number_match:
        number = number_match.group(1)
        multiplier = number_match.group(2)
        currency = ''
        if currency_match:
            currency = currency_match.group(1)
    return year, number, multiplier, currency

"""
This function rrocess the 'net_assets' field in a DataFrame row.

Arguments:
row: A DataFrame row containing net_assets information.

Returns:
The modified DataFrame row.
"""
def process_net_asset_field(row):
    text = row['net_assets']

    if text:
        year, number, multiplier, currency = extract_year_money_currency(text)
        
        # Format and convert the number based on the multiplier
        formatted_number = None
        if number:
            if number.strip():  # Ensure the number is not empty
                # Remove dots (thousands separators) and replace commas with periods
                cleaned_number = number.replace('.', '').replace(',', '.')

                # Convert to float if it's not an empty string
                if cleaned_number:
                    formatted_number = float(cleaned_number.strip())

                    # Apply the multiplier if present
                    if multiplier:
                        multiplier_value = multipliers.get(multiplier, 1)  # Use 1 if multiplier is not found
                        formatted_number *= multiplier_value

        # Determine the currency code based on the extracted currency representation
        if currency:
            currency_code = currencies.get(currency, default_currency)
        else:
            currency_code = default_currency

        # Concatenate the number and currency as a string and store it in 'net_assets' column
        if formatted_number:
            formatted_number = int(formatted_number)
            # Check if 'kunden' is in the text to determine if 'net_assets' should be empty
            row['net_assets'] = '' if 'kunden' in text.lower() else formatted_number
            # Store the currency code in a new 'net_assets_currency' column
            row['net_assets_currency'] = currency_code
            # Store the year in a new 'net_assets_year' column
            row['net_assets_year'] = year
        else:
            row['net_assets'] = ''
            row['net_assets_currency'] = ''
            row['net_assets_year'] = ''

    return row
