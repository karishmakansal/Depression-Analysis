from flask import Flask,render_template,request
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import json
app = Flask(__name__)
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       inputss = request.form.get("inp")
       outputs = datreeINPUT(inputss)
       return outputs
    return render_template("text.html")

vectorizer = CountVectorizer(stop_words='english')
x = []
y = []
tweets_data = []

def retrieveTweet(data_url):
    tweets_data_path = data_url
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
def retrieveProcessedData(Pdata_url):
    sent = pd.read_excel(Pdata_url)
    for i in range(len(tweets_data)):
        if tweets_data[i]['id'] == sent['id'][i]:
            x.append(tweets_data[i]['text'])
            y.append(sent['sentiment'][i])

retrieveTweet('dep_tweet.txt')
retrieveProcessedData('dep_output.xls')
def datreeINPUT(inputtweet):
    from sklearn import tree
    train_featurestree = vectorizer.fit_transform(x)
    dtree = tree.DecisionTreeClassifier()

    dtree = dtree.fit(train_featurestree, [int(r) for r in y])

    inputdtree = vectorizer.transform([inputtweet])
    predictt = dtree.predict(inputdtree)

    if predictt == 1:
        return("Positive: Means that you are unlikely to have depression or anxiety")
    elif predictt == 0:
        return("Neutral: Means You may suffer from depression or may be not but may also be more prone to being depress")
    elif predictt == -1:
        return ("Negative: It is the lowest level where depression and anxiety being detected through user tweets")
    else:
        return("Nothing")

if __name__=="__main__":
    app.run(debug=True)

