from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from URL_Analyzer import emailAddressAnalyzer
file_path=r'D:\SEM 4\COMPUTER NETWORKS\CN PACKAGE\URL_Analyzer\Phishing_Email.csv'

def report_body(email_body,email_address,report):
    def train_model(csv_file):
        df = read_csv(csv_file, nrows=3000)
        df['Email Text'] = df['Email Text'].fillna('')
        X = df['Email Text']
        y = df['Email Type']
        vectorizer = CountVectorizer()
        X_vectorized = vectorizer.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        return model, vectorizer

    def predict_body(body, model, vectorizer):
        body_vectorized = vectorizer.transform([body])
        prediction = model.predict(body_vectorized)
        return prediction[0]

    model, vectorizer = train_model(file_path)
    label = predict_body(email_body, model, vectorizer)
    if label == 'Phishing Email':
        report["body_score"] = 0.99
    else:
        report["body_score"] = 0.05
    return emailAddressAnalyzer.report_emailAddress(email_address,report)

