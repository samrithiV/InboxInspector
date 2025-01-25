import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from URL_Analyzer import emailBodyAnalyzer
file_name = r'D:\SEM 4\COMPUTER NETWORKS\CN PACKAGE\URL_Analyzer\malicious_phish.csv'

def email_report(email_address, urls, email_body):
    report = {}
    predicted_labels = []
    url_score = 0

    def train_model(csv_file):
        df = pd.read_csv(csv_file, nrows=10000)
        X = df['url']
        y = df['type']
        vectorizer = CountVectorizer()
        X_vectorized = vectorizer.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model, vectorizer
    
    def predict_url(url, model, vectorizer):
        url_vectorized = vectorizer.transform([url])
        prediction = model.predict(url_vectorized)
        return prediction[0]
    
    # Initialize report
    report["url_score"] = 0
    
    if len(urls) != 0:
        model, vectorizer = train_model(file_name)
        for given_url in urls:
            label = predict_url(given_url, model, vectorizer)
            predicted_labels.append(label)
            if label == 'benign':
                url_score += 0.01
            elif label == 'defacement':
                url_score += 0.25
            elif label == 'phishing':
                url_score += 0.7
            else:
                url_score += 0.99
        url_score = url_score / len(urls)
        report["url_score"] = url_score
        emailBodyAnalyzer.report_body(email_body, email_address, report)
        return report

    else:
        report = emailBodyAnalyzer.report_body(email_body, email_address, report)
        return report

