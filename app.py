from flask import Flask, request, send_file, jsonify
import io
from sentiment_analysis import get_tweets, tweets_to_df, apply_sentiment, clean_tweet
import matplotlib.pyplot as plt
import pandas as pd
import nltk

app = Flask(__name__)

nltk.download('stopwords')

@app.route('/sentiment', methods=['GET'])
def sentiment_analysis():
    query = request.args.get('query', default='', type=str)
    lang = request.args.get('lang', default='es', type=str)
    num_tweets = request.args.get('num_tweets', default=10, type=int)

    tweets = get_tweets(query=query, lang=lang, num_tweets=num_tweets)
    df = tweets_to_df(tweets)

    labels = ['POS', 'NEU', 'NEG', 'DOMINANT_SENTIMENT']
    df[labels] = df.apply(apply_sentiment, axis=1)

    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/sentiment/plot', methods=['GET'])
def sentiment_plot():
    query = request.args.get('query', default='', type=str)
    lang = request.args.get('lang', default='es', type=str)
    num_tweets = request.args.get('num_tweets', default=10, type=int)

    tweets = get_tweets(query=query, lang=lang, num_tweets=num_tweets)
    df = tweets_to_df(tweets)

    plt.figure(figsize=(10, 6))
    plt.hist(df['POS'], bins=20, label='POS', color='blue', alpha=0.7)
    plt.hist(df['NEU'], bins=20, label='NEU', color='green', alpha=0.7)
    plt.hist(df['NEG'], bins=20, label='NEG', color='red', alpha=0.7)

    plt.title('Distribución de Sentimientos (POS, NEU, NEG)')
    plt.xlabel('Valor de Sentimiento')
    plt.ylabel('Frecuencia')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)