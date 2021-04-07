import requests
from bs4 import BeautifulSoup

baseurl = "https://www.springer.com/la"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

# k = requests.get(baseurl).text
# parse to html
# soup=BeautifulSoup(k,'html.parser')
# get all disciplines
# booklist = soup.find_all("ul",{"class":"cms-col cms-link-list"})

# print(booklist)


first_url = baseurl + "/product-search/discipline?disciplineId=computerscience&facet-type=type__book&facet-lan=lan__en&returnUrl=la%2Fcomputer-science"

k1 = requests.get(first_url).text.encode('utf8').decode('ascii', 'ignore')
# parse to html
soup_fu=BeautifulSoup(k1,'html.parser')
# get all disciplines
first_booklist_page = soup_fu.find_all("div",{"class":"result-type-book"})

books = []


for book in first_booklist_page:
    # name = book.find("a",{"class":"product-card"}).get('href')                 
    # productlinks.append(baseurl + link)
    books.append({  
        'bookname': book.h4.a.string, 
        'authors': book.find('p', attrs={'class':'meta contributors book-contributors'}).get_text(), 
        'price': book.find('span', attrs={'class':'price'})
        })
    # print(book.h4.a.string)


for book in books:
    print(book)

print(first_booklist_page)