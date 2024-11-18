import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import matplotlib.pyplot as plt


# Function to save data to a CSV file
def save_to_csv(data, filename="books.csv"):
    """
    Save book data to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "availability", "rating"])
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write the book data
    print(f"Data saved to {filename}")


# Function to fetch the webpage content
def fetch_page(url):
    """
    Fetch the HTML content of a webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        return response.text # Return the page's HTML content
    except requests.RequestException as e:
        print(f"Error fetching the URL: {url}\n{e}")
        return None


# Function to parse the HTML content
def parse_page(html):
    """
    Parse the HTML content with BeautifulSoup.
    """
    return BeautifulSoup(html, 'html.parser')


# Function to extract book data
def extract_books(soup):
    """
    Extract book details from the parsed HTML content.
    """
    books = []
    book_elements = soup.select('.product_pod')  # Select all HTML elements with the class "product_pod"
    
    for book in book_elements: # Loop through each book container
        title = book.h3.a['title']  # Get the book title
        price = book.select_one('.price_color').text  # Get the price
        availability = book.select_one('.availability').text.strip()  # Get availability status and strip extra spaces
        rating = book.select_one('p.star-rating')['class'][1]  # Rating is the second class
        books.append({ # Append a dictionary with the extracted data to the list
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating
        })

    return books


# Function to scrape books
def scrape_books(base_url):
    """
    Scrape books from all pages of the website.
    """
    books = []
    current_page = 1 # Start with the first page

    while True:  # Loop indefinitely until no more pages are found
        print(f"Scraping page {current_page}...")

        page_url = f"{base_url}catalogue/page-{current_page}.html"  # Construct the URL for the current page
        
        html = fetch_page(page_url)  # Fetch the HTML content of the page
        if not html: 
            break# Stop if the page couldn't be fetched

        soup = parse_page(html) # Parse the HTML content
        page_books = extract_books(soup)  # Extract books from the parsed HTML
        if not page_books:
            break  # Stop if no books are found (end of pages)

        books.extend(page_books) # Add the books from the current page to the main list
        current_page += 1 # Increment to the next page

    return books


# Function to clean data
def clean_data(data):
    """
    Clean non-ASCII characters and handle encoding issues in book data.
    """
    for book in data:
        # Clean title and remove non-ASCII characters
        book['title'] = book['title'].encode('ascii', 'ignore').decode('ascii')
        
        # Clean price: Remove any non-ASCII characters and '£' symbol
        book['price'] = book['price'].encode('ascii', 'ignore').decode('ascii')  # Remove non-ASCII characters
        book['price'] = re.sub(r'[^\x00-\x7F]+', '', book['price'])  # Remove any remaining non-ASCII characters
        book['price'] = book['price'].replace('Â','')  # Remove the 'Â' character specifically
        
        # Clean availability and rating
        book['availability'] = book['availability'].encode('ascii', 'ignore').decode('ascii')
        book['rating'] = book['rating'].encode('ascii', 'ignore').decode('ascii')

    return data


# Fuction to create visualizations
def create_visualizations(data):
    """
    Create visualizations from the scraped data.
    """
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Clean and process data for the 'price' column
    df['price'] = df['price'].str.replace('£', '', regex=False)  # Remove "£"
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric, coerce invalid values to NaN
    
    # Check if the 'price' column is numeric
    print(df['price'].dtype)  # Ensure it's a float
    
    # Plot price distribution
    plt.figure(figsize=(10, 6))
    df['price'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
    plt.title("Price Distribution of Books")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")
    plt.show()
    
    # Plot rating distribution
    rating_counts = df['rating'].value_counts()
    rating_counts.plot(kind='bar', color='orange', edgecolor='black')
    plt.title("Rating Distribution of Books")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plt.show()


# Main function
def main():
    """
    Main function to run the web scraper.
    """
    base_url = "https://books.toscrape.com/"
    all_books = scrape_books(base_url)
    
    # Display the extracted data
    for book in all_books:
        print(book)
    
    # Clean non-ASCII characters
    all_books = clean_data(all_books)

    # Saving data in a csv file
    save_to_csv(all_books)

    # Create visualizations
    create_visualizations(all_books)


# Run the script
if __name__ == "__main__":
    main()