import requests
from bs4 import BeautifulSoup
import re

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

# Formatting URL for getting books list of the first page
first_url = baseurl + "/la/product-search/discipline?disciplineId=computerscience&facet-type=type__book&facet-lan=lan__en&returnUrl=la%2Fcomputer-science"

# Request page content from URL
k1 = requests.get(first_url, headers).text.encode('utf8').decode('ascii', 'ignore')

# Parse to html
soup_fu = BeautifulSoup(k1,'html.parser')

# Get all disciplines
first_booklist_page = soup_fu.find_all("div",{"class":"result-type-book"})

# Create an empty list of books
books = []

#print(first_booklist_page[0])

for book in first_booklist_page:

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

    # Prices    
    for t in types:
        if t.get_text() == 'eBook':
            parent_ebook = t.parent
            price_ebook = parent_ebook.find('span', {'class': 'price'})            
        elif t.get_text() == 'Hardcover':
            parent_hardcover = t.parent
            price_hardcover = parent_hardcover.find('span', {'class': 'price'})    

    # print(type(price_ebook))
    # print(type(price_hardcover))

    # Subtitle
    subtitle = ''
    if info.h2 is None:
        subtitle = 'NA'
    else: 
        subtitle = info.h2.get_text()

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
        'title': book.h4.a.string, 
        'subtitle': subtitle,
        'topic': topic,
        'isbn': isbn,
        'pages': pages,
        'ebook-price': price_ebook.get_text().strip(),
        'hardcover-price': price_hardcover.get_text().strip(),
        'partial-url': book.a.get('href'),
        'authors': book.find('p', attrs={'class':'meta contributors book-contributors'}).get_text().strip()       
        })
    
    # print(type(books))

    # Clearing price tags for avoid setting previous prices
    price_ebook.clear()
    price_hardcover.clear()

for book in books:
    print(book)
