import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import sys
import os.path

sys.stdout.reconfigure(encoding='utf-8')

# Get the format type of the book content
def get_number_of_formats(formats):
    list_of_formats = formats.find_all("span")
    if len(list_of_formats) == 2:
        return 5
    elif len(list_of_formats) > 2:
        return 6
    else:        
        format_name = list_of_formats.get_text().strip()
        if format_name == 'eBook':
            return 1
        elif format_name == 'Hardcover':
            return 2
        elif format_name == 'Book with Online Access':
            return 3
        elif format_name == 'Softcover':
            return 4

    return 0    

# Define if the book has online access
def has_online_access(formats):
    list_of_formats = formats.find_all("span")

    for item in list_of_formats:
        format_name = item.get_text().strip()
        if format_name == 'Book with Online Access':
            return 1            

    return 0

# Define method for save data to csv file
def save_to_csv(books, filename):
    path_to_file = 'data/' + filename

    try:
        fileEmpty = os.stat(path_to_file).st_size == 0
    except:
        fileEmpty = True

    with open(path_to_file, 'a+', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, [ 'Page', 'title', 'topic', 'isbn', 'pages', 
                                'year', 'online_access', 'format', 'editorial', 'ebook-price', 
                                'hardcover-price', 'softcover-price', 'print-price', 'print-ebook-price', 'authors'])
        
        if fileEmpty:
            w.writeheader()  # file doesn't exist yet, write headers
        
        for book in books:
            w.writerow(book)


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

topics_param_get_url = "topic=I00001%2CI1200X%2CI12018%2CI12026%2CI12034%2CI12042%2CI12050%2CI12069%2CI12077%2CI13006%2CI16013%2CI13014%2CI1603X%2CI13049%2CI13057%2CI14002%2CI14010%2CI14029%2CI14037%2CI14045%2CI15009%2CI15017%2CI15025%2CI15041%2CI16005%2CI16021%2CI16048%2CI17001%2CI1701X%2CI17028%2CI17036%2CI17044%2CI17052%2CI18008%2CI18016%2CI18024%2CI18030%2CI18032%2CI18040%2CI18059%2CI18067%2CI19000%2CI21000%2CI21040%2CI22005%2CI22013%2CI22021%2CI2203X%2CI22040%2CI23001%2CI2301X%2CI23028%2CI23036%2CI23044%2CI23050%2CI23060%2CI24008%2CI24016%2CI24024%2CI24032%2CI24040%2CI24059%2CI24067%2CI24075%2CI24083%2CI25004%2CI27000%2CI28000%2CI28010%2CI28020%2CI28060%2CI29000%2CI29010%2CI29020%2CI29030%2CI29040%2CI29050%2CI29060%2CI29070%2CI29080%2CI29090%2CI29110%2CI29120%2CV24000"

# Create an empty list of books
books = []
for page in range(401, 501):
    #URL format to obtain the list of books in the pages. In this case there are only 3.
    url = baseurl + "/la/product-search/discipline?disciplineId=computerscience&facet-lan=lan__en&facet-type=type__book&page={}&returnUrl=la%2Fcomputer-science&{}".format(page, topics_param_get_url)
    print (url)
    # Request page content from URL
    k1 = requests.get(url, headers).text.encode('utf8').decode('ascii', 'ignore')

    # Parse to html
    soup_fu = BeautifulSoup(k1,'html.parser')

    # Get all items
    book_items = soup_fu.find_all("div",{"class":"result-type-book"})    
  
    for book in book_items:
        # Get list of available formats
        formats = book.find('p', attrs={'class':'format'})
        # Format URL for getting book page content
        book_url = baseurl + book.a.get('href')
        # Get book page content
        req = requests.get(book_url, headers).text.encode('utf8')
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
                price_ebook = parent_ebook.find('span', {'class': 'price'}).get_text().strip().replace("$", "")

            if t.get_text() == 'Hardcover':
                parent_hardcover = t.parent
                price_hardcover = parent_hardcover.find('span', {'class': 'price'}).get_text().strip().replace("$", "")

            if t.get_text() == 'Softcover':
                parent_softcover = t.parent
                price_softcover = parent_softcover.find('span', {'class': 'price'}).get_text().strip().replace("$", "")

            if t.get_text() == 'Print':
                parent_print = t.parent
                price_print = parent_print.find('span', {'class': 'price'}).get_text().strip().replace("$", "")

            if t.get_text() == 'Print + eBook':
                parent_print_ebook = t.parent
                price_print_ebook = parent_print_ebook.find('span', {'class': 'price'}).get_text().strip().replace("$", "")   

        # title
        try:
            title = book.h4.a.get_text().strip()
        except:
            title = None

        # topic
        try:
            topic = soup_book.find('a', attrs={'itemprop':'genre'}).get_text().strip()
        except:
            topic = None

        # ISBN
        try:
            isbn = soup_book.find('dd', attrs={'itemprop':'isbn'}).get_text().strip()
        except:
            isbn = None
        
        # pages
        try:
            numberOfPages = soup_book.find('dd', attrs={'itemprop':'numberOfPages'}).get_text().strip()
        except:
            numberOfPages = None

        # online access
        try:
            is_online = has_online_access(formats)
        except:
            is_online = None

        # formats
        try:                        
            format_type = get_number_of_formats(formats)
        except:
            format_type = None  

        # year
        try:            
            year_tag = soup_book.find('div', attrs={'class':'copyright'})
            year =  year_tag.get_text().split()[1] # Get the year number online
        except:
            year = None  

        # editorial
        try:            
            editorial_tag = soup_book.find('dd', attrs={'itemprop':'publisher'})
            editorial =  editorial_tag.span.get_text().strip()
        except:
            editorial = None  

        # authors
        try:            
            authors = book.find('p', attrs={'class':'meta contributors book-contributors'}).get_text().strip()
        except:
            authors = None  

        # Add elements of books to list
        books.append({
            'Page':page,
            'title': title,
            'topic': topic,
            'isbn': isbn,
            'pages': numberOfPages,
            'year': year,
            'online_access': is_online,
            'format': format_type,
            'editorial': editorial,
            'ebook-price': price_ebook,
            'hardcover-price': price_hardcover,
            'softcover-price': price_softcover,
            'print-price': price_print,
            'print-ebook-price': price_print_ebook,
            'authors': authors
            })
        
    print('Page #{page} scrapped'.format(page=page))
    time.sleep(3)


for book in books: 
    print(book)

# Call to save_to_csv method
save_to_csv(books, 'books_data_springer.csv')
