from dashboard import app
from flask import render_template
from data_preprocessing.data_wrangling import create_plot
import pandas as pd

import plotly.graph_objs as go
import plotly.express as px
import plotly, json

@app.route("/")
@app.route("/index")
def index():
    # Create chart
    figures = create_plot()

    # plot ids for the html id tag
    ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls = plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", ids = ids, figuresJSON = figuresJSON)