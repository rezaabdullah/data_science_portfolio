# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load data
def load_data(azdias_filepath, customers_filepath, attributes_filepath, attributes_desc_filepath):
    """
    Method for loading dataset from CSV & Excel

    Since the dataset is more than 1GB, c engine instead of python to load data faster. In addition, there are 
    mixed data in column 18 & 19; more specifically some NaN values are represented by X & XX. These values are
    set as na_values.
    
    Args:
        azdias_filepath (str): Azdias filepath (Udacity_AZDIAS_052018)
        customers_filepath (str): Customers filepath (Udacity_CUSTOMERS_052018)
        attributes_filepath (str): Attributes filepath (DIAS Attributes - Values 2017.xlsx)
        attributes_desc_filepath (str): Attributes description (DIAS Information Levels - Attributes 2017.xlsx)
        
    Output:
        azdias: Pandas Dataframe
        customers: Pandas Dataframe
        attributes: Pandas Dataframe
        attributes_desc: Pandas Dataframe
    """
    
    # Load "azdias" dataset
    azdias = pd.read_csv(azdias_filepath, na_values=["X", "XX"], engine="c")
    # Set LNR as index
    #azdias = azdias.set_index("LNR")
    
    # Load "customers" dataset
    customers = pd.read_csv(customers_filepath, na_values=["X", "XX"], engine="c")
    # Set LNT as index
    #customers = customers.set_index("LNR")
    
    # Load "attributes" dataset
    attributes = pd.read_excel(attributes_filepath, header=1).loc[:, ["Attribute", "Value", "Meaning"]].fillna(method='ffill')
    
    # Load "attributes_desc"
    attributes_desc = pd.read_excel(attributes_desc_filepath, header=1).loc[:, ["Information level", "Attribute", "Description",
                                                                                "Additional notes"]].fillna(method='ffill')
    
    return azdias, customers, attributes, attributes_desc

# Create a dataframe that describes the information about each features
def build_feat_info(df):
    """
    Method for finding statistics for each features in a dataset

    Args:
        df (Pandas Dataframe): Dataframe that needs to be described
        
    Output:
        Pandas Dataframe
    """

    return pd.DataFrame({
        "value_count" : [df[x].count() for x in df.columns],
        "value_distinct" : [df[x].unique().shape[0] for x in df.columns],
        "num_nans" : [df[x].isnull().sum() for x in df.columns],
        "percent_nans" : [round(df[x].isnull().sum()/df[x].shape[0], 3) for x in df.columns],
    }, index=df.columns)

# Plot bar plots
def bar_plt_nan(series1, series2):
    """
    Method for plotting NaN counts for each features
    
    Args:
        series1: Series of NaN count for each feature
        series2: Series of NaN count for each feature
    
    Output:
        fig: matplotlib Figure
    """
    
    fig = plt.figure(figsize=(8,6))
    
    ax1 = fig.add_axes([0, 0.85, 1, 0.5])
    ax1.set_title("azdias: Distribution of NaN Count")
    ax1.set_xlabel("Number of NaN Count") 
    ax1.set_ylabel("Number of Features") 
    ax1.hist(series1, bins=100)
    
    ax2 = fig.add_axes([0, 0.15, 1, 0.5])
    ax2.hist(series2, bins=100)
    ax2.set_title("customers: Distribution of NaN Count")
    ax2.set_xlabel("Number of NaN Count") 
    ax2.set_ylabel("Number of Features")
    
    return None

# Replace unknown values with NaN
def replace_nan(df1, df2):
    """
    Method for substituting unknown values with NaN
    
    There are unknowns mapped to values in df1. These values are needed to be encoded to NaN in df2
    
    Args:
        df1 (Pandas Dataframe): Features dataframe with mapped values
        df2 (Pandas Dataframe): azdias or customers dataframe
        
    Output:
        df2 (Pandas Dataframe): Dataframe with unknown values replaced by NaN
    """
    
    # Create a subset of "attributes" with each feature and the associated unknown values
    df1 = df1[(df1["Meaning"].str.contains("unknown") | df1["Meaning"].str.contains("no "))]

    # Create a list of unknown value for each feature
    unknown_val = []
    for attribute in df1["Attribute"].unique():
        val = df1.loc[df1["Attribute"] == attribute, "Value"].astype("str").str.cat(sep=",").split(",")
        val = list(map(int, val)) # Convert the list to "int"
        unknown_val.append(val)

    # Create a dataframe of features with the list unknown value
    df1 = pd.concat([pd.Series(df1["Attribute"].unique()), pd.Series(unknown_val)], axis=1)

    # Rename the columns
    df1.columns = ["attribute", "unknown"]

    # Append the row to attributes_unknown_val
    df1 = df1.append({"attribute" : "ARBEIT", "unknown" : [-1, 9]}, ignore_index=True)
    
    print("Please wait: replacing unknown with NaN")
    for row in df1.itertuples(index=False):
        if row.attribute in df2.columns.values.tolist():
            nan_val = df1.loc[df1['attribute'] == row.attribute, 'unknown'].iloc[0]
            nan_idx = df2.loc[:, row.attribute].isin(nan_val)
            df2.loc[nan_idx, row.attribute] = np.NaN
        else:
            continue
            
    return df2

# Remove rows and features with high NaN count
def clean_data(df1, df2, df3, feat_list, drop_feat):
    """
    Method for cleaning up features and rows with high NaN count
    
    Args:
        df1 (Pandas Dataframe): azdias dataset
        df2 (Pandas Dataframe): customers dataset
        df3 (Pandas Dataframe): attributes dataset
        feat_list (list): List of features whose descriptions are available
        drop_feat (list): List of features that are needed to be drop
        
    Output:
        df1 (Pandas Dataframe): Cleaned azdias dataset
        df2 (Pandas Dataframe): Cleaned customers dataset
    """
    
    # Select the features whose information are available
    df1 = df1.loc[:, feat_list]
    df2 = df2.loc[:, feat_list]
    
    # Replace unknown values with NaN
    df1 = replace_nan(df3, df1)
    df2 = replace_nan(df3, df2)
    
    # Replace zeros in GEBURTSJAHR with NaN
    df1["GEBURTSJAHR"].replace(0, np.nan, inplace=True)
    df2["GEBURTSJAHR"].replace(0, np.nan, inplace=True)
    
    # NaN count for each feature
    feature_nan_count = pd.DataFrame({
                            "azdias_nan_count": [round(df1[x].isnull().sum()/df1[x].shape[0], 3) for x in df1.columns],
                            "customers_nan_count": [round(df2[x].isnull().sum()/df2[x].shape[0], 3) for x in df2.columns]
                        }, index=df1.columns)
    
    # Drop features where NaN count is higher than 20% in both df1 and df2
    feature_nan_count = feature_nan_count.loc[((feature_nan_count.azdias_nan_count <= 0.2) | 
                                               (feature_nan_count.customers_nan_count <= 0.2))]
    feature_nan_count = feature_nan_count.rename_axis("features").reset_index()
    
    # Select Features from feature_nan_count
    df1 = df1.loc[:, feature_nan_count.features.tolist()]
    df2 = df2.loc[:, feature_nan_count.features.tolist()]
    
    # Drop the features listed on drop_feat
    df1.drop(columns=drop_feat, inplace=True)
    df2.drop(columns=drop_feat, inplace=True)
    
    # Drop the rows in azdias
    count_nan_row = df1.shape[1] - df1.count(axis=1)
    drop_row = df1.index[count_nan_row > 50]
    df1.drop(drop_row, axis=0, inplace=True)

    # Drop the rows in customers
    count_nan_row = df2.shape[1] - df2.count(axis=1)
    drop_row = df2.index[count_nan_row > 50]
    df2.drop(drop_row, axis=0, inplace=True)
    
    return df1, df2

# Plot comparison of value distribution in two dataframe
def plot_comparison(column, df1, df2):
    """
    Method for plotting comparison of value distribution among two dataframes
    
    Args:
        column (series): Series from a feature
        df1 (Pandas Dataframe): azdias dataset
        df2 (Pandas Dataframe): customers dataset
        
    Output:
        None
    """
    
    print(column)
    sns.set(style="darkgrid")
    fig, (ax1, ax2) = plt.subplots(figsize=(12,4), ncols=2)
    sns.countplot(x = column, data=df1, ax=ax1, palette="Set3")
    ax1.set_xlabel('Value')
    ax1.set_title('Distribution of feature in AZDIAS dataset')
    sns.countplot(x = column, data=df2, ax=ax2, palette="Set3")
    ax2.set_xlabel('Value')
    ax2.set_title('Distribution of feature in CUSTOMERS dataset')
    fig.tight_layout()
    plt.show()
    
# Feature Engineering
def feat_eng(df1, df2):
    """
    Method for feature engineering & encoding & scaling the data
    
    Args:
        df1 (Pandas Dataframe): azdias dataset
        df2 (Pandas Dataframe): customers dataset
        
    Output:
        df1: Scaled azdias dataframe
        df2: Scaled customers dataframe
    """
    
    # OST_WEST_KZ needs to be encoded since the data are strings
    df1["OST_WEST_KZ"].replace(["W", "O"], [0, 1], inplace=True)
    df2["OST_WEST_KZ"].replace(["W", "O"], [0, 1], inplace=True)
    
    # Impute numeric columns
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    df1 = pd.DataFrame(imputer.fit_transform(df1), columns = df1.columns)
    df2 = pd.DataFrame(imputer.fit_transform(df2), columns = df2.columns)
    
    # Standardize the data
    scaler = StandardScaler()
    df1_scaled = scaler.fit_transform(df1)
    df2_scaled = scaler.transform(df2)
    
    # Create dataframe from scaled dataset
    df1 = pd.DataFrame(data=df1_scaled, index=df1.index, columns=df1.columns)
    df2 = pd.DataFrame(data=df2_scaled, index=df2.index, columns=df2.columns)
    
    return df1, df2