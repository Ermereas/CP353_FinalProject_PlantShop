from flask import Flask, request, jsonify,json,render_template
from flask_restx import Api, Resource, fields
from flask_basicauth import BasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from connexion.resolver import RestyResolver
import connexion
from flask import Flask
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask,render_template,request,redirect,Blueprint
from urllib.parse import quote
from urllib.request import urlopen
import json
import requests
import urllib.parse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from api.routes import create_route
from flask_cors import CORS
import os
from flask import Flask, request, render_template, jsonify
from PIL import Image
import base64
# from check import check
from ml_model import TFModel


app = Flask(__name__)
# app.register_blueprint(check)

CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"
], supports_credentials=True)

api = Api(app)
create_route(api=api)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Flask RESTful API"
    }
)

app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.config['BASIC_AUTH_USERNAME'] = 'Admin'
app.config['BASIC_AUTH_PASSWORD'] = 'Admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basic_auth = BasicAuth(app)

@app.route("/")
def home():
    data = json.load(open('plant.json'))
    return render_template('home.html',data=data)


UPLOAD_FOLDER = './static/pic'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model=TFModel(model_dir='./static/ml-model/')
model.load()

@app.route('/check', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        image_1 = Image.open(path)
        outputs = model.predict(image_1)

        return render_template('predict.html', pred_result=outputs)

    return render_template('update.html')


if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True,use_reloader=True)

app.run(debug=True,use_reloader=True)

