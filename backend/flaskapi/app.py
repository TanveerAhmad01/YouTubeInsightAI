import sys
import os
from flask import Flask, request, render_template, redirect, url_for

# Add project root to sys.path so 'backend' becomes importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.scraping.script import scrape_youtube_comments
from backend.scripts.classify import calling_result

app = Flask(__name__, template_folder='../../extension_gui/templates')

result_global = None  # Temporary store for result

@app.route('/')
def index():
    return render_template('main.html')  # Show main.html

@app.route('/get_url', methods=['POST'])
def get_url():
    global result_global
    video_url = request.form.get('video_url')
    
    if not video_url:
        return "No URL provided", 400

    # Step 1: Scrape comments
    comments = scrape_youtube_comments(video_url)

    # Step 2: Get sentiment result from classification model
    result_global = calling_result()

    return redirect(url_for('show_result'))

@app.route('/result')
def show_result():
    global result_global

    return render_template('result.html', sentiment=result_global)

if __name__ == '__main__':
    app.run(debug=True)
