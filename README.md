# credi-predic

Project: deploy an online scoring app in order to predict a client's ability to repay a loan and decide if the loaan can be granted.

Data: https://www.kaggle.com/c/home-credit-default-risk/data

In this folder:
-> main.py is the Python script deploying the API using flask, unit tests are implemented using Pytest in test_main.py
-> Pickles contain Python objects including the model (called "randfor.pkl") and tools for data preprocessing or generating visual explanations for the results
-> cleaned_data.csv contains pre-processed data that are used here
-> Procfile is used for initializing the app on the cloud
-> requirements.txt contains a list of the essential packages to run the app
-> runtime.txt specifies the version of Python used here
