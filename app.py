from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import re
import os
from medical_nlp import analyze_medical_text

app = Flask(__name__)

# Load Model & Vectorizer
MODEL_PATH = "models/sentiment_model.pkl"
VEC_PATH = "models/tfidf_vectorizer.pkl"
METRICS_PATH = "models/metrics.pkl"
DATA_PATH = "data.csv"

model = None
vectorizer = None
metrics = None

def load_resources():
    global model, vectorizer, metrics
    if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VEC_PATH)
        print("Loaded trained model and vectorizer.")
    else:
        print("Model files not found. Running training script...")
        from train import train_nlp_model
        train_nlp_model(DATA_PATH)
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VEC_PATH)
        
    if os.path.exists(METRICS_PATH):
        metrics = joblib.load(METRICS_PATH)

load_resources()

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        
        if not text or not text.strip():
            return jsonify({'error': 'Please enter valid text for analysis.'}), 400
            
        cleaned = clean_text(text)
        vec_text = vectorizer.transform([cleaned])
        
        # Sentiment prediction
        pred = model.predict(vec_text)[0]
        probs = model.predict_proba(vec_text)[0]
        classes = model.classes_
        
        prob_dict = {str(c): round(float(p) * 100, 2) for c, p in zip(classes, probs)}
        max_confidence = round(float(np.max(probs)) * 100, 2)
        
        # Medical Analysis
        med_analysis = analyze_medical_text(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'sentiment': pred,
            'confidence': max_confidence,
            'probabilities': prob_dict,
            'medical_analysis': med_analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medical-analyze', methods=['POST'])
def medical_analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        if not text or not text.strip():
            return jsonify({'error': 'Please provide medical transcription text.'}), 400
            
        analysis = analyze_medical_text(text)
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset-stats', methods=['GET'])
def dataset_stats():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({'error': 'Dataset not found'}), 404
            
        df = pd.read_csv(DATA_PATH)
        df['Sentiment'] = df['Sentiment'].astype(str).str.lower().str.strip()
        sentiment_counts = df['Sentiment'].value_counts().to_dict()
        
        total_samples = len(df)
        avg_sentence_len = round(float(df['Sentence'].dropna().astype(str).apply(lambda x: len(x.split())).mean()), 1)
        
        model_metrics = metrics if metrics else {}
        
        return jsonify({
            'success': True,
            'total_samples': total_samples,
            'avg_word_count': avg_sentence_len,
            'sentiment_counts': sentiment_counts,
            'metrics': model_metrics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    try:
        if 'file' in request.files:
            file = request.files['file']
            df = pd.read_csv(file)
        else:
            # Load default dataset preview (first 25 rows)
            df = pd.read_csv(DATA_PATH).head(25)
            
        text_col = 'Sentence' if 'Sentence' in df.columns else df.columns[0]
        df[text_col] = df[text_col].astype(str)
        
        clean_texts = df[text_col].apply(clean_text).tolist()
        vec_texts = vectorizer.transform(clean_texts)
        
        preds = model.predict(vec_texts)
        probs = model.predict_proba(vec_texts)
        max_probs = np.max(probs, axis=1)
        
        results = []
        for i, row in df.iterrows():
            text_val = row[text_col]
            med_info = analyze_medical_text(text_val)
            results.append({
                'id': i + 1,
                'sentence': text_val[:120] + ('...' if len(text_val) > 120 else ''),
                'full_sentence': text_val,
                'actual_sentiment': str(row.get('Sentiment', 'N/A')),
                'predicted_sentiment': str(preds[i]),
                'confidence': round(float(max_probs[i]) * 100, 1),
                'specialty': med_info['specialty'],
                'risk_level': med_info['risk_level']
            })
            
        summary = {
            'total_processed': len(results),
            'positive_count': sum(1 for r in results if r['predicted_sentiment'] == 'positive'),
            'neutral_count': sum(1 for r in results if r['predicted_sentiment'] == 'neutral'),
            'negative_count': sum(1 for r in results if r['predicted_sentiment'] == 'negative')
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-data', methods=['GET'])
def sample_data():
    samples = [
        {
            'label': 'Cardiology Clinical Note',
            'category': 'Medical',
            'text': 'Patient presents with acute severe chest pain radiating to the left arm and dyspnea. ECG showed ST elevation. Administered aspirin and heparin. Immediate cardiac catheterization recommended.'
        },
        {
            'label': 'Favorable Recovery Report',
            'category': 'Medical',
            'text': 'Patient is recovering well after knee arthroscopy. Surgical wound is clean and intact with no swelling or redness. Vital signs are normal and stable. Discharged with routine physical therapy.'
        },
        {
            'label': 'Positive Financial Release',
            'category': 'Financial Sentiment',
            'text': 'Kone net sales rose by 14% year-on-year in the first nine months with strong operating profit growth.'
        },
        {
            'label': 'Negative Market Report',
            'category': 'Financial Sentiment',
            'text': 'The company reported a severe net loss in Q3 due to unexpected raw material cost inflation and falling revenues.'
        },
        {
            'label': 'Neutral Corporate Announcement',
            'category': 'General',
            'text': 'The annual general meeting of shareholders will be held on Thursday at the corporate headquarters in Espoo.'
        }
    ]
    return jsonify({'success': True, 'samples': samples})

if __name__ == '__main__':
    print("Starting NLP & Medical Transcription Analysis Web Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
