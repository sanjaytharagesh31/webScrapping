import webbrowser
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os

def single_page(url):
     t = PrettyTable(['Name','Price'])
     page = requests.get(url)
     soup = BeautifulSoup(page.content,'html.parser')
     div = soup.findAll('div',class_='col-sm-8 col-md-9')
     sec = div[0].section
     ol = sec.findAll('ol',class_='row')
     li = ol[0].findAll('li')
     for i in range(len(li)):
          row = []
          row.append(li[i].h3.a['title'])
          divp = li[i].findAll('div',class_='product_price')
          row.append(divp[0].p.text.encode('utf-8'))
          t.add_row(row)

     t.align['Name'] = "l"
     print t

url = 'http://books.toscrape.com/index.html'
page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
div = soup.findAll('div',class_='side_categories')
table = PrettyTable(['No.','Category'])
li = div[0].ul.li.ul.findAll('li')

for i in range(len(li)):
     row = [i+1,li[i].a.text.strip()]
     table.add_row(row)

table.align = "l"
print table
ch = input("Enter the category no. : ")
url = 'http://books.toscrape.com/'
url += li[ch-1].a['href']
single_page(url)
