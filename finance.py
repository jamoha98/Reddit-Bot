# importing libraries
import datetime as dt
import pandas_datareader.data as web
import praw
import bs4 as bs
import pickle
import requests
import argparse

# Command line parser to accept credentials
parser = argparse.ArgumentParser(description='Reddit Bot Credentials')
parser.add_argument('Credentials', type=str, nargs=4,
                    help='Enter Credentials in this order with space in between: Username, Password, Client ID, Client Secret')
args = parser.parse_args().credentials


# Checks if the ticker is in the S&P500
def check_tickers(oneticker):
    # Webscrapes Wikipedia page of S&P500
    resp = requests.get(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    # Makes list of tickers from S&P500 companies
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    pickle.dump(tickers)

    # check if the ticker requested is in the list
    for x in tickers:
        if x == oneticker:
            return True
    return False


# API request from yahoo finance to get last closing price
def getquote(company):
    start = dt.datetime(2000, 1, 1)
    time = dt.datetime.now()
    df = web.DataReader(company, 'yahoo', start, time)
    closing_price = df.tail(1).Close
    return closing_price


# reddit authentification, takes in user command line credentials
def authenticate():
    reddit = praw.Reddit(username=args[0], password=args[1], client_id=args[2],
                         client_secret=args[3], user_agent='This is a bot')

    '''my personal client_id = 0g1vLWnW_cUR4A
    my personal client_secret = rBvEc35KeH82VxphZ1Hv5Hnwhj8'''
    return reddit


# Running the bot, if the keyphrase is in new comments then check if ticker is in S&P500 or not and give response
def run_bot(reddit, keyphrase):
    for comment in reddit.subreddit('investing').comments(limit=40):
        if keyphrase in comment.body:

            oneticker = comment.body.replace(keyphrase, '')
            oneticker = oneticker.replace(' ', '')

            try:
                if check_tickers(oneticker) == True:
                    # Comment the latest closing price if ticker is in the S&P500 list
                    quote = str(getquote(oneticker))
                    quote = quote[15:]
                    quote = quote[:10]
                    reply = "The latest closing price of " + oneticker + " is " + quote
                    comment.reply(reply)

                else:
                    # Comment if company not in the list
                    reply = "This is not a company in the S&P 500"
                    comment.reply(reply)
            except:
                print("Failed")


# main fucntion
def main():
    keyphrase = '!quotethis'
    reddit = authenticate()
    run_bot(reddit, keyphrase)


if __name__ == '__main__':
    main()
