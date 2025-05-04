# main.py

import pandas as pd
from clean_data import clean_data_from_csv
from bert_sentiment import run_bert_sentiment_pipeline

def main():
    # File path to the dataset
    file_path = "E:/Tanveer Data/YouTubeInsightAI/backend/Data/data.csv"
    
    # Clean the data
    print("Cleaning the data...")
    df_cleaned = clean_data_from_csv(file_path, 'comment')  # Assuming 'comment' is the text column
    
    # Run BERT sentiment analysis pipeline
    print("Running the BERT sentiment pipeline...")
    trainer, eval_result = run_bert_sentiment_pipeline(df_cleaned, text_col='comment', label_col='label', num_labels=3)

    # You can print or log the evaluation result for further analysis
    print("Evaluation Result:", eval_result)

    

if __name__ == "__main__":
    main()
