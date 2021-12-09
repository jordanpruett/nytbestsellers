"""
Methods for getting urls from Hawes and downloading Hawes PDFs as tempfiles.
"""

import re
from tempfile import TemporaryFile

import requests
from bs4 import BeautifulSoup

def get_year_urls(mainpage: str):

    request = requests.get(mainpage)
    soup = BeautifulSoup(request.text, features="html.parser")

    return [link.get('href')
            for link in soup.find_all('a')
            if re.match(r'\d{4}/\d{4}\.htm', link.get('href'))]

def get_pdf_urls(yearpage: str):

    request = requests.get(yearpage)
    soup = BeautifulSoup(request.text, features="html.parser")

    return [link.get('href')
            for link in soup.find_all('a')
            if link.get('href') and link.get('href').endswith('.pdf')]

def get_pdf_tempfile(pdf_url: str):

    temp = TemporaryFile()
    temp.write(requests.get(pdf_url).content)
    return temp
