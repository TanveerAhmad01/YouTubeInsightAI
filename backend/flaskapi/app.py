import sys
import os
from flask import Flask, request, render_template, redirect, url_for
from backend.scraping.script import scrape_youtube_comments
from backend.scripts.classify import calling_result

app = Flask(__name__)
result_global = None  # Temporary store for result

@app.route('/')
def index():
    return render_template('index.html')  # HTML form to input video URL

@app.route('/get_url', methods=['POST'])
def get_url():
    global result_global
    video_url = request.form.get('video_url')
    
    if not video_url:
        return "No URL provided", 400

    # Step 1: Scrape comments
    comments = scrape_youtube_comments(video_url)

    # Step 2: Classify sentiment
    result_global = calling_result(comments)

    return redirect(url_for('show_result'))

@app.route('/result')
def show_result():
    global result_global

    sentiment = {
        "1": "Positive",
        "-1": "Negative",
        "0": "Neutral"
    }.get(str(result_global), "Unknown")

    return render_template('result.html', sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
