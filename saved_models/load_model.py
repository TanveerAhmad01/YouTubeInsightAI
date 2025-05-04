import dagshub
import mlflow
import torch
import os

def save_model():
    # Initialize DagsHub MLflow tracking
    dagshub.init(repo_owner='TanveerAhmad01', repo_name='YouTubeInsightAI', mlflow=True)

    # Load the model from DagsHub via MLflow
    logged_model = "runs:/c4185e984d1144a7a6a47833428cede8/bert_model"
    model = mlflow.pytorch.load_model(logged_model, map_location=torch.device('cpu'))

    # Save the model to a pickle file
    os.makedirs("saved_models", exist_ok=True)
    torch.save(model.state_dict(), "saved_models/bert_model.pkl")

save_model()