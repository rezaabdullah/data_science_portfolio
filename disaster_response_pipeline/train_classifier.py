# Import libraries
import sys
import pandas as pd
import numpy as np

from sqlalchemy import create_engine

import re
import pickle
import nltk
nltk.download(['punkt', 'wordnet', "stopwords"])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score

# Load data from database
def load_data(database_filepath):
    """
    Load data from the sqlite database
    
    input:
        database_filepath: sql db filepath
    output:
        X: Input training dataset
        Y: Output training dataset
        category_names: Labels for categories
    """
    
    # Load the dataset to dataframe
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('messages', con=engine)

    # Split the dataframe into x and y
    X = df['message']
    Y = df.drop(columns=['id','message','original','genre'])
    #Y = df[df.columns[4:]].values
    #Y = df.loc[:, [4:]].values

    # Get the label names
    category_names = Y.columns

    return X, Y, category_names

# Write a tokenization function to process your text data
def tokenize(text):
    """
    Tokenize and lemmatize each word in a given text
    
    input:
        text: Tokenize messages
    output:
        clean_tokens: Result list after tokenization.
    """

    # Normalise the texts and remove punctuation
    text = re.sub(r"[^\w\s]", " ", text.lower())
    
    # Create token
    tokens = word_tokenize(text)
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words("english")]
    
    # Lemmatise each words
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Lemmatize each word in tokens
    """
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    """
    return clean_tokens

# Build a machine learning pipeline
def build_model():
    """
    Creates machine learning pipeline for learning
    
    :Input:
        :None: Doesn't require an input
    :Returns:
        :pipeline: Machine Learning pipeline with fit/predict methods
    """

    # Create a pipeline consists of count vectorizer -> KneighborsClassifier()
    pipeline = Pipeline([
        ('text_pipeline', Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidf', TfidfTransformer())
        ])),
        ('clf', MultiOutputClassifier(KNeighborsClassifier()))
    ])

    ## Find the optimal model using GridSearchCV
    parameters = {
        'text_pipeline__tfidf__use_idf': (True, False),
        'clf__estimator__weights': ['uniform', 'distance']
    }

    pipeline = GridSearchCV(pipeline, param_grid=parameters, verbose=5, cv=2, n_jobs=2)

    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """Display the classification report for the given model"""

    # Predict the given X_test and create the report based on the Y_pred
    Y_pred = model.predict(X_test)
    print(classification_report(Y_test, Y_pred, target_names=category_names))


def save_model(model, model_filepath):
    """Save the given model into pickle object"""

    # Save the model based on model_filepath given
    pkl_filename = '{}'.format(model_filepath)
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()