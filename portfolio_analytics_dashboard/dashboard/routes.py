from dashboard import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/dashboard-portfolio")
def dashboard_portfolio():
    return render_template(dashboard_portfolio.html)