import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# table schema
class ArticleModel(db.Model):
#    __tablename__ = 'articlemodel'
    articleId = db.Column(db.Integer, primary_key=True,autoincrement=True)
    url = db.Column(db.String(255),nullable=False)
    category = db.Column(db.String(64),nullable=True)
    createdAt = db.Column(db.DateTime,nullable=False,default=datetime.now())
    
