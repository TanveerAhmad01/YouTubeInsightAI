# Flask Integration Guide

This document outlines how to integrate this React frontend with a Flask backend for URL analysis.

## Flask Backend Setup

1. Create a basic Flask application structure:

```
backend/
  ├── app.py
  ├── requirements.txt
  └── utils/
      └── url_analyzer.py
```

2. Install required packages:

```
pip install flask flask-cors requests beautifulsoup4
```

3. Basic Flask app structure (`app.py`):

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.url_analyzer import analyze_url

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    
    try:
        result = analyze_url(data['url'])
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    # In a real app, this would fetch from a database
    # For demo purposes, returning mock data
    return jsonify({
        'success': True,
        'data': [
            {
                'url': 'https://example.com',
                'analyzed_at': '2023-09-15T10:30:00Z',
                'title': 'Example Domain'
            }
            # More history items
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
```

4. URL Analyzer module (`utils/url_analyzer.py`):

```python
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import random

def analyze_url(url):
    """Analyze a URL and return comprehensive information"""
    
    start_time = time.time()
    
    # Make request to the URL
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract basic information
    title = soup.title.string if soup.title else 'No title'
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'] if meta_description else 'No description'
    
    # Analyze meta tags
    meta_tags = {}
    for tag in soup.find_all('meta'):
        name = tag.get('name') or tag.get('property')
        if name and tag.get('content'):
            meta_tags[name] = tag.get('content')
    
    # Check for headings
    headings = bool(soup.find_all(['h1', 'h2', 'h3']))
    
    # Check for images with alt text
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    images_have_alt = len(images_with_alt) / len(images) > 0.8 if images else False
    
    # Calculate load time
    load_time = f"{time.time() - start_time:.1f}s"
    
    # Extract technologies (simplified demo)
    technologies = []
    if soup.find('script', src=lambda s: s and 'react' in s.lower()):
        technologies.append('React')
    if soup.find('link', href=lambda s: s and 'tailwind' in s.lower()):
        technologies.append('Tailwind CSS')
    if soup.find('script', src=lambda s: s and 'jquery' in s.lower()):
        technologies.append('jQuery')
    
    # For demo purposes, add some random technologies
    possible_techs = ['Node.js', 'Express', 'Vue.js', 'Angular', 'WordPress', 'Bootstrap']
    technologies.extend(random.sample(possible_techs, k=min(2, len(possible_techs))))
    
    # Calculate security score (simplified demo)
    security_score = random.randint(60, 95)
    
    # Prepare result
    result = {
        'url': url,
        'title': title,
        'description': description,
        'statusCode': response.status_code,
        'contentType': response.headers.get('Content-Type', 'Unknown'),
        'server': response.headers.get('Server', 'Unknown'),
        'securityScore': security_score,
        'performance': {
            'loadTime': load_time,
            'resourceCount': len(soup.find_all(['script', 'link', 'img'])),
            'totalSize': f"{len(response.content) / 1024:.1f} KB"
        },
        'seo': {
            'title': bool(title and len(title) > 5),
            'description': bool(description and len(description) > 10),
            'headings': headings,
            'images': images_have_alt
        },
        'technologies': technologies,
        'metaTags': meta_tags
    }
    
    return result
```

## Connecting React to Flask

1. Set environment variables in your React app:

Create a `.env` file in the React project root:
```
VITE_API_BASE_URL=http://localhost:5000/api
```

2. Start both applications:

- Flask backend: `cd backend && python app.py`
- React frontend: `npm run dev`

## Production Deployment

For production, you would typically:

1. Build the React app (`npm run build`)
2. Configure Flask to serve the built static files
3. Deploy both to a production server

Example production Flask setup:

```python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.url_analyzer import analyze_url
import os

app = Flask(__name__, static_folder='../dist')
CORS(app)

# API routes
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Same as before...

@app.route('/api/history', methods=['GET'])
def history():
    # Same as before...

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```