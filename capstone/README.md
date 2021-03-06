# Capstone Project: Create a Customer Segmentation Report
### Project Motivation
In this project, demographics data for customers of a mail-order sales company in Germany will be analyzed. The dataset will be compared against demographics information for the general population. There are two main objectives of the project:
1. To identify core customer base of the company
2. Determine individuals who are most liely to get converted into customers

The blog on the project can be found on [medium](https://medium.com/@abdullahreza/find-your-core-customers-and-determine-customer-segments-e5a49180d95c)

### Brief Overview of the Process
1. Part 0  
    a. Data exploration  
    b. Data cleaning  
    c. Feature engineering  
2. Part 1: Unsupervised machine learning to identify features of core customers
3. Part 2: Supervised machine learning to identify individuals who will be converted to customers
4. Part 3: Predict the response of a testing dataset based on the model created on Part 2.

### Problem Statement
1. How to identify core demographics of customers from demographics of general population
2. Find clusters of customers and determine who are most likely to be converted into customers

### Results:
1. For unsupervised model PCA and KMeans were applied to identify groups of individuals who best describe the core customer base. 6 clusters were identified with cluster 1, 4 and 5 underpresented in the customers while 0, 2 and 3 are well represented.
2. In supervised machine learning five models were applied with Logistic Regression yielding the best result; a score of 0.55.

### Required Libraries
1. numpy
2. pandas
3. collections
4. operator
5. time
6. sklearn
7. matplotlib
8. seaborn

### Data
1. Demographics data for customers of a mail-order sales company in Germany.
2. Demographics information for the general population of Germany.
3. Demographics information for targets of a marketing campaign for the company - Train Set
4. Demographics information for targets of a marketing campaign for the company - Test Set

### Description of the Files
`Arvato_Project_Workbook.ipynb` is a jupyter notebook file which contains all the scripts including functions and charts.

### Improvements
There are few improvements that could improve the model result
1. Drop fewer columns: explore each feature and determine whether the feature should be dropped. 
2. Impute features with a different strategy based on feature type i.e. numerical, categorical and ordinal.
3. Apply Multi Factor Analysis instead of PCA
4. Try different classification models with hyperparameter tuning.

### Acknowledgement
1. Arvato Financial Solutions
2. Udacity
3. [Tobias Gorgs](https://github.com/Tobi81)