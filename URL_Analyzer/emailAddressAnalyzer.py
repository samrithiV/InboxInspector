import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

def report_emailAddress(email_address,report):
    current_dir = os.path.dirname(__file__)
    blacklist_path = os.path.join(current_dir, 'blacklist.txt')
    whitelist_path = os.path.join(current_dir, 'whitelist.txt')

    with open(blacklist_path, 'r') as file:
        blacklist = [line.strip() for line in file]

    with open(whitelist_path, 'r') as file:
        whitelist = [line.strip() for line in file]

    whitelist = whitelist[:10000]
    data = blacklist + whitelist
    labels = [1] * len(blacklist) + [0] * len(whitelist)
    model = make_pipeline(CountVectorizer(), RandomForestClassifier())
    model.fit(data, labels)

    predicted_label = model.predict([email_address])[0]
    if predicted_label == 0:
        report["email_score"] = 0.1
    else:
        report["email_score"] = 0.99
    return report


