( First Part of the code ) ( Use Jupyter Notebook )
import numpy as np
import pandas as pd
import wordcloud

data = pd.read_csv('spamdata.csv',encoding = 'latin-1')
data.shape
data.head()

#Dropping the unused columns
data = data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis = 1)

# rename the columns

data = data.rename(columns = {'v1': 'Type', 'v2': 'Messages'})

data.columns

#Print Spam messages in messages

df = pd.DataFrame(data) 
Spamfilter = df.loc[df['Type'] == 'spam']
print (Spamfilter)

#Print ham messages in Messages

df = pd.DataFrame(data) 
hamfilter = df.loc[df['Type'] == 'ham']
print (hamfilter)

#Print the most common number of words used in all Messages

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(background_color = 'White', width = 1000, height = 1000, max_words = 50).generate(str(data['Messages']))

plt.rcParams['figure.figsize'] = (10, 10)
plt.title('Most Common words in the dataset', fontsize = 20)
plt.axis('off')
plt.imshow(wordcloud)

#Print the most number of words used in spam messages

from wordcloud import WordCloud

wordcloud = WordCloud(background_color = 'white', width = 1000, height = 1000, max_words = 50).generate(str([Spamfilter]))

plt.rcParams['figure.figsize'] = (10, 10)
plt.title('Most Common words in spam', fontsize = 20)
plt.axis('off')
plt.imshow(wordcloud)

#Print most number of words used in ham messages


from wordcloud import WordCloud

wordcloud = WordCloud(background_color = 'white', width = 1000, height = 1000, max_words = 50).generate(str([hamfilter]))

plt.rcParams['figure.figsize'] = (10, 10)
plt.title('Most Common words in ham', fontsize = 20)
plt.axis('off')
plt.imshow(wordcloud)

( Second part of the Code )

import pandas as pd
from sklearn.model_selection import train_test_split
data=pd.read_csv("spamdata.csv",encoding = 'latin-1')
data.head()

data = data.rename(columns = {'v1': 'Type', 'v2': 'Messages'})

data.columns

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

for i in range(0, 5572):
    review = re.sub('[^a-zA-Z]', ' ',data['Messages'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
  
  # stemming
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
  
  # joining them back with space
    review = ' '.join(review)
    corpus.append(review)


from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
x = cv.fit_transform(corpus).toarray()
y = data.iloc[:, 0]

print(x.shape)
print(y.shape)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 42)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn.ensemble import RandomForestClassifier
from pandas_confusion import ConfusionMatrix
import matplotlib.pyplot as plt

model = RandomForestClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

print("Training Accuracy :", model.score(x_train, y_train))
print("Testing Accuracy :", model.score(x_test, y_test))

confusion_matrix = ConfusionMatrix(y_test, y_pred)
print("Confusion matrix:\n%s" % confusion_matrix)


confusion_matrix.plot()
