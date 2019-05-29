import datetime as dt
import matplotlib.pyplot as plt
#from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import praw
import bs4 as bs
import pickle
import requests
import os

def check_tickers(oneticker):
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
  # with open("sp500tickers.pickle", "wb") as f:
  #      pickle.dump(tickers, f)

    last = False
    for x in tickers:
        if x == oneticker:
            return True
    return last
    
        
def check_list(alltickers, oneticker):
    for a in 500:
        print(a)
        if oneticker == alltickers[a]:
            print(a)
            return true
        else:
            return false

def getquote(company):
    print('company is')
    print(company)
    start = dt.datetime(2000,1,1)
    time = dt.datetime.now()
    df = web.DataReader(company, 'yahoo',start, time)
    print('not printing right')
    print(df.tail(1).Close)
    abc = df.tail(1).Close
    return abc
    
def authenticate():
    reddit = praw.Reddit(username='redditbot54321', password='superheroyo', client_id='0g1vLWnW_cUR4A', client_secret='rBvEc35KeH82VxphZ1Hv5Hnwhj8', user_agent='This is a bot')

    return reddit


def run_bot(reddit, keyphrase):
    for comment in reddit.subreddit('investing').comments(limit=40):
        if keyphrase in comment.body:
            
            oneticker = comment.body.replace(keyphrase, '')
            oneticker = oneticker.replace(' ','')
            
            try:
               # alltickers = check_tickers()
                print(oneticker)
                if check_tickers(oneticker)==True:
                    quote = str(getquote(oneticker))
                    quote = quote[15:]
                    quote = quote[:10]
                    reply = "The latest closing price of "+oneticker+" is "+quote
                    print(reply)
                    comment.reply(reply)
                    print("This is a bot")
                else:
                    reply = "This is not a company in the S&P 500"
                    #comment.reply(reply)
                    print('failed')
                    print("This is a bot")
            except:
                print("no frequent")

def main():
    #replied = get_replied()
    keyphrase = '!quotethis'
    reddit = authenticate()
    run_bot(reddit, keyphrase)
        
if __name__ == '__main__':
    main()








#style.use('ggplot')
##start = dt.datetime(2000,1,1)
##end = dt.datetime(2018, 9,16)
##
##df = web.DataReader('TSLA', 'yahoo', start, end)
##df.to_csv('tsla.csv')
##start = dt.datetime(2000,1,1)
##time = dt.datetime.now()
##df = web.DataReader('TSLA', 'yahoo',start, time)
##print("As of ")
##print(time)
##print("the stock price is ")
##print(df.tail(1).Close)
##df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
##print(df.tail(1))
##
##df.plot()
##plt.show()


