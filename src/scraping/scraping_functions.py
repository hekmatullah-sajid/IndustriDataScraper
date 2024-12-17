from bs4 import BeautifulSoup
import requests


"""
The get_company_list functions gets a list of company information from a webpage.

Arguments:
    page_url (str): webpage's URL to scrape.
    parent_div_class (str): CSS class name of the parent div element that contains company information (link to Danten und Kontak's page and city name).
    city_div_class (str): The CSS class name of the div that contains city name where company is located.

Returns:
    list: A list of dictionaries, where each dictionary has company information, like name, city, and etc.
    Returns an empty list if no data is found or in case there is an issue with the HTTP request.
"""

def get_company_list(page_url, parent_div_class, city_div_class):
    response = requests.get(page_url)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all div elements with the specified parent_div_class
        links_parent_divs = soup.find_all('div', {'class': parent_div_class})
        company_data = []  # List to store company data
        
        for div in links_parent_divs:
            # Find the first 'a' element in the div
            link_elm = div.find('a')
            if link_elm:
                company_name = link_elm.get_text()
                company_href = link_elm['href']
                # Find the div with the specified city_div_class
                company_city_div = div.find('div', {'class': city_div_class})
                company_city = company_city_div.get_text() if company_city_div else ''

                # Scrape contact info for the company
                company_data_contact = scrape_contact_info(company_href)
                
                if company_data_contact:
                    # Create a dictionary with company information
                    company_info = {'name': company_name, 'city': company_city}
                    company_info.update(company_data_contact) # add information retrived from "Daten und Kontakte" section to the dictionary
                    company_data.append(company_info)
                else:
                    print(f"Failed to scrape contact info for {company_name}")

        return company_data
    else:
        print(f"Failed to fetch {page_url}")
        return []


"""
The scrape_contact_info function scrapes contact information for a company from its webpage's "Daten und Kontakte" section.

Arguments:
    company_link (str): The URL of the webpage the contains "Daten und Kontakte" of the company.

Returns:
    a dictionary containing information for the company extracted from "Daten und Kontakte" section.
    returns an empty dictionary if no data is found or in case there is an issue with the HTTP request.
"""
def scrape_contact_info(company_link):
    response = requests.get(company_link)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        page_content = BeautifulSoup(response.content, 'html.parser')
        # Find the div with class 'textwidget', this div contains "Daten und Kontakte" section.
        data_contact_sec = page_content.find('div', {'class': 'textwidget'})

        if data_contact_sec:
            data_contact_info = {}
            # Find the first 'dl' element within data_contact_sec
            dl_element = data_contact_sec.find("dl")

            if dl_element:
                # Find all 'dt' and 'dd' elements within dl_element
                # 'dt' elements contain icons that describe the type of information
                # 'dd' elements contain the corresponding values
                
                dt_elements = dl_element.find_all('dt')
                dd_elements = dl_element.find_all('dd')

                # Iterate through dt_elements and dd_elements in parallel to retrieve the icon and corresponding value
                for dt, dd in zip(dt_elements, dd_elements):
                    icon_class = dt.find('i')['class'][1]
                                       
                    # If it's an address, separate address parts with spaces
                    # The address parts are separated using <br> elements in the HTML
                    if icon_class == 'fa-map-pin':
                        address_parts = [part.strip() for part in dd.stripped_strings]
                        data_contact_info[icon_class] = ' '.join(address_parts)
                    else:
                        data_contact_info[icon_class] = dd.get_text()
            else:
                print("No contact info found on ", company_link)
            return data_contact_info
        else:
            print("No contact info section found on ", company_link)
    else:
        print("Failed to fetch ", company_link)
    return {}

"""
The icon_to_name function converts an icon's CSS class name to a human-readable filed name.

Arguments:
    icon_class (str): icon's CSS class name

Returns:
    str: a human-readable data name corresponding to the icon

def icon_to_name(icon_class):

    # Dictionary to map icon class to human-readable data names
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

    # Use the dictionary to get data name
    return icon_name_dict.get(icon_class)
"""
