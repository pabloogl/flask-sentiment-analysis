import pandas as pd
from ntscraper import Nitter
import re
from nltk.corpus import stopwords
import nltk
import emoji
from pysentimiento import create_analyzer
from langdetect import detect
import matplotlib.pyplot as plt

scraper = Nitter(log_level= 0, skip_instance_check=False)
language = ""


def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'http\S+', '', tweet)  # Deletes URLs
    tweet = re.sub(r'@\w+', '', tweet)  # Deletes mentions
    tweet = re.sub(r'#\w+', '', tweet)  # Deletes hashtags
    tweet = re.sub(r'\d+', '', tweet)  # Deletes numbers
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words])
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
    print(final_tweets)
    return df


tweets = get_tweets(query="estoy cansado de", lang="es", num_tweets= 10)
df = tweets_to_df(tweets)


nltk.download('stopwords')
stopword_en = nltk.corpus.stopwords.words('english')
stopword_es = nltk.corpus.stopwords.words('spanish')
stop_words = stopword_en + stopword_es

labels = ['POS', 'NEU', 'NEG', 'DOMINANT_SENTIMENT']
df[labels] = df.apply(apply_sentiment, axis=1)


plt.figure(figsize=(10,6))
plt.hist(df['POS'], bins= 20, label='POS', color= 'blue')
plt.hist(df['NEU'], bins=20, alpha=0.7, label='NEU', color='green')
plt.hist(df['NEG'], bins=20, alpha=0.7, label='NEG', color='red')

# Title and labels
plt.title('Distribución de Sentimientos (POS, NEU, NEG)')
plt.xlabel('Valor de Sentimiento')
plt.ylabel('Frecuencia')
plt.legend()

# Show visuals
plt.show()

