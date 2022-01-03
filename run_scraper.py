
import time
import os
from urllib.parse import urljoin

from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import NewConnectionError
from socket import gaierror

from pdfminer.high_level import extract_pages

from nytscrape.download import get_year_urls, get_pdf_urls, get_pdf_tempfile
from nytscrape.extract import extract_blurbs, parse_blurb
from nytscrape.process import add_row_to_csv

HOME_URL = 'http://www.hawes.com'
LISTPAGE = 'http://www.hawes.com/pastlist.htm'
TEST = 'http://www.hawes.com/2021/2021.htm'
TSV_DEST = 'nyt_full.tsv'
MISSING_WEEKS = 'missing_weeks.txt'

CONNECTION_EXCEPTIONS = (
    ConnectionError,
    MaxRetryError,
    NewConnectionError,
    gaierror
)

def main():

    year_urls = get_year_urls(LISTPAGE)
    destpath = os.path.join('data', TSV_DEST)
    for year_url in year_urls:
        yearpage = urljoin(HOME_URL, year_url)
        pdf_urls = get_pdf_urls(yearpage)

        for pdf_url in pdf_urls:
            year = year_url.split('-')[0].split('/')[0]
            week = pdf_url.split('.')[0]
            pdfpage = f'{urljoin(HOME_URL, year, pdf_url)}/{pdf_url}'
            complete = False

            while not complete:

                try:
                    pdf_obj = get_pdf_tempfile(pdfpage)
                    pdf_page = list(extract_pages(pdf_obj))[0]
                    pdf_obj.close()

                    blurbs = extract_blurbs(pdf_page)
                    if blurbs:
                        rank = 1
                        for blurb in blurbs:
                            book = parse_blurb(blurb)
                            book.rank = rank
                            # sometimes the week sneaks in as a title w/o anything else
                            if book.author or book.publisher:
                                add_row_to_csv(
                                    week=week,
                                    book=book,
                                    destpath=destpath
                                )
                                rank += 1
                    else:
                        with open(os.path.join('data', MISSING_WEEKS), 'a+') as f:
                            f.write(f'{year}\t{week}\n')
                    complete = True
                
                except CONNECTION_EXCEPTIONS:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(f'Connection error at {current_time}')
                    print('Waiting 5 minutes before continuing.')
                    time.sleep(300)

            print(f'Finished {pdf_url}')
            time.sleep(2) # be a polite scraper!


if __name__=='__main__':
    main()