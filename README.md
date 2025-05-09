# YouTubeInsightAI 🎥🧠

YouTubeInsightAI is an advanced sentiment analysis system designed to evaluate YouTube video credibility based on the comments section. It combines web scraping, NLP, and deep learning (BERT) to generate real-time insights, integrated with a Chrome Extension UI and deployed using MLflow on DagsHub.

---

## 🚀 Features

- 🔎 **YouTube Comment Scraper**: Extracts comments directly from YouTube videos.
- 🧠 **BERT-Based Sentiment Analysis**: Uses a fine-tuned BERT model for classifying comment sentiments.
- 🧪 **MLflow Integration**: Tracks experiments and model performance seamlessly.
- 🌐 **Chrome Extension**: GUI for real-time analysis from within YouTube.
- 📊 **Model Evaluation Pipeline**: Automated using GitHub Actions for reproducibility.
- 🗃️ **Project Versioning**: Managed using DVC and tracked on DagsHub.

---

## 📁 Project Structure

```
YouTubeInsightAI/
├── Chrome_Extension/        # Frontend to display results on YouTube
├── comment_fetcher/         # Web scraping logic using Selenium
├── model/                   # BERT training, evaluation, and tokenizer
├── pipeline/                # Orchestration scripts for preprocessing, training, inference
├── .github/workflows/       # GitHub Actions CI/CD
├── MLproject                # MLflow project configuration
├── dvc.yaml                 # DVC pipeline definition
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Chrome Browser
- ChromeDriver (matching your Chrome version)
- Node.js (for Chrome Extension if development is needed)
- Docker (optional for deployment)

### Setup

1. **Clone the repository**  
```bash
git clone https://github.com/TanveerAhmad01/YouTubeInsightAI.git
cd YouTubeInsightAI
```

2. **Create a virtual environment & activate it**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Set up ChromeDriver**  
Ensure `chromedriver` is added to your system path and matches your browser version.

5. **Run the pipeline**  
```bash
python pipeline/run_pipeline.py
```

---

## ⚙️ Usage

### ▶️ Run Sentiment Analysis

- Automatically scrape YouTube comments.
- Process them with BERT model.
- Get sentiment scores: **Positive**, **Negative**, or **Neutral**.
- View results directly on YouTube using the Chrome Extension.

### 💻 Chrome Extension

1. Navigate to `chrome://extensions/`
2. Enable **Developer Mode**
3. Click **Load Unpacked**
4. Select the `Chrome_Extension/` folder

---

## 📈 Model Tracking with MLflow

Track metrics, parameters, and models:

```bash
mlflow ui
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 📦 Versioning with DVC

To pull datasets and model artifacts:

```bash
dvc pull
```

---

## 🤖 GitHub Actions

CI/CD pipeline for:
- Model training
- Evaluation
- Reporting

Check `.github/workflows/` for automation configuration.

---

## 📊 Results

- Accuracy: 87%
- F1 Score: 80%+
- Precision / Recall: Available in `model/evaluation/metrics.json`

---

## 🤝 Contributing

**Tanveer Ahmad**  
🔗 [LinkedIn](https://www.linkedin.com/in/tanveer-ahmad-22431529a/)  
💻 [GitHub](https://github.com/TanveerAhmad01)

**Muhammad Bilal Sajid**  
🔗 [LinkedIn](https://www.linkedin.com/in/muhammad-bilal-sajid-/)  
💻 [GitHub](https://github.com/BilalSajid202)

**Abdul Moeez**  
🔗 [LinkedIn](https://www.linkedin.com/in/abdulmoeez1/)  
💻 [GitHub](https://github.com/mianabdulmoez)


---

## 👤 Authors

**Tanveer Ahmad**  
🔗 [LinkedIn](https://www.linkedin.com/in/tanveer-ahmad-22431529a/)  
💻 [GitHub](https://github.com/TanveerAhmad01)

**Muhammad Bilal Sajid**  
🔗 [LinkedIn](https://www.linkedin.com/in/muhammad-bilal-sajid-/)  
💻 [GitHub](https://github.com/BilalSajid202)

**Abdul Moeez**  
🔗 [LinkedIn](https://www.linkedin.com/in/abdulmoeez1/)  
💻 [GitHub](https://github.com/mianabdulmoez)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---


## ⭐ Acknowledgements

- Hugging Face 🤗 Transformers
- Selenium for scraping
- MLflow for model tracking
- DagsHub for version control and collaboration
