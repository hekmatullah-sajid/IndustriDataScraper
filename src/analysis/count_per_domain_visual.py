import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
csv_file = "../../data/cleaned/cleaned_companies_data.csv"
df = pd.read_csv(csv_file)

# Function to extract domain from a URL
def extract_domain(url):
    url = str(url)
    if url == '<na>':
        return ''
    parts = url.split('.')
    if len(parts) > 1:
        domain_parts = parts[-1]
        domain = domain_parts.split('/')
        return domain[0]
    return None

# Apply the extract_domain function to create a new 'domain' column
df['domain'] = df['website'].apply(extract_domain)

# Count the occurrences of each domain
domain_counts = df['domain'].value_counts()

# Filter domains with counts greater than 6
# To have more readable visual 
filtered_domain_counts = domain_counts[domain_counts > 6]

if not filtered_domain_counts.empty:
    # bar chart for filtered domains
    plt.figure(figsize=(12, 6))
    ax = filtered_domain_counts.plot(kind='bar')
    plt.title('Domains with 7+ Companies')
    plt.xlabel('Domain')
    plt.ylabel('Number of Companies')

    # display the chart
    plt.xticks(rotation=45)
    plt.tight_layout()

    # data labels for each bar
    for i, v in enumerate(filtered_domain_counts):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    # save the chart as a PDF
    plt.savefig('csv_file = "../../visulas/companies_per_domain.pdf', format='pdf', bbox_inches='tight')
    plt.show()
else:
    print("No data to plot.")
