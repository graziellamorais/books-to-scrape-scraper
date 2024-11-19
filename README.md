# Book Scraper Project 📚

This project is a web scraper designed to extract information about books from the [Books to Scrape](http://books.toscrape.com/) website. The scraper collects data such as book titles, prices, availability, and ratings. The project also includes functionality to clean the data, save it as a CSV file, and generate visualizations.

---

## Features

- **Web Scraping**: Extracts book details including titles, prices, availability, and ratings from multiple pages.
- **Data Cleaning**: Removes non-ASCII characters and ensures data consistency.
- **Data Storage**: Saves the scraped data into a CSV file for further analysis.
- **Visualization**: Creates visualizations for:
  - Price distribution.
  - Rating distribution.

---

## Technologies Used

- **Python**: Primary language used.
- **Libraries**:
  - `requests`: For fetching webpage content.
  - `BeautifulSoup` (`bs4`): For HTML parsing and data extraction.
  - `csv`: For saving scraped data.
  - `re`: For regex operations in data cleaning.
  - `pandas`: For data manipulation and analysis.
  - `matplotlib`: For creating visualizations.
