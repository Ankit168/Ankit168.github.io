from flask import Flask
from flask import request, render_template, url_for, redirect, flash
from model import *
from app import app
from datetime import datetime
from webScrapper import *
from trainModel import *
from predictor import *

db.create_all()

@app.route("/",methods=["GET"])
def home(): 
    
    return render_template('home.html')

@app.route("/prediction", methods=["GET","POST"])
def prediction():

    cv, classifier = train_model()
    if request.method == "POST":
        url = request.form.get('url')
        scraped_text = web_scraper(url)
        print(scraped_text)
        predicted_category = predictor(cv, classifier, scraped_text)
        print("===================================")
        print(predicted_category)
        new_article = ArticleModel(url='url',category='predicted_category')
        try:
            print(new_article)
            db.session.add(new_article)
            db.session.commit()
            return render_template("home.html")
        except:
            raise
        
    return render_template('prediction.html')