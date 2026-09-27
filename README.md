# Medical Transcription & Text Processing Intelligence (NLP)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-00E599.svg?style=for-the-badge&logo=render&logoColor=white)](https://medicaltextprocessing.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

An end-to-end Natural Language Processing (NLP) & Medical Text Intelligence web application built with Python, Scikit-Learn, and Flask. The platform provides real-time clinical text entity extraction, medical specialty classification, patient risk scoring, and sentiment prediction on the dataset (`data.csv`).

---

## 🌐 Live Web Application

👉 **[https://medicaltextprocessing.onrender.com/](https://medicaltextprocessing.onrender.com/)**

Try out the live web app online directly on Render!

---

## 🌟 Key Features

1. **Medical Transcription & Clinical Entity Extractor (`medical_nlp.py`)**:
   - **Medical Specialty Classifier**: Categorizes clinical transcripts into *Cardiology, Neurology, Pulmonology, Gastroenterology, Orthopedics, Oncology, Dermatology, Psychiatry,* or *General Medicine*.
   - **Named Entity Recognition (NER)**: Extracts key clinical concepts including **Symptoms & Conditions**, **Anatomical Structures**, **Medications & Treatments**, and **Procedures & Surgeries**.
   - **Risk & Outlook Scoring**: Automatically flags clinical urgency (*High/Critical, Moderate, Low/Stable*).

2. **Machine Learning Sentiment Pipeline (`train.py`)**:
   - **Feature Union Vectorizer**: Combines Word N-grams (1-3) and Character WB N-grams (2-5) with sublinear TF-IDF scaling.
   - **Calibrated Classifier**: Logistic Regression / LinearSVC classifier calibrated for probability estimates.

3. **Modern Accessible Web UI (`templates/index.html` & `static/css/styles.css`)**:
   - **Clean Minimalist Light Mode**: High-contrast, WCAG AAA compliant typography and professional color palette.
   - **Interactive Visualization**: Sentiment probability progress bars, sample prompt presets, and Chart.js analytics charts.
   - **Theme Switcher**: One-click toggle between Light Mode and Dark Slate Mode.

4. **Batch Processing & REST APIs (`app.py`)**:
   - **Single Text Analyzer**: Real-time extraction and confidence breakdown.
   - **Batch Explorer**: Runs dataset predictions across thousands of rows.
   - **REST APIs**: `/api/predict`, `/api/medical-analyze`, `/api/batch-predict`, and `/api/dataset-stats`.

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/adityasingh463/medicaltextprocessing.git
cd medicaltextprocessing
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Server
```bash
python app.py
```

### 4. Access the Web App Locally
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📡 REST API Documentation

### `POST /api/predict`
Analyzes a single clinical text input.
- **Request Body**: `{"text": "Patient presents with severe chest pain and dyspnea."}`
- **Response**:
```json
{
  "success": true,
  "sentiment": "neutral",
  "confidence": 78.5,
  "probabilities": {
    "positive": 12.3,
    "neutral": 78.5,
    "negative": 9.2
  },
  "medical_analysis": {
    "specialty": "Cardiology",
    "risk_level": "High (Urgent Attention Required)",
    "entities": {
      "Symptoms": ["Chest Pain", "Dyspnea"],
      "Anatomy": ["Chest"],
      "Procedures": ["ECG"]
    }
  }
}
```

### `GET /api/dataset-stats`
Returns dataset distribution counters and model training metrics.

---

## 📁 Project Structure

```
medicaltextprocessing/
│
├── data.csv                 # Dataset file (Sentence, Sentiment)
├── train.py                 # ML training & feature vectorization pipeline
├── medical_nlp.py           # Medical specialty & clinical NER engine
├── app.py                   # Flask server & REST API endpoints
├── wsgi.py                  # Production WSGI entrypoint
├── Procfile                 # Production server configuration (Gunicorn)
├── render.yaml              # Render 1-click deployment Blueprint
├── requirements.txt         # Python package dependencies
├── README.md                # Project documentation
├── models/                  # Saved ML models & vectorizers
│   ├── sentiment_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── metrics.pkl
├── templates/
│   └── index.html           # Main web application HTML template
└── static/
    ├── css/
    │   └── styles.css       # High-contrast stylesheet (Light & Dark theme)
    └── js/
        └── main.js          # Interactive JavaScript client logic
```

---

## 🛡️ License
This project is open-source under the [MIT License](LICENSE).
