import pandas as pd
import numpy as np
import re
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_nlp_model(data_path="data.csv"):
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path).dropna(subset=['Sentence', 'Sentiment'])
    df['Sentence_clean'] = df['Sentence'].apply(preprocess_text)
    df['Sentiment'] = df['Sentiment'].str.lower().str.strip()
    
    X = df['Sentence_clean']
    y = df['Sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    # Dual Word + Char Feature Extractor
    word_vec = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=10000,
        sublinear_tf=True,
        stop_words='english'
    )
    
    char_vec = TfidfVectorizer(
        ngram_range=(2, 5),
        analyzer='char_wb',
        max_features=12000,
        sublinear_tf=True
    )
    
    union = FeatureUnion([
        ('word', word_vec),
        ('char', char_vec)
    ])
    
    X_train_vec = union.fit_transform(X_train)
    X_test_vec = union.transform(X_test)
    
    # Calibrated Classifier for Optimal Probabilities & Accuracy
    base_svc = LinearSVC(C=1.2, max_iter=2000, random_state=42)
    clf = CalibratedClassifierCV(estimator=base_svc, method='sigmoid')
    clf.fit(X_train_vec, y_train)
    
    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nFinal Optimized Model Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    report = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))
    
    cm = confusion_matrix(y_test, y_pred, labels=['negative', 'neutral', 'positive'])
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/sentiment_model.pkl")
    joblib.dump(union, "models/tfidf_vectorizer.pkl")
    
    metrics = {
        'accuracy': round(acc * 100, 2),
        'report': report,
        'confusion_matrix': cm.tolist(),
        'classes': ['negative', 'neutral', 'positive'],
        'dataset_size': len(df),
        'class_counts': y.value_counts().to_dict()
    }
    joblib.dump(metrics, "models/metrics.pkl")
    print("Optimized model saved successfully to models/")

if __name__ == "__main__":
    train_nlp_model()
