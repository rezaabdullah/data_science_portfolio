# Import modules
import sys
import pandas as pd
from sqlalchemy import create_engine

# Load datasets
def load_data(messages_filepath, categories_filepath):
    """
    Read .csv files for messages and categories dataset and merge it into one dataframe
    
    input:
        messages_filepath: The .csv file path of messages dataset
        categories_filepath: The .csv file path of categories dataset
        
    output:
        df: Return merged dataset
    """
    
    # Read input dataset
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # Merge input dataframes
    df = pd.merge(messages, categories, on = "id", how = "outer")
    
    return df

# Clean the dataset
def clean_data(df):
    """
    Clean the merged dataset from load_data
    
    input:
        df: The merged dataset from load_data
    
    output:
        df: Clean dataset
    """
    
    # Split categories into separate category columns
    # Ceate a dataframe of the 36 individual category columns
    categories = df.categories.str.split(';', expand = True)
    
    # Select the first row of the categories dataframe
    row = categories.loc[0]
    
    # Use this row to extract a list of new column names for categories
    category_colnames = row.str.split("-").str[0].tolist()
    
    # Rename the columns of `categories`
    categories.columns = category_colnames
    
    # Convert category values to just numbers 0 or 1
    for column in categories:
        categories[column] = categories[column].astype(str).str[-1]
        categories[column] = pd.to_numeric(categories[column])
    
    # Replaces rows with value 2 of 'related' column to 1
    categories['related'] = categories['related'].replace(2, 1)
    
    # Replace categories column in df with new category columns
    df.drop('categories', axis = 1, inplace = True)
    
    # Concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1)
    
    # Deduplication
    df.drop_duplicates(inplace = True)
    
    return df

# Save the clean dataset into an sqlite database
def save_data(df, database_filename):
    """
    Save the clean dataframe into an sqlite database
    """

    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('messages', engine, index = False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()