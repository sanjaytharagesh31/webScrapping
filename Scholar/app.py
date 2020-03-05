from flask import Flask, render_template, request
import urllib.request
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd

app = Flask(__name__)


def calc(arg):
    t = PrettyTable(['SNO', 'TITLE', 'CITED BY', 'YEAR'])  # to create table
    url = arg
    page = requests.get(url)  # send request to cc server and returns the page
    soup = BeautifulSoup(page.content, 'html.parser')  # store html content in soup
    # print(soup.prettify())  # prettify() to print the html code in well intended form
    table = soup.findAll('table', id="gsc_a_t")  # return the tables with class=dataTable
    req_table = table[0]
    # print(len(table))
    # print('----------------------------------------------------------------------------------------------')
    # print(req_table)
    # print('----------------------------------------------------------------------------------------------')
    tr = req_table.tbody.findAll('tr')  # tr from all tbody tag
    # print (len(tr))
    # td = tr[0].findAll('td') #find all td from tr[0]
    # print (len(td))
    # print (td[0].text)
    paper_titles = []
    for i in range(len(tr)):
        td = tr[i].findAll('td')
        paper_titles.append(td[0].text)
        t.add_row([i + 1, td[0].text, td[1].text, td[2].text])  # add_row takes a 'list' of data
    # print(t)
    html_table = t.get_html_string()
    df = pd.read_html(html_table, header=0)[0]
    # print(df)
    # Store the dataframe in Excel file
    print("after count")
    # print(paper_titles)
    answer = []
    for tt in paper_titles:
        ss = tt
        tt = tt.replace(" ", "")
        tt = tt.lower()
        if 'crypto' in tt:
            answer.append([ss])
    df_ans = pd.DataFrame.from_records(answer)
    print(answer)
    df_ans.to_excel("D:\sem6\openLab\BeautifulSoup\jitle_data.xlsx")
    df.to_excel("D:\sem6\openLab\BeautifulSoup\export_data.xlsx")
    return df


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/scrap', methods=['POST'])
def func_tool():
    print("Hrloo")
    url = request.form["url"]
    print(url)
    html_table = calc(url)
    return render_template("index.html", table_data=[html_table.to_html()])


if __name__ == '__main__':
    app.run()
