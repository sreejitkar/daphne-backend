import pickle
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

with open('covid_response/static/fixtures/intent.json') as f:
    doc7 = f.read()
    inte = json.loads(doc7)
    list_of_intents = inte["intents"]
df = pd.read_csv("data.csv")
x = df["Questions"]
y = df["tag"]
text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', SGDClassifier(loss='modified_huber'))])
text_clf.fit(x, y)

file = open("covid_response/static/fixtures/model_output.pkl", "wb")
pickle.dump(text_clf, file)
file.close()
