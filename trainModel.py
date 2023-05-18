import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB

# This is to preprocess the scraped text for better prediction.
def preprocessing(data):
    data['Text'] = data['Text'].apply(remove_tags)
    data['Text'] = data['Text'].apply(special_char)
    data['Text'] = data['Text'].apply(convert_lower)
    data['Text'] = data['Text'].apply(remove_stopwords)
    data['Text'] = data['Text'].apply(lemmatize_word)
    return data

def remove_tags(text):
    remove = re.compile(r'')
    return re.sub(remove, '', text)

def special_char(text):
    reviews = ''
    for x in text:
        if x.isalnum():
            reviews = reviews + x
        else:
            reviews = reviews + ' '
    return reviews

def convert_lower(text):
    return text.lower()

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return [x for x in words if x not in stop_words]


def lemmatize_word(text):
    wordnet = WordNetLemmatizer()
    return " ".join([wordnet.lemmatize(word) for word in text])

def train_model():
    
    # We have used this as training data to train our model from Kaggle
    data = pd.read_csv('./BBC News Train.csv')
    #print(data.head())

    target_category = data['Category'].unique()
    #print(target_category)

    data['CategoryId'] = data['Category'].factorize()[0]
    #print(data.head())

    category = data[['Category', 'CategoryId']].drop_duplicates().sort_values('CategoryId')
    #print(category)

    data = preprocessing(data)    

    x = data['Text']
    y = data['CategoryId']

    x = np.array(data.iloc[:,0].values)
    y = np.array(data.CategoryId.values)
    cv = CountVectorizer(max_features = 5000)
    x = cv.fit_transform(data.Text).toarray()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0, shuffle = True)

    # After running on multiple models(in Google Collab) and comparing their F1-values, 
    # RandomForestClassifier turns out to be the best, so it is being used here.
    model_random_forest = RandomForestClassifier(n_estimators=100 ,criterion='entropy' , random_state=0)

    oneVsRest = OneVsRestClassifier(model_random_forest)

    oneVsRest.fit(x_train, y_train)

    classifier = RandomForestClassifier(n_estimators=100 ,criterion='entropy' , random_state=0).fit(x_train, y_train)
    
    return cv,classifier