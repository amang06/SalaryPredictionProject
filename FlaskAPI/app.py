import flask
from flask import Flask, jsonify, request
import json
import pickle
from data_in import data_in
import numpy as np


def load_model():
    file_name = "models/model_file.pkl"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model


app = Flask(__name__)


@app.route('/predict', methods=['GET'])
def predict():
    # stub input features
    request_json = request.get_json()
    x = request_json['input']
    x_in = np.array(x).reshape(1, -1)
    # load model
    model = load_model()
    prediction = model.predict(x_in)[0]
    response = json.dumps({'response': prediction})
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)
