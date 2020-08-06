# Disaster Response Pipeline

### Project Motivation
In this project, disaster data obtained from Figure Eight will be analyzed and a classifier model will be developed to classify the messages for facilitating faster response from the various emergency teams. The dataset contains pre-labelled tweet and messages from real-life disaster events. The objective of the project is to build a Natural Language Processing (NLP) model to categorize messages on a real time that can be relayed to appropriate emergency response teams to take necessary actions.

### Description of Files
To create end-to-end solution, the project adhere to the three steps of data science. The files are organized into the steps they belong to.
1. ETL Process (Data Preprocessing): `data` 
2. Building Models (Data Processing): `models`
3. Create Dashboard (Data Postprocessing): `app`

```
- app
| - template
| |- master.html            # main page of web app
| |- go.html                # classification result page of web app
|- run.py                   # Flask file that runs app

- data
|- disaster_categories.csv  # data to process 
|- disaster_messages.csv    # data to process
|- process_data.py
|- DisasterResponse.db      # database to save clean data to

- models
|- train_classifier.py
|- classifier.pkl           # saved model 

- README.md
```