import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import re
import string
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("fake reviews dataset.csv")

df = df.sample(frac = 1)
df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)

# Creating a function to convert the text in lowercase, remove the extra space, special chr., ulr and links.



def wordopt(text):
  text = text.lower()
  text = re.sub('\[.*?\]', '', text) #Removing special character
  text = re.sub("\\W"," ",text) #Removes non-alphanumeric
  text = re.sub('https?://\S+|www\.\S+', '', text) #Removing Hyperlinks
  text = re.sub('<.*?>+', '', text)
  text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #removing punctuation
  text = re.sub('\n', '', text) #Removing the next line
  text = re.sub('\w*\d\w*', '', text)
  return text



df["text_"] = df["text_"].apply(wordopt)



import pandas as pd
def convert_to_binary(value):
    if 'OR' in value:
        return 1
    elif 'CG' in value:
        return 0
    else:
        return None
    

df['label'] = df['label'].apply(convert_to_binary)


x = df["text_"]
y = df["label"]
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.25)


from sklearn.feature_extraction.text import TfidfVectorizer
vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)



from sklearn.svm import SVC
SVM = SVC(random_state=0)
SVM.fit(xv_train, y_train)
pred_svm = SVM.predict(xv_test)



def output_label(n):
 	if n == 0 :
        		return "Computer generated"
 	elif n == 1 :
        		return "Orginial review"



accuracy=accuracy_score(y_test, pred_svm)*100
precision = precision_score(y_test, pred_svm, average='weighted')*100
recall = recall_score(y_test, pred_svm, average='weighted')*100
f1 = f1_score(y_test, pred_svm, average='weighted')*100



print(accuracy)
print(precision)
print(recall)
print(f1)

# filename="svm_model.pkl"
# joblib.dump(SVM,filename)

# vector="vectorizer.pkl"
# joblib.dump(vectorization,vector)



joblib.dump((vectorization, SVM), "vectorizer_model.joblib")
print("HEllo WORLD")
