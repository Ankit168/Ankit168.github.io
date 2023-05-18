from flask import Flask
from flask import request, render_template, url_for, redirect, flash
from model import *
from app import app
from datetime import datetime
from webScrapper import *
from trainModel import *
from predictor import *

db.create_all()

# route for home page 
@app.route("/",methods=["GET"])
def home(): 
    
    return render_template('home.html')

# route for prediction page
@app.route("/prediction", methods=["GET","POST"])
def prediction():

    if request.method == "POST":
        input_url = request.form.get('url') 
        if input_url is not None:
            cv, classifier = train_model()  # model is trained   
            scraped_text = web_scraper(input_url) # scraped text is returned
            predicted_category = predictor(cv, classifier, scraped_text)  # model will predict the category
            new_article = ArticleModel(url=input_url, category=predicted_category)
            try:
                all_predictions = db.session.query(ArticleModel).all()
                db.session.add(new_article)
                db.session.commit()
                return render_template("history.html", category=predicted_category, all_predictions=all_predictions)
            except:
                raise
        
    return render_template('prediction.html')