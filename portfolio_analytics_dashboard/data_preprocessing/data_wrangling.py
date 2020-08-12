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

# Find distribution of audiences around each billboard
def billboard_sort(df):
    """
    Method to bin the billboards based on the number of audiences

    Args:
        df (pandas dataframe): Dataframe from clean_data()

    Returns:
        billboard_df (pandas dataframe): Billboards sorted by highest audiences
    """

    # Groupby billboards, latitude, longitude
    df = df.groupby(["billboard_object_id", "latitude", "longitude"], as_index = False)[["count_id"]].sum()
    
    # Sort values based on number of audiences
    df.sort_values(by = ["count_id"], ascending = False, inplace = True)

    # Determine percentage rank
    df["pcnt_rank"] = df["count_id"].rank(method = "max", pct=True)

    # Divide billboards into 10 bins based on percentage rank
    conditions = [
        (df['pcnt_rank'] >= 0.9),
        (df['pcnt_rank'] >= 0.8) & (df['pcnt_rank'] < 0.9),
        (df['pcnt_rank'] >= 0.7) & (df['pcnt_rank'] < 0.8),
        (df['pcnt_rank'] >= 0.6) & (df['pcnt_rank'] < 0.7),
        (df['pcnt_rank'] >= 0.5) & (df['pcnt_rank'] < 0.6),
        (df['pcnt_rank'] >= 0.4) & (df['pcnt_rank'] < 0.5),
        (df['pcnt_rank'] >= 0.3) & (df['pcnt_rank'] < 0.4),
        (df['pcnt_rank'] >= 0.2) & (df['pcnt_rank'] < 0.3),
        (df['pcnt_rank'] >= 0.1) & (df['pcnt_rank'] < 0.2),
        (df['pcnt_rank'] >= 0.0) & (df['pcnt_rank'] < 0.1)
        ]

    # create a list of the values we want to assign for each condition
    values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    # create a new column and use np.select to assign values to it using our lists as arguments
    df['tier'] = np.select(conditions, values)

    df.drop(columns = ["pcnt_rank"], inplace = True)

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

    # Aggregate number of audiences for each districts
    districtDf = df.groupby(["districtName"], as_index = False)["count_id"].agg("sum")

    # Load Geojson file for KL Map
    with open("dashboard/asset/data/kl_map.geojson") as file:
        geojsonKL = json.load(file)

    # Get mapbox access token
    mapbox_access_token = open("dashboard/asset/token/.mapbox_token").read()

    # Create Choropleth Map for districts
    graph_one = []
    graph_one.append(
        go.Choroplethmapbox(
            geojson = geojsonKL,
            locations = districtDf.districtName,
            z = districtDf.count_id,
            featureidkey = "properties.NAMA_DM",
            colorscale = "viridis"
        )
    )

    layout_one = dict(margin = {"r":0,"t":0,"l":0,"b":0},
        mapbox = dict(
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = dict(
                lat = 3.148274,
                lon = 101.680077
            ),
            pitch = 0,
            zoom = 10,
            style = "carto-positron"
        )
    )

    # Find districts with highest number of audiences
    topdistrict = top_district(df, 5)

    # Create column chart for districts with highest audiences
    graph_two = []
    graph_two.append(
        go.Bar(
            x = topdistrict.districtName.tolist(),
            y = topdistrict.count_id.tolist()
        )
    )

    layout_two = dict(title = "Top 5 Districts",
        xaxis = dict(title = "District Names"),
        yaxis = dict(title = "Number of Audiences")
    )

    # Find top billboards and assign tiers
    billboard_df = billboard_sort(df)

    # Create scatter plot map
    graph_three = []
    graph_three.append(
        go.Scattermapbox(
            lat = billboard_df.latitude,
            lon = billboard_df.longitude,
            mode = "markers",
            marker = go.scattermapbox.Marker(
                size = billboard_df.tier,
                color = billboard_df.count_id,
                colorscale = "viridis",
                showscale = True
            ),
            text = billboard_df.count_id,
            hoverinfo = "text"
        )
    )

    layout_three = dict(margin = {"r":0,"t":0,"l":0,"b":0},
            mapbox = dict(
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = dict(
                lat = 3.148274,
                lon = 101.680077
            ),
            pitch = 0,
            zoom = 10,
            style = "carto-positron"
        )
    )

    # Show top 10 billboards
    billboard_df_rank = billboard_df[:10]

    # Create column chart for districts with highest audiences
    graph_four = []
    graph_four.append(
        go.Bar(
            x = billboard_df_rank.billboard_object_id.tolist(),
            y = billboard_df_rank.count_id.tolist()
        )
    )

    layout_four = dict(title = "Top 10 Billboards",
        xaxis = dict(title = "Billboard Name"),
        yaxis = dict(title = "Number of Audiences")
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data = graph_two, layout = layout_two))
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures