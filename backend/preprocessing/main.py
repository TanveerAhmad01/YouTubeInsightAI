
import os
import pandas as pd
from clean_data import clean_data_from_csv
from bert_sentiment import run_bert_sentiment_pipeline

def main():
    # Use relative path for GitHub Actions compatibility
    file_path = os.path.join("backend", "Data", "data.csv")
    
    # Clean the data
    print("Cleaning the data...")
    df_cleaned = clean_data_from_csv(file_path, 'comment')  # Assuming 'comment' is the text column
    
    # Run BERT sentiment analysis pipeline
    print("Running the BERT sentiment pipeline...")
    trainer, eval_result = run_bert_sentiment_pipeline(df_cleaned, text_col='comment', label_col='label', num_labels=3)

    # Print the evaluation result
    print("Evaluation Result:", eval_result)

if __name__ == "__main__":
    main()
