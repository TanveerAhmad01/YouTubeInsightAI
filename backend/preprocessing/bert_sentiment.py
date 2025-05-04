# bert_sentiment.py

import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import classification_report, accuracy_score
from torch.utils.data import Dataset
import mlflow
import dagshub

# Enable DagsHub logging
dagshub.init(repo_owner='TanveerAhmad01', repo_name='YouTubeInsightAI', mlflow=True)

def run_bert_sentiment_pipeline(df_cleaned, text_col, label_col, num_labels):
    # Step 1: Prepare data
    X = df_cleaned[text_col]
    y = df_cleaned[label_col]
    
    # Split into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    
    # Map labels (-1, 0, 1) to (0, 1, 2)
    label_map = {-1: 0, 0: 1, 1: 2}
    y_train_mapped = y_train.map(label_map)
    y_val_mapped = y_val.map(label_map)

    # Load tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Tokenize data
    train_encodings = tokenizer(X_train.tolist(), padding=True, truncation=True, max_length=128, return_tensors='pt')
    val_encodings = tokenizer(X_val.tolist(), padding=True, truncation=True, max_length=128, return_tensors='pt')

    # Define custom dataset
    class CustomDataset(Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = torch.tensor(labels, dtype=torch.long)

        def __getitem__(self, idx):
            item = {key: val[idx] for key, val in self.encodings.items()}
            item['labels'] = self.labels[idx]
            return item

        def __len__(self):
            return len(self.labels)

    # Create datasets
    train_dataset = CustomDataset(train_encodings, y_train_mapped.values)
    val_dataset = CustomDataset(val_encodings, y_val_mapped.values)

    # Load model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)

    # Set training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        report_to="none",  # Disable wandb/huggingface hub logging
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Train model
    trainer.train()

    # Evaluate the model
    predictions = trainer.predict(val_dataset)
    preds = torch.argmax(torch.tensor(predictions.predictions), axis=1)

    # Reverse label map for original labels
    reverse_label_map = {0: -1, 1: 0, 2: 1}
    y_pred = preds.numpy()
    y_pred_labels = [reverse_label_map[p] for p in y_pred]
    y_true_labels = y_val.values

    # Print classification report
    eval_result = classification_report(y_true_labels, y_pred_labels)
    report = classification_report(y_true_labels, y_pred_labels, output_dict=True)
    accuracy = accuracy_score(y_true_labels, y_pred_labels)
    print(eval_result)

    # Conditionally log to MLflow
    log_to_mlflow(model, report, accuracy)

    return trainer, eval_result


def log_to_mlflow(model, report, accuracy):
    accuracy_threshold = 0.80
    metric_threshold = 0.70
    required_labels = ['-1', '0', '1']

    if accuracy < accuracy_threshold:
        print("❌ Model accuracy below 80%. Not logging to MLflow.")
        return

    for label in required_labels:
        metrics = report.get(label)
        if not metrics:
            print(f"❌ Metrics missing for class {label}. Not logging to MLflow.")
            return
        if any(metrics[metric] < metric_threshold for metric in ['precision', 'recall', 'f1-score']):
            print(f"❌ One or more metrics below 70% for class {label}. Not logging to MLflow.")
            return

    with mlflow.start_run():
        print("✅ Logging model to MLflow...")
        mlflow.log_metric("accuracy", accuracy)
        for label, metrics in report.items():
            if isinstance(metrics, dict) and "precision" in metrics:
                mlflow.log_metric(f"{label}_precision", metrics["precision"])
                mlflow.log_metric(f"{label}_recall", metrics["recall"])
                mlflow.log_metric(f"{label}_f1-score", metrics["f1-score"])

        mlflow.pytorch.log_model(
            model,
            artifact_path="bert_model",
            registered_model_name="bert-sentiment-model"
        )
