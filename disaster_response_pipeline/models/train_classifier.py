# Import libraries
import sys
import pandas as pd
from sqlalchemy import create_engine

import nltk
nltk.download(['punkt', 'wordnet', "stopwords"])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

import warnings
warnings.filterwarnings("ignore")

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.multioutput import MultiOutputClassifier
#from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.externals import joblib
from sklearn.metrics import classification_report, accuracy_score

# Load data from database
def load_data(database_filepath):
    """
    Method for loading data from the sqlite database
    
    Args:
        database_filepath (str): sqlite db filepath
        
    output:
        X (numpy.ndarray): Input training dataset
        Y (numpy.ndarray): Output training dataset
        category_names: Labels for categories
    """
    
    engine = create_engine("sqlite:///{}".format(database_filepath))
    df = pd.read_sql_table("messages", con = engine)
    X = df.message.values
    Y = df[df.columns[4:]].values
    category_names = list(df.columns[4:])
    
    return X, Y, category_names

def tokenize(text):
    """
    Method for tokenizing words
    
    Args:
        text (str): Message data for tokenization
        
    output:
        clean_tokens (str): Result list after tokenization
    """
    
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    
    clean_tokens = [word for word in clean_tokens if word not in stopwords.words("english")]
    
    return clean_tokens

# Build ML Model
def build_model():
    """
    Method for training model by creating ML pipeline and Grid Search for finding best parameters
    
    Args:
        None
        
    output:
        cv_results_ (dict of numpy ndarrays): Cross-validation Result
    """
    
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier(random_state = 0)))
    ])
    
    parameters = {
                'tfidf__smooth_idf':[True, False],
                'clf__estimator__n_estimators': [100, 110, 120]
    }
    
    cv = GridSearchCV(pipeline, param_grid = parameters, scoring = 'precision_samples', cv = 5, verbose = 5, n_jobs = -1)
    
    return cv

# ML Model evaluation
def evaluate_model(model, X_test, Y_test, category_names):
    """
    Method for evaluating model performance
    
    Args:
        model (dict of numpy ndarray): Classifier model
        X_test (numpy ndarray): Test input dataset
        Y_test (numpy ndarray): Test output dataset
    
    output:
        None
    """
    
    Y_pred = model.predict(X_test)
    
    print(classification_report(Y_test, Y_pred, target_names = category_names))
    print("..................................................")
    for i in range(Y_test.shape[1]):
        print("%25s accuracy : %.2f" %(category_names[i], accuracy_score(Y_test[:, i], Y_pred[:, i])))

# Store the model
def save_model(model, model_filepath):
    """
    Method for saving the model in pickle file
    """
    
    joblib.dump(model, model_filepath)

# Main function
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