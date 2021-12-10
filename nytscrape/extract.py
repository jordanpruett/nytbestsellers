"""
Classes and methods for extracting information from Hawes PDFs.
"""
import re
from dataclasses import dataclass

from pdfminer.layout import LTTextBoxHorizontal, LTPage

@dataclass
class Book:
    """Class for representing a book found within a Hawes blurb."""
    title: str
    author: str
    publisher: str
    description: str

def splitList(lst, sep):
    """
    Helper function used by extract_entries to split lists based on a separator.
    """
    new = []
    prior = 0
    for index, item in enumerate(lst):
        if item == sep:
            new.append(''.join(lst[prior:index]))
            prior = index + 1
    new.append(''.join(lst[prior:]))
    return new

def extract_blurbs(pdf_page: LTPage):
    """
    Given an LTPage object from a Hawes PDF, extracts individual blurbs
    corresponding to single NYT bestsellers.

    :param page: LTPage object from which to extract blurbs.

    :return: a list of strings corresponding to found blurbs.
    """
    for element in pdf_page:
        if isinstance(element, LTTextBoxHorizontal):
            block = [line.get_text() for line in element]
            block = splitList(block, ' \n')
            block = [text.replace('\n', '') for text in block]

            # hackish way to check if this is the text block containing
            # bestseller entries. 
            if any(['(' in string for string in block]):
                return block

    print('No valid text block found.')
    return None

def parse_blurb(blurb: str):

    # title
    title = re.split(r'[,!?] (?=[a-z])', blurb)[0]

    # author
    match = re.search(r'(?<=, by ).+?(?= \()', blurb)
    if match:
        author = match.group()
        author = author[:-1]
    else:
        author = blurb.replace(title, '')
        author = author.replace(',', '')
        author = author.split('(')[0]
        author = author.strip()
        author = author[:-1]

    # publisher
    match = re.search(r'\((.*?)\)', blurb)
    if match:
        publisher = match.group()
    else:
        publisher = ''

    # description
    if match:
        description = blurb.split(publisher)[1].strip()
    else:
        description = ''

    # leave parentheses until the end, as they are useful for parsing description
    publisher = publisher.replace('(', '').replace(')', '')
    return Book(title, author, publisher, description)

