import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd

def basic_clean(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    text = re.sub(r"[^a-z0-9'\s]", '', text)
    return text

def tokenize(text):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(text, return_str=True)

def stem(text):
    ps = nltk.porter.PorterStemmer()
    words = text.split()
    stems = [ps.stem(word) for word in words]
    return ' '.join(stems)

def lemmatize(text):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    return ' '.join(lemmas)

def remove_stopwords(text, stopword_list=stopwords.words('english')):
    words = text.split()
    filtered_words = [word for word in words if word not in stopword_list]
    return ' '.join(filtered_words)

def nlp_prep(df):
    df = df.rename(columns={'content':'original'})
    df['clean'] = (df.original.apply(basic_clean)
                     .apply(tokenize)
                     .apply(remove_stopwords)
                  )
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    return df