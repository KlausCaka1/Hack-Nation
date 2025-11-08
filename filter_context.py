import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
import re
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
import text_cleaner



nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))



def preprocess(text):
    """Clean, tokenize, remove stopwords, and lemmatize"""
    text = str(text).lower()
    text = re.sub(r'\W+', ' ', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stopwords]
    return ' '.join(tokens)

def get_tag(text, tagset='universal'):
    all_tags=['ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRT','PRON','VERB','.','X']
    rows = []

    for sentence in text.split('.'):
        pos_tags = Counter([j for i, j in nltk.pos_tag(word_tokenize(sentence), tagset=tagset)])
        rows.append(pos_tags)

    df = pd.DataFrame(rows).fillna(0).astype(int)

    for col in all_tags:
        if col not in df.columns:
            df[col] = 0

    return df[all_tags]

def normalization(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    text = text_cleaner.text_cleaner(text)
    tokens = [lemmatizer.lemmatize(word) for word in text.split() if word not in stopwords]
    return " ".join(tokens)

def GetTFIDF(text, top_n=20):
    if not text or len(text.strip()) == 0:
        return []

    cleaner_text = normalization(text)

    docs = [cleaner_text]

    vector_stop_words = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vector_stop_words.fit_transform(docs)
    feature_names = np.array(vector_stop_words.get_feature_names_out())

    scores = tfidf_matrix.toarray().flatten()

    top_indices = np.argsort(scores)[::-1][:top_n]
    top_keyword = feature_names[top_indices]

    return top_keyword.tolist()

