from flask import Flask, request ,render_template,flash
import subprocess
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
#from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import string

app=Flask(__name__)
app.secret_key = "your_secret_key_here"

vectorizer, model = joblib.load("vectorizer_model.joblib")




import re
import string

def wordopt(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters enclosed in square brackets
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove non-alphanumeric characters
    text = re.sub(r'\W', ' ', text)
    
    # Remove hyperlinks starting with "http://" or "https://" or "www."
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation marks
    text = re.sub(r'[{}]'.format(re.escape(string.punctuation)), '', text)
    
    # Remove newline characters
    text = re.sub(r'\n', '', text)
    
    # Remove words containing digits
    text = re.sub(r'\w*\d\w*', '', text)
    
    return text



def output_label(n):
    if n == 'CG' :
        return "Fake"
        #return "Computer generated"

    elif n == 'OR' :
        return "Genuine"
        #return "Original review"

    

def testing(review, vectorizer, model):
    testing_review = {"text": [review]}
    new_test = pd.DataFrame(testing_review)
    new_test["text"] = new_test["text"].apply(wordopt)
    new_x_test = new_test["text"]
    new_xv_test = vectorizer.transform(new_x_test)
    pred_SVM = model.predict(new_xv_test)
    out = output_label(pred_SVM)
    return out  


@app.route("/")
def home():
    flash("stranger things")
    return render_template("index.html")







@app.route('/websearch',methods=['POST'])
def display_dataframe():
    cust_names = []
    review_title = []
    review_content = []
    buyer_details=[]

    url =request.form['url_input']
    url=url+str("&page=1")

    page=requests.get(url)
    soup=bs(page.content,'html.parser')


    img_tag=soup.find('img',class_='_396cs4')

    if img_tag:
        src_url=img_tag['src']
        print(src_url)
        anchor_tag=soup.find('a','s1Q9rs _2qfgz2')
        teext=anchor_tag.get_text();
        
    else:
        img_tag=soup.find('img',class_='_2r_T1I')
        src_url=img_tag['src']
        #print("image not found")

    for x in range(1, 10):
        conc_str = str(x)
        url = url[:-1] + conc_str

        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        names = soup.find_all('p', class_='_2sc7ZR _2V5EHH')
        for i in range(0, len(names)):
            cust_names.append(names[i].get_text())

        title = soup.find_all('p', class_='_2-N8zT')
        for i in range(0, len(title)):
            review_title.append(title[i].get_text())

        review = soup.find_all("div", class_="t-ZTKy")
        for i in range(0, len(review)):
            review_content.append(review[i].get_text())


        date=soup.find_all("p",class_="_2mcZGG")
        for i in range(0,len(date)):
            buyer_details.append(date[i].get_text())

    df = pd.DataFrame()
    df['cust_names'] = cust_names
    df['review_title'] = review_title
    df['review_content'] = review_content
    df['buyer_details']=buyer_details

    df['prediction'] = None
    for index, row in df.iterrows():
        text = row['review_content']  # Access the 'review_content' value for the current row

        processed_text = testing(text,vectorizer, model)

        df.at[index, 'prediction'] = processed_text
        
        #df['review_content']


    df.index+=1;


    return render_template('index2.html',dynamic_image_url=src_url,product_title=teext,dataframe=df.to_html())    




  


