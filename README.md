# Medical Transcription & NLP Sentiment Analysis Intelligence

An end-to-end Natural Language Processing (NLP) web application built using Python, Scikit-Learn, and Flask. It provides clinical text intelligence, medical transcription analysis, named entity extraction (NER), and sentiment classification on the provided dataset (`data.csv`).

## 🌟 Key Features

1. **Medical Transcription & Clinical Text Extraction (`medical_nlp.py`)**:
   - **Medical Specialty Classifier**: Categorizes transcripts into Cardiology, Neurology, Pulmonology, Gastroenterology, Orthopedics, Oncology, Dermatology, Psychiatry, or General Medicine.
   - **Clinical Entity Extraction (NER)**: Automatically extracts Symptoms, Anatomical Structures, Medications/Treatments, and Procedures/Surgeries.
   - **Risk & Outlook Assessment**: Evaluates clinical urgency (High/Critical, Moderate, Low/Stable).

2. **Sentiment Analysis Machine Learning Pipeline (`train.py`)**:
   - Uses **TF-IDF Feature Union** (Word N-grams + Character WB N-grams) with Logistic Regression.
   - Evaluates and outputs accuracy, precision, recall, and class distribution stats.

3. **High-Contrast Accessible UI (`static/css/styles.css`)**:
   - **Accessible Contrast Design**: High contrast typography and color palettes for maximum legibility (WCAG AAA compliant contrast ratios).
   - **Dark & Light Mode Toggle**: One-click toggle between Dark Slate Mode and Crisp Light Mode.
   - **Interactive Visualizations**: Progress bars for class probabilities and Chart.js pie chart for dataset distribution.

4. **Batch Explorer & API Endpoints (`app.py`)**:
   - Real-time single sentence analyzer.
   - Batch CSV runner for thousands of rows.
   - REST API endpoints (`/api/predict`, `/api/medical-analyze`, `/api/batch-predict`, `/api/dataset-stats`).

---

## 🚀 How to Run the Project

1. **Install Dependencies**:
   ```bash
   pip install pandas scikit-learn flask matplotlib joblib uvicorn
   ```

2. **Train the NLP Model (Optional, auto-runs if models are missing)**:
   ```bash
   python train.py
   ```

3. **Start the Web Server**:
   ```bash
   python app.py
   ```

4. **Open in Browser**:
   Navigate to `http://localhost:5000` or `http://127.0.0.1:5000`.

---

## 📁 Project Structure

```
nlpproject/
│
├── data.csv                 # Dataset file (Sentence, Sentiment)
├── train.py                 # Model training & vectorization script
├── medical_nlp.py           # Medical NLP entity extraction & specialty engine
├── app.py                   # Flask server & REST API endpoints
├── models/                  # Trained ML models and vectorizers
│   ├── sentiment_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── metrics.pkl
├── templates/
│   └── index.html           # Main web interface template
└── static/
    ├── css/
    │   └── styles.css       # High-contrast CSS stylesheet (Dark/Light mode)
    └── js/
        └── main.js          # Interactive UI logic & API integrations
```
