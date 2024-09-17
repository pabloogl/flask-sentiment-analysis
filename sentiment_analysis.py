import pandas as pd
from ntscraper import Nitter
import re
from nltk.corpus import stopwords
import emoji
from pysentimiento import create_analyzer
from langdetect import detect


def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'http\S+', '', tweet)  # Deletes URLs
    tweet = re.sub(r'@\w+', '', tweet)  # Deletes mentions
    tweet = re.sub(r'#\w+', '', tweet)  # Deletes hashtags
    tweet = re.sub(r'\d+', '', tweet)  # Deletes numbers
    tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
    tweet = emoji.replace_emoji(tweet, replace= '') # Deletes emojis
    return tweet

def get_language(txt: str):
    return detect(txt)
    
def get_sentiment(tweet):
    analyzer = create_analyzer(task="sentiment", lang= language)
    return analyzer.predict(tweet).probas

def apply_sentiment(row):
    cleaned_tweet = clean_tweet(row['text'])
    sentiment = get_sentiment(cleaned_tweet) 
    dominant_sentiment = max(sentiment, key=sentiment.get)
    return pd.Series({
        'POS': sentiment['POS'],
        'NEU': sentiment['NEU'],
        'NEG': sentiment['NEG'],
        'DOMINANT_SENTIMENT': dominant_sentiment
    })

def get_tweets(query: str, mode: str = "term", num_tweets: int = 100, lang = 'es'):
    '''
    Main function for web scraping tweets.
    Args:
        query: Words that are going to be searched
        mode: Searching query as a "term", "hashtag" or a "user" tweet
        num_tweets: Number of tweets to be scraped
        lang: Language of the tweets to be scraped
    '''
    global language
    language = lang
    tweets = scraper.get_tweets(terms= query, mode= mode, number= num_tweets, language= lang)
    return tweets

def tweets_to_df(tweets):
    '''
        Process the dictionary data from get_tweets function
        Args:
            tweets: Json type data collected through get_tweets

        Output:
            Pandas DataFrame with profle_id, text columns
    '''
    final_tweets = []
    for tweet in tweets['tweets']:
        data = [tweet['user']['profile_id'], tweet['text']]
        final_tweets.append(data)
    df = pd.DataFrame(final_tweets)
    df.columns = ["profile_id", "text"]
    
    labels = ['POS', 'NEU', 'NEG', 'DOMINANT_SENTIMENT']
    df[labels] = df.apply(apply_sentiment, axis=1)
    return df




