import dagshub
import mlflow
import torch
from transformers import BertTokenizer
import pandas as pd
import torch
# Reinitialize DagsHub
dagshub.init(repo_owner='TanveerAhmad01', repo_name='YouTubeInsightAI', mlflow=True)

# Load the model from DagsHub via MLflow
logged_model = "runs:/c4185e984d1144a7a6a47833428cede8/bert_model"
model = mlflow.pytorch.load_model(logged_model,map_location=torch.device('cpu'))

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model.eval()


def classify_comments(comments):
    """
    Classify a list of comments into negative, positive, and neutral categories.
    
    Parameters:
    - comments (list of str): List of text comments to classify
    
    Returns:
    - dict: Counts of negative, positive, and neutral comments
    """
    # Step 1: Preprocess the comments and prepare for model inference
    encodings = tokenizer(comments, padding=True, truncation=True, max_length=128, return_tensors='pt')

    # Step 2: Pass the encodings through the model
    with torch.no_grad():  # Disable gradient computation for inference
        outputs = model(**encodings)

    # Step 3: Get predictions (logits -> probabilities)
    logits = outputs.logits
    preds = torch.argmax(logits, dim=1)  # Get the predicted class indices

    # Step 4: Map the predictions back to the original labels (-1, 0, 1 -> negative, neutral, positive)
    label_map = {0: -1, 1: 0, 2: 1}  # Mapping for BERT output to sentiment labels
    sentiment_map = {-1: "negative", 0: "neutral", 1: "positive"}

    # Step 5: Count the number of each sentiment
    sentiment_counts = {"negative": 0, "neutral": 0, "positive": 0}

    for p in preds:
        sentiment = sentiment_map[label_map[p.item()]]
        sentiment_counts[sentiment] += 1

    return sentiment_counts


# Example usage:
comments_list = [
    "I love this product! It's amazing.",
    "This is the worst experience I've had.",
    "It was okay, neither good nor bad."
]

result = classify_comments(comments_list)
print(result)