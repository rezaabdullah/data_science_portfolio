# Import packages
import pandas as pd
import numpy as np
#import plotly.express as px
#import matplotlib.pyplot as plt
#import seaborn as sns
#%matplotlib inline

# Clean dataset
def clean_data():
    """
    Method for cleaning the data and removing unnecessary features

    Args:
        None

    Attributes:
        df (pandas dataframe): Return pandas dataframe
    """
    df = pd.read_csv("dashboard/asset/data/kl_billboard.csv")

    # Drop different types of roads such as motorway, trunk etc.
    df.drop(columns = ["motorway", "trunk", "primary", "secondary", "tertiary"], inplace = True)

    # Drop NaN
    df.dropna(axis = "columns", inplace = True)
    
    return df

# Find the districts with highest audiences
def top_district(df, rank_filter):
    """
    Method for finding the total number of audience in the district

    Args:
        df (pandas dataframe): Dataframe from clean_data
        rank_filter (int): Number of top districts to display

    Attributes:
        data (list): Return list of (x, y) value for plotting
    """

    # Groupby district name and sum the number of audiences
    df = df.groupby(["districtName"], as_index = False)["count_id"].agg("sum")

    # Sort values in descending order
    df.sort_values(by = ["count_id"], ascending = False, inplace = True)

    # Slice the rows to select top n rows
    df = df[:rank_filter]

    # Prepare data into x, y lists for plotting
    data = list()
    x = df.districtName.tolist()
    y = df.count_id.tolist()
    data.append((x, y))
    print (x, y)
    
    return data

# Main function
def main():
    # File path for CSV
    #filepath = "../dashboard/asset/data/kl_billboard.csv"

    # Clean dataset
    df = clean_data()

    # Rank districts based on number of audiences
    topdistrict = top_district(df, 3)

    print(top_district)

if __name__ == "__main__":
    main()

"""
# Find the total number of mobile devices around the billboard
df_total_audience = df.groupby(["billboard_object_id", "districtName", "latitude", "longitude"], as_index = False) \
                        [["count_id"]].sum()
df_total_audience.sort_values(by = ["count_id"], ascending = False, inplace = True)

# Determine percentage rank
df_total_audience["pcnt_rank"] = df_total_audience["count_id"].rank(method = "max", pct=True)

# Determine the shape of the dataframe where total number of rows corresponds to total number of billboards
print(df_total_audience.shape)

# Plot a histogram with 10 bins to find the distribution of audiences around the billboard
hist = df_total_audience[["billboard_object_id", "count_id"]].hist(bins=10)

# Divide billboards into 10 bins based on percentage rank
conditions = [
    (df_total_audience['pcnt_rank'] >= 0.9),
    (df_total_audience['pcnt_rank'] >= 0.8) & (df_total_audience['pcnt_rank'] < 0.9),
    (df_total_audience['pcnt_rank'] >= 0.7) & (df_total_audience['pcnt_rank'] < 0.8),
    (df_total_audience['pcnt_rank'] >= 0.6) & (df_total_audience['pcnt_rank'] < 0.7),
    (df_total_audience['pcnt_rank'] >= 0.5) & (df_total_audience['pcnt_rank'] < 0.6),
    (df_total_audience['pcnt_rank'] >= 0.4) & (df_total_audience['pcnt_rank'] < 0.5),
    (df_total_audience['pcnt_rank'] >= 0.3) & (df_total_audience['pcnt_rank'] < 0.4),
    (df_total_audience['pcnt_rank'] >= 0.2) & (df_total_audience['pcnt_rank'] < 0.3),
    (df_total_audience['pcnt_rank'] >= 0.1) & (df_total_audience['pcnt_rank'] < 0.2),
    (df_total_audience['pcnt_rank'] >= 0.0) & (df_total_audience['pcnt_rank'] < 0.1)
    ]

# create a list of the values we want to assign for each condition
values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# create a new column and use np.select to assign values to it using our lists as arguments
df_total_audience['tier'] = np.select(conditions, values)

print(df.head())

# Group by the number of audiences based on hour and number of POIs
df_poi_hour = df.groupby(["count_poi", "hour", "total_num_road"])[["count_id"]].sum()
df_poi_hour.reset_index(inplace = True)

# Determine correlation matrix
sns.heatmap(df_poi_hour.corr(), annot=True, fmt = "0.2f")
plt.show()

# The function returns the list of potential district names
def select_district(df, threshold_tier):
"""
"""
Returns lists of potential district names for building new billboards

Extended description of the function

Parameters:
df: Pandas dataframe
threshold_tier: Threshold value for selecting the tier

Returns:
district_list: List of district names
"""
"""
# Count the number of billboards for each tier in a district
df_area = df.groupby(["districtName", "tier"], as_index = False)[["billboard_object_id"]].count()

# Choose districts with threshold tier value and assign the selected district names to a list and return the list
district_list = df_area[df_area.tier >= threshold_val].districtName.unique()
return district_list

# Select areas with threshold tier of 9
area_list = select_district(df_total_audience, 9)
print(area_list)
"""