# Import modules
import sys
import pandas as pd
from sqlalchemy import create_engine

# Load datasets
def load_data(messages_filepath, categories_filepath):
    """
    Method for reading two CSV files and merge into one pandas dataframe
    
    The function reads CSV file of messages and categories and merge them into one pandas dataframe

    Args:
        messages_filepath (str): The .csv file path of messages dataset
        categories_filepath (str): The .csv file path of categories dataset
        
    output:
        df (pandas dataframe): Return merged dataset of messages and categories
    """
    
    # Read input dataset
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # Merge two dataframes into one dataframe
    df = pd.merge(messages, categories, on = "id", how = "outer")
    
    return df

# Clean the dataset
def clean_data(df):
    """
    Method for cleaning the dataframe obtained from 'load_data'
    
    Args:
        df (pandas dataframe): The merged dataframe from load_data
    
    output:
        df (pandas dataframe): Sanitized dataframe
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
    
    # Some rows on related column has value of 2
    # Replace 2 with 1
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
    Method for saving the clean dataframe into an sqlite database

    Args:
        df (pandas dataframe): Sanitized dataframe obtained from 'clean_data'
        database_filename (str): DB filename

    Output:
        None
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