from google.cloud import datastore   #google Cloud Datastore
import yfinance as yf               #yahoo Finance
from datetime import datetime       #handle date and time

#Google Cloud project ID
PROJECT_ID = 'linear-listener-436516-c9'

#initialize the Datastore client with project
client = datastore.Client(project=PROJECT_ID)

def store_stock_data(ticker):
    #fetch stock data for the given ticker symbol
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')  #latest day's data

    #check if data is available
    if data.empty:
        print("No data found for", ticker)
        return

    #new entity in Datastore with kind 'stockData'
    entity = datastore.Entity(client.key('stockData'))

    #set the properties of the entity with stock data
    entity.update({
        'ticker': ticker,                          #ticker symbol
        'price': round(data['Close'][0], 2),       #closing price, rounded to 2 decimal places
        'volume': int(data['Volume'][0]),          #trading volume
        'timestamp': datetime.utcnow()             #timestamp in UTC
    })

    #save the entity to Datastore
    client.put(entity)
    print(f"Stored data for {ticker}")

def retrieve_stock_data(): #retrieve all stored data and display it
    #create a query for entities of kind 'stockData'
    query = client.query(kind='stockData')

    #fetch all entities matching the query
    results = query.fetch()

    #display each entity's data w/ iteration
    for entity in results:
        print(f"{entity['timestamp']} - {entity['ticker']}: ${entity['price']} (Volume: {entity['volume']})")

if __name__ == '__main__':
    #set the ticker symbol for which to fetch stock data
    ticker_symbol = 'MSFT' #AMZN, MSFT

    #everytime you change the ticker symbol, the retrieval function will remember past stock info.

    #store stock data in Datastore
    store_stock_data(ticker_symbol)

    #call the function to retrieve and display all stored stock data
    retrieve_stock_data()
