import requests
from bs4 import BeautifulSoup
import re
import time
import csv

# Setting base URL
baseurl = "https://www.springer.com"

# Setting request headers
headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 
	'Accept-Encoding':'gzip, deflate', 
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.8', 
	'Cache-Control': 'no-cache',
	'Pragma': 'no-cache',
	'DNT':'1',
	'Upgrade-Insecure-Requests':'1'
	}

# Create an empty list of books
books = []
for page in range(1, 501):
    #URL format to obtain the list of books in the pages. In this case there are only 3.
    url = baseurl + "/la/product-search/discipline?disciplineId=computerscience&facet-lan=lan__en&facet-type=type__book&page={}&returnUrl=la%2Fcomputer-science".format(page)
    # Request page content from URL
    k1 = requests.get(url, headers).text.encode('utf8').decode('ascii', 'ignore')

    # Parse to html
    soup_fu = BeautifulSoup(k1,'html.parser')

    # Get all items
    book_items = soup_fu.find_all("div",{"class":"result-type-book"})

  
    for book in book_items:
        # Format URL for getting book page content
        book_url = baseurl + book.a.get('href')
        # Get book page content
        req = requests.get(book_url, headers).text.encode('utf8').decode('ascii', 'ignore')
        # parse to html
        soup_book = BeautifulSoup(req,'html.parser')
        
        # Get tag for getting subtitle
        info = soup_book.find('div', attrs={'class':'bibliographic-information'})    

        # Get prices tag by regex
        prices = soup_book.find_all('dt', {'class': re.compile(r'buy-rendition-')})

        # Get formats of books
        types = soup_book.find_all('span', {'class': 'cover-type'})

        #Default price values
        price_ebook='NA'
        price_hardcover='NA'
        price_softcover='NA'
        price_print='NA'
        price_print_ebook='NA'
        
        # Prices 
        for t in types:

            if t.get_text() == 'eBook':
                parent_ebook = t.parent
                price_ebook = parent_ebook.find('span', {'class': 'price'}).get_text().strip()

            if t.get_text() == 'Hardcover':
                parent_hardcover = t.parent
                price_hardcover = parent_hardcover.find('span', {'class': 'price'}).get_text().strip()

            if t.get_text() == 'Softcover':
                parent_softcover = t.parent
                price_softcover = parent_softcover.find('span', {'class': 'price'}).get_text().strip()

            if t.get_text() == 'Print':
                parent_print = t.parent
                price_print = parent_print.find('span', {'class': 'price'}).get_text().strip()

            if t.get_text() == 'Print + eBook':
                parent_print_ebook = t.parent
                price_print_ebook = parent_print_ebook.find('span', {'class': 'price'}).get_text().strip()   

        # print(type(price_ebook))
        # print(type(price_hardcover))

        # Subtitle
        # subtitle = ''
        try:
            subtitle = info.h2.get_text()
        except:
            subtitle=None

        # Topic
        topic = soup_book.find('a', attrs={'itemprop':'genre'}).get_text()

        # ISBN
        isbn = soup_book.find('dd', attrs={'itemprop':'isbn'}).get_text()

        # Pages
        pages = 0
        numberOfPages = soup_book.find('dd', attrs={'itemprop':'numberOfPages'})
        if numberOfPages is None:
            pages = 0
        else: 
            pages = numberOfPages.get_text()    

        # Add elements of books to list
        books.append({
            'Page':page,
            'title': book.h4.a.string, 
            'subtitle': subtitle,
            'topic': topic,
            'isbn': isbn,
            'pages': pages,
            'ebook-price': price_ebook,
            'hardcover-price': price_hardcover,
            'softcover-price': price_softcover,
            'print-price': price_print,
            'print-ebook-price': price_print_ebook,
            'partial-url': book.a.get('href'),
            'authors': book.find('p', attrs={'class':'meta contributors book-contributors'}).get_text().strip()       
            })
        
    print('Page #{page} scrapped'.format(page=page))
    time.sleep(20)


for book in books: 
    print(book)


filename = 'books_data_springer.csv'

with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, [ 'Page','title','subtitle','topic','isbn', 
                            'pages', 'ebook-price', 'hardcover-price', 'softcover-price', 
                            'print-price', 'print-ebook-price', 'partial-url', 'authors' ])
    w.writeheader()

    for book in books:
        w.writerow(book)