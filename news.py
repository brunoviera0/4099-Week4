from google.cloud import datastore   # Google Cloud Datastore
from newsapi import NewsApiClient    # News API client
from textblob import TextBlob        # Sentiment analysis
from datetime import datetime        # Handle date and time


# Make sure you have an API key from NewsAPI
# Before running this program, make sure to have run the following commmands in your terminal:

    # pip install google-cloud-datastore textblob newsapi-python
    # python -m textblob.download_corpora (this command downloads corpora for textBlob)

# Google Cloud project ID
PROJECT_ID = 'your-google-cloud-project-id'

# Initialize the Datastore client with project
client = datastore.Client(project=PROJECT_ID)

# News API key (replace with your own API key)
NEWS_API_KEY = 'your_newsapi_key_here'

# Initialize News API client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_news(topic):
    # Fetch the latest news articles for the given topic
    articles = newsapi.get_everything(q=topic, language='en', sort_by='publishedAt', page_size=5)

    # Check if any articles are found
    if not articles['articles']:
        print(f"No news found for the topic: {topic}")
        return []

    return articles['articles']

def analyze_sentiment(text):
    # Perform sentiment analysis on the news content
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a sentiment score between -1 (negative) and 1 (positive)

def store_news_data(article, topic):
    # Create a new entity in Datastore with kind 'newsData'
    entity = datastore.Entity(client.key('newsData'))

    # Perform sentiment analysis
    sentiment_score = analyze_sentiment(article['content'] or article['description'] or '')

    # Set the properties of the entity with news data
    entity.update({
        'topic': topic,                            # Topic of the news
        'title': article['title'],                 # News article title
        'description': article['description'],     # Short description of the article
        'sentiment_score': round(sentiment_score, 2),  # Sentiment score, rounded to 2 decimal places
        'url': article['url'],                     # URL of the news article
        'published_at': article['publishedAt'],    # When the article was published
        'timestamp': datetime.utcnow()             # Timestamp in UTC when data is stored
    })

    # Save the entity to Datastore
    client.put(entity)
    print(f"Stored article: {article['title']}")

def retrieve_news_data():  # Retrieve and display all stored news data
    # Create a query for entities of kind 'newsData'
    query = client.query(kind='newsData')

    # Fetch all entities matching the query
    results = query.fetch()

    # Display each entity's data with iteration
    for entity in results:
        print(f"{entity['published_at']} - {entity['title']}")
        print(f"Sentiment Score: {entity['sentiment_score']}, URL: {entity['url']}")
        print(f"Description: {entity['description']}\n")

if __name__ == '__main__':
    # Set the news topic for which to fetch articles
    news_topic = 'technology'  # Can be any topic, e.g., "technology", "finance", "politics", etc.

    # Fetch news articles for the given topic
    news_articles = fetch_news(news_topic)

    # Store news data in Datastore
    for article in news_articles:
        store_news_data(article, news_topic)

    # Retrieve and display all stored news data
    retrieve_news_data()
