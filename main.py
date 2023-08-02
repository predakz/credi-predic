# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 22:46:47 2023

@author: Paul
"""

from flask import Flask, jsonify, request
import pandas as pd
import dill as pickle


app = Flask(__name__)

def check_data(data):
    if len(data)==251845:
        print('Données chargées avec succès')
        return 1
    else:
        print("Problème dans les données")
        return 0

# Function returning a prediction based on a customer ID
@app.route('/predict', methods=['GET'])
def predict():
    # Reading the customer ID in the request
    username = int(request.args.get('customer'))
    # Probability threshold over whch a customer is considered as a good one
    threshold = 0.5757575757575758
    # Importing data
    data = pd.read_csv('cleaned_data.csv', index_col=0)
    check = check_data(data)
    list_features = pickle.load(open('Pickles/features.pkl', 'rb')) # Features used
    model = pickle.load(open('Pickles/randfor.pkl', 'rb')) # Trained model (Random Forests)
    transformers = pickle.load(open('Pickles/transformers.pkl', 'rb')) # Transformations to apply on data
    list_transformers = [i for i in transformers]  # as a list (1 element = 1 feature)
    explainer = pickle.load(open('Pickles/explainer.pkl', 'rb')) #load lime explainer
    distributions = pickle.load(open('Pickles/distributions.pkl', 'rb')) # Distributions in different features for the explainer
    print('Verification ID: '+str(username))
    if username not in data.index:
        # Raise an error if the ID is unknown
        return {
            'Statut': 'Erreur',
            'Message': 'Erreur: ID inconnu'
        }
    elif check == 0:
        return {
            'Statut': 'Erreur',
            'Message': 'Problème dans les données'
        }
    else:
        # Loading data for the customer whose ID has been entered
        data_user = pd.DataFrame(data.loc[[username]])
        data_user = data_user.drop('TARGET', axis=1)
        # Applying the right transformations on data
        for i in list_transformers:
            data_user[i] = transformers[i].transform(data_user[i])
        # Calculating the customer's score and generating the prediction according to this score
        proba = model.predict_proba(data_user.values.reshape(1,-1))[0][1]
        prediction = 1 if proba > threshold else 0
        score = round(float(proba), 3)
        # Generating the explainer in terms of 6 key features
        expl_details = explainer.explain_instance(
            data_user.values.reshape(-1),
            model.predict_proba,
            num_features=6
        )
        expl_details_map, expl_details_list = pd.DataFrame(expl_details.as_map()[1], columns=['Feature_idx', 'Scaled_value']), expl_details.as_list()
        names_main_features = []
        for i in expl_details_map['Feature_idx']:
            names_main_features.append(list_features['all_features'][i])
        # Getting the distributions for these features in order to plot them, giving visual interpretation
        feat_to_plot = [i for i in distributions if i in names_main_features]
        distributions_to_plot = {}
        for i in feat_to_plot:
            distributions_to_plot[i] = distributions[i]
        return jsonify({
                'Statut': 'Succès',
                'Prédiction': int(prediction),
                'Score': score,
                'Seuil': round(threshold, 3),
                'Infos utilisateur': data_user.to_dict(),
                'Explainer map': expl_details_map.to_dict('list'),
                'Explainer list': expl_details_list,
                'Distributions': distributions_to_plot
            })


if __name__ == '__main__':
    app.run(debug=True,port=5000)