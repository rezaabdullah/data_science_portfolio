from dashboard import app
from flask import render_template
from data_preprocessing.data_wrangling import clean_data, top_district
import pandas as pd

# Clean dataset
clean_df = clean_data()

# Filter out top 5 districts that has the highest number of audience
topdistrict = top_district(clean_df, 5)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/dashboard-portfolio")
def dashboard_portfolio():
    return render_template(dashboard_portfolio.html)