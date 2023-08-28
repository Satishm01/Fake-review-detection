import requests
from bs4 import BeautifulSoup as bs
import validators

cust_names=[]
review_title=[]
review_content=[]
review_rating=[]
buyer_details=[]
img_url='url'
url=input("Enter the url")
url=url+str("&page=1")

page=requests.get(url)
soup=bs(page.content,'html.parser')

img_tag=soup.find('img',class_='_396cs4')

if img_tag:
    src_url=img_tag['src']
    print(src_url)
else:
    print("image not found")



for x in range(1,10):
    conc_str=str(x)
    url=url[:-1]+conc_str

    page=requests.get(url)
    soup=bs(page.content,'html.parser')



    names=soup.find_all('p',class_='_2sc7ZR _2V5EHH')


    for i in range(0,len(names)):
        cust_names.append(names[i].get_text())


    title=soup.find_all('p',class_='_2-N8zT')
    for i in range(0,len(title)):
        review_title.append(title[i].get_text())
    



    review=soup.find_all("div",class_="t-ZTKy")
    for i in range(0,len(review)):
        review_content.append(review[i].get_text())


    date=soup.find_all("p",class_="_2mcZGG")
    for i in range(0,len(date)):
        buyer_details.append(date[i].get_text())

    # rating=soup.find_all("div",class_="_3LWZlK _1BLPMq")
    # for i in range(0,len(rating)):
    #     review_rating.append(rating[i].get_text())


import pandas as pd
df=pd.DataFrame()
df['cust_names']=cust_names
df['review_title']=review_title
df['review_content']=review_content
df['buyer_details']=buyer_details

df.index+=1;

df
print(df)