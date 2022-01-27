from flask import Flask, render_template, redirect, url_for
from matplotlib.figure import Figure
from flask_bootstrap import Bootstrap

app = Flask(__name__)  
Bootstrap(app)

from flask import request

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template(
            'template_home_test.html',
            data=[{'name':'bitcoin'}, {'name':'ethereum'}, {'name':'solana'}])
    elif request.method == 'POST':
        data = request.form.get("comp_select")
        return redirect(url_for('graphCrypto', crypto=data))

    
@app.route("/predict" , methods=['GET', 'POST'])
def predict():
    return render_template(
        'template_predict_test.html',
        data=[{'name':'bitcoin'}, {'name':'ethereum'}])


@app.route("/graph/<crypto>", methods=['GET', 'POST'])
def graphCrypto(crypto):
    return crypto


if __name__ == '__main__':
    app.run(debug=True, port=2745)