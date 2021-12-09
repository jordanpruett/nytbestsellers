
import time
from urllib.parse import urljoin

from pdfminer.high_level import extract_pages

from nytscrape.download import get_year_urls, get_pdf_urls, get_pdf_tempfile
from nytscrape.extract import extract_blurbs, parse_blurb

HOME_URL = 'http://www.hawes.com'
LISTPAGE = 'http://www.hawes.com/pastlist.htm'
TEST = 'http://www.hawes.com/2021/2021.htm'

def main():

    year_urls = get_year_urls(LISTPAGE)
    for year_url in year_urls:
        yearpage = urljoin(HOME_URL, year_url)
        pdf_urls = get_pdf_urls(yearpage)

        for pdf_url in pdf_urls:
            year = year_url.split('-')[0].split('/')[0]
            pdfpage = f'{urljoin(HOME_URL, year, pdf_url)}/{pdf_url}'
            pdf_obj = get_pdf_tempfile(pdfpage)
            pdf_page = list(extract_pages(pdf_obj))[0]
            pdf_obj.close()

            blurbs = extract_blurbs(pdf_page)
            for blurb in blurbs:
                book = parse_blurb(blurb)
                print(book.title, book.author, book.publisher)
                print()
            time.sleep(2) # be polite!


    #     print(pdf_urls)
    #     print()
    #     time.sleep(3)
    # # pdf_urls = get_pdf_urls(TEST)
    # # print(pdf_urls)

if __name__=='__main__':
    main()