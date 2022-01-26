import flask
from pymongo import MongoClient
import time
from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px

app = flask.Flask(__name__,template_folder='./templates')

@app.route("/")
def home():

    df = pd.DataFrame(list(db["ethereum"].find()))
    fig = px.line(df, x='date', y='open', markers=True)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('template.html', graphJSON=graphJSON,data=db.list_collection_names())


if __name__ == '__main__':
    #time.sleep(1)

    # Coonect to MONGODB
    client = MongoClient("0.0.0.0:27017")

    # Create our database
    db = client["coingecko"]

    app.run(host='0.0.0.0', port=5001, debug=True)
