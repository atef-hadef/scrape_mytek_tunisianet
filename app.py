from flask import Flask, render_template, request, jsonify
from mytek import scrapper_mytek_filtré
from tunisianet import scrapper_tunisianet
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produits')
def produits():

    marque = request.args.get('marque')
    prix_min = request.args.get('prix_min')
    prix_max = request.args.get('prix_max')
    processeur = request.args.get('processeur')


    if not any([marque, prix_min, prix_max, processeur]):
        return jsonify([])


    prix_min = float(prix_min) if prix_min else None
    prix_max = float(prix_max) if prix_max else None

    df_mytek = scrapper_mytek_filtré(marque, prix_min, prix_max, processeur)
    df_tunisianet = scrapper_tunisianet(marque, prix_min, prix_max,processeur)

    df_total = pd.concat([df_mytek, df_tunisianet], ignore_index=True)

    if df_total.empty:
        return jsonify([]) 
    
    produits = df_total.to_dict(orient='records')
    return jsonify(produits)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
