import pandas as pd
import re
import html
import emoji
import string

def clean_text(text: str) -> str:
    """
    Clean a single YouTube comment string.

    Args:
        text (str): Raw text input

    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www.\S+", "", text)          

    # Remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)                 

    # Decode HTML entities (e.g., &amp; becomes &)
    text = html.unescape(text) 

    # Remove emojis
    text = emoji.replace_emoji(text, replace='')         

    # Remove all punctuation except periods, commas, and other useful punctuation
    # Keeping some punctuation that is often useful like period (.), comma (,), etc.
    text = text.translate(str.maketrans('', '', string.punctuation.replace('.', '').replace(',', '').replace('!', '').replace('?', ''))) 

    # Remove special characters that are not alphanumeric or spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()             

    return text


def clean_dataframe(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Clean a specific column in a pandas DataFrame and return only the 'comment' and 'label' columns.

    Args:
        df (pd.DataFrame): Your original DataFrame
        column (str): Name of the column to clean

    Returns:
        pd.DataFrame: Updated DataFrame with only 'comment' and 'label' columns
    """
    # Drop missing values (NaN) from the specified column
    df = df.dropna(subset=[column])

    # Clean the 'comment' column
    df['comment'] = df[column].apply(clean_text)

    # Retain only 'comment' and 'label' columns
    df = df[['comment', 'label']]

    return df


def clean_data_from_csv(file_path: str, column: str) -> pd.DataFrame:
    """
    Load a CSV file, clean a specific column, and return the cleaned DataFrame with only 'comment' and 'label' columns.

    Args:
        file_path (str): Path to the CSV file.
        column (str): Column name to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Clean the DataFrame using the specified column
    df_cleaned = clean_dataframe(df, column)

    return df_cleaned
