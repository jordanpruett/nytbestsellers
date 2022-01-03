This is a scraper that extracts entries on the New York Times bestseller list from PDFs hosted by [Hawes Publications](http://www.hawes.com/pastlist.htm).

It downloads the PDFs into a temporary directory, scrapes the contents, aggregates based on title, and saves to csv.

It uses requests and beautifulsoup to get the files, pdfminer to extract their contents, and csv for preparing and manipulating the output csv.