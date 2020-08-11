# Import packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly, json
import plotly.graph_objects as go

# Clean dataset
def clean_data():
    """
    Method for cleaning the data and removing unnecessary features

    Args:
        None

    Returns:
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

    Returns:
        data (list): Return list of (x, y) value for plotting
    """

    # Groupby district name and sum the number of audiences
    df = df.groupby(["districtName"], as_index = False)["count_id"].agg("sum")

    # Sort values in descending order
    df.sort_values(by = ["count_id"], ascending = False, inplace = True)

    # Slice the rows to select top n rows
    df = df[:rank_filter]
    
    #return data
    return df

def create_plot():
    """
    Method for creating Plotly charts

    Args:
        None
    
    Returns:
        list (dict): list containing the four plotly visualizations
    """

    # Clean dataset
    df = clean_data()

    # Find districts with highest number of audiences
    df = top_district(df, 5)

    # Create column chart for districts with highest audiences
    graph_one = []
    graph_one.append(
        go.Bar(
            x = df.districtName.tolist(),
            y = df.count_id.tolist()
        )
    )

    layout_one = dict(title = "Top 5 Districts",
        xaxis = dict(title = "District Names"),
        yaxis = dict(title = "Number of Audiences")
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data = graph_one, layout = layout_one))

    return figures

    """
    fig = px.bar(df, x = "districtName", y = "count_id",
            title = "Top 5 Districts with Highest Number of Audiences",
            hover_data = ["count_id"],
            labels={"count_id" : "Number of Audiences",
                    "districtName" : "District Name"})

    # Convert the plotly figures to JSON for javascript in HTML template
    figuresJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    """