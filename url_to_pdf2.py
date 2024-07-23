import pandas as pd
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scraped Content', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 10, title, 0, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def clean_html(soup, title):
    # Remove script, style, and advertisement elements
    for element in soup(['script', 'style', 'aside', 'footer', 'header', 'nav']):
        element.decompose()

    # Remove specific divs or sections by class or id that typically contain ads
    ad_classes = ['ad', 'advertisement', 'ads', 'promo', 'sponsored']
    for ad_class in ad_classes:
        for element in soup.find_all(class_=ad_class):
            element.decompose()
        for element in soup.find_all(id=ad_class):
            element.decompose()

    # Remove news headline items at the bottom (example: by class 'headline' or 'news')
    headline_classes = ['headline', 'news']
    for headline_class in headline_classes:
        for element in soup.find_all(class_=headline_class):
            element.decompose()

    # Extract the text content and remove unnecessary white spaces
    text_content = soup.get_text(separator=' ', strip=True)

    # Remove the title from the content
    if title in text_content:
        text_content = text_content.replace(title, '', 1).strip()

    return text_content


def extract_title(soup):
    # Try to get the title from <title> tag
    title = soup.title.string if soup.title else None
    # If not found, try to get it from the first <h1> tag
    if not title:
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else 'No Title'
    return title


def is_valid_url(url):
    return url.startswith(('http://', 'https://'))


def handle_encoding(text):
    # Replace problematic characters with a placeholder or remove them
    return text.encode('latin1', 'replace').decode('latin1')


# Load the Excel file
file_path = 'AI Ethics Corpus-Sample_10.xlsx'
df = pd.read_excel(file_path)

# Extract the content of the 3rd column (index 2, since index starts at 0)
url_column = df.iloc[:, 2]

# Iterate through each URL in the third column
for index, url in url_column.items():
    # Ensure the URL is properly formatted
    if not is_valid_url(url):
        print(f"Skipping invalid URL: {url}")
        continue

    try:
        # Get the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title = extract_title(soup)

        # Clean the HTML content
        clean_content = clean_html(soup, title)

        # Create a PDF file
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Add title and content to PDF, handling encoding issues
        pdf.chapter_title(f'Title: {handle_encoding(title)}')
        pdf.chapter_body(handle_encoding(clean_content))

        # Define the file name using the index to avoid overwriting files
        file_name = f'url_content/scraped_content_{index}.pdf'

        # Save the PDF
        pdf.output(file_name, 'F')

        print(f"Content from {url} saved to {file_name}")
    except requests.RequestException as e:
        print(f"Failed to retrieve content from {url}: {e}")
