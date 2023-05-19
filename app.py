from flask import Flask
from flask import request,redirect, make_response,render_template,url_for
from model import db,ArticleModel
from flask_restful import Resource, Api

app = Flask(__name__, instance_path='/tmp/')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///articleHistory.sqlite3"
db.init_app(app)

with app.app_context():
    db.create_all()
    
api = Api(app)
app.app_context().push()

from controller import *

if __name__ == '__main__':
    app.run(debug=True,port=8000, host='0.0.0.0')
