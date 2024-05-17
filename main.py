import nltk
from flask import Flask, request, render_template
from nltk.sentiment import SentimentIntensityAnalyzer
from google_play_scraper import app, Sort, reviews_all

nltk.download('vader_lexicon')

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    game_id = request.form.get('game_id')
    
    # game_info = app(game_id)
    game_reviews = reviews_all(
        'com.mobile.legends',
        lang='id',
        country='id',
        sort=Sort.MOST_RELEVANT,
        count=2000,
        filter_score_with= None
    )
    
    review_sentiments = []
    for review in game_reviews:
        polarity_scores = sia.polarity_scores(review['content'])
        sentiment = 'Positif' if polarity_scores['compound'] > 0.5 else 'Negatif'
        review_sentiments.append((review['content'], sentiment))
    
    return render_template('index.html', review_sentiments=review_sentiments)
