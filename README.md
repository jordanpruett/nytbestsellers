This is a scraper that extracts entries on the New York Times bestseller list from PDFs hosted by Hawes Publications.

Given a date range to scrape, it downloads the PDFs into a temporary directory, scrapes the contents, and saves to csv.

It uses requests and beautifulsoup to get the files, pdfminer to extract their contents, and pandas for preparing and manipulating the output csv.