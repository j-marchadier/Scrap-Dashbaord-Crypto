from pymongo import MongoClient
import time
import pandas as pd
import json
import plotly
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, template_folder='./templates')


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # On recupere les donners dans notre mongoDB
        df = pd.DataFrame(list(db["ethereum"].find()))[["date", "marketcap", "volume", "open"]]

        # Graphine line of Ethereum value
        fig = px.line(df, x='date', y='open', markers=True)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        etherValue = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Graphine line of Ethereum MarketCap
        fig = px.line(df, x='date', y='marketcap', markers=True)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        etherMK = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Graphine line of Ethereum volume
        fig = px.line(df, x='date', y='marketcap', markers=True)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        etherVolume = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('template_home_test.html', graphJSON=etherValue, graphJSON2=etherMK,
                               graphJSON3=etherVolume, data=db.list_collection_names())

    elif request.method == 'POST':
        data = request.form.get("comp_select")
        return redirect(url_for('graphCrypto', crypto=data))


@app.route("/predict")
def predict():
    graphJSON = IA()
    return render_template('template_predict_test.html', graphJSON=graphJSON, data=db.list_collection_names())


@app.route("/graph/<crypto>", methods=['GET', 'POST'])
def graphCrypto(crypto):
    df = pd.DataFrame(list(db[str(crypto)].find()))[["date", "marketcap", "volume", "open"]]
    fig = px.line(df, x='date', y='open', markers=True)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('template_home_test.html', graphJSON=graphJSON, data=db.list_collection_names())


def IA():
    df = pd.DataFrame(list(db["ethereum"].find()))[["date", "marketcap", "volume", "open"]]
    df = df.iloc[::-1].reset_index()
    df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')

    # Define a size for the train/test sets
    train_size = int(0.8 * len(df))
    train_set = df[:train_size]
    test_set = df[train_size:]

    y_train = train_set['open']
    y_test = test_set['open']

    df["train"] = y_train
    df["test"] = y_test
    # 1er model
    ARMAmodel = SARIMAX(y_train, order=(7, 2, 6))
    ARMAmodel = ARMAmodel.fit(disp=0)

    y_pred_sarimax = ARMAmodel.get_forecast(len(test_set))
    y_pred_df_sarimax = y_pred_sarimax.conf_int(alpha=0.05)
    y_pred_df_sarimax["Predictions"] = ARMAmodel.predict(start=y_pred_df_sarimax.index[0],
                                                         end=y_pred_df_sarimax.index[-1])
    y_pred_df_sarimax.index = test_set["date"]
    y_pred_out_sarimax = y_pred_df_sarimax["Predictions"]
    y_pred_out_sarimax.index = range(train_size, len(df))
    df["sarimax"] = y_pred_out_sarimax

    # 2ème model
    ARIMAmodel = ARIMA(y_train, order=(3, 1, 4))
    ARIMAmodel = ARIMAmodel.fit()

    y_pred_arima = ARIMAmodel.get_forecast(len(test_set["date"]))
    y_pred_df_arima = y_pred_arima.conf_int(alpha=0.05)
    y_pred_df_arima["Predictions"] = ARIMAmodel.predict(start=y_pred_df_arima.index[0], end=y_pred_df_arima.index[-1])
    y_pred_df_arima.index = test_set["date"]
    y_pred_out_arima = y_pred_df_arima["Predictions"]
    y_pred_out_arima.index = range(train_size, len(df))
    df["arima"] = y_pred_out_arima

    fig = px.line(df, x='date', y=["train", "test", "sarimax", "arima"])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == '__main__':
    time.sleep(1)

    # Coonect to MONGODB
    # client = MongoClient("mongo",27017)  #Pour le Docker compose
    client = MongoClient("0.0.0.0", 27017)

    # Create our database
    db = client["coingecko"]

    app.run(host='0.0.0.0', port=5001, use_reloader=False)
