import requests
from bs4 import BeautifulSoup

baseurl = "https://www.springer.com/la"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

k = requests.get('https://www.springer.com/la').text
# parse to html
soup=BeautifulSoup(k,'html.parser')
# get all disciplines
booklist = soup.find_all("ul",{"class":"cms-col cms-link-list"})

# print(soup)
print(booklist)