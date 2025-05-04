import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
# Load the model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)
model.load_state_dict(torch.load("saved_models/bert_model.pkl", map_location=torch.device('cpu')))
model.eval()

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def classify_comments(comments):
    encodings = tokenizer(comments, padding=True, truncation=True, max_length=128, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**encodings)
    logits = outputs.logits
    preds = torch.argmax(logits, dim=1)

    label_map = {0: -1, 1: 0, 2: 1}
    sentiment_map = {-1: "negative", 0: "neutral", 1: "positive"}

    sentiment_counts = {"negative": 0, "neutral": 0, "positive": 0}
    for p in preds:
        sentiment = sentiment_map[label_map[p.item()]]
        sentiment_counts[sentiment] += 1

    return sentiment_counts


df = pd.read_csv('backend/Data/youtube_comments.csv')  # adjust the path if needed

# Check if 'comment' column exists
if 'Comment' not in df.columns:
    raise ValueError("The CSV must contain a 'Comment' column.")

# Extract comments
comments = df['Comment'].dropna().astype(str).tolist()

# Run sentiment classification
results = classify_comments(comments)

# Print result
print("Sentiment Distribution:", results)
# result = classify_comments(test_comments)
# print(result)
