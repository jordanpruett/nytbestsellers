"""
Methods for processing data extracted from Hawes bestseller PDFs.

We wish to yield three related .csv files:
1) a table of all individual entries over the whole history of the list
2) a table of individual titles, with a sum of total weeks on the list
3) a table of titles matched to HathiTrust
"""
import csv
import os

def add_row_to_csv(week: str, book, destpath: str):

    if not os.path.exists(destpath):
        with open(destpath, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(['week', 'title', 'author', 'publisher', 'description'])

    else:
        with open(destpath, 'a+', encoding='UTF-8') as f:
            writer =  csv.writer(f, delimiter='\t')
            row = [week, book.title, book.author, book.publisher, book.description]
            writer.writerow(row)
    
    return

