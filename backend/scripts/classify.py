import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load the model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)
model.load_state_dict(torch.load("backend/model/bert_model.pkl", map_location=torch.device('cpu')))
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


# result = classify_comments(test_comments)
# print(result)
