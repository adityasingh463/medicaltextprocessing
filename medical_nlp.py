import re

SPECIALTY_KEYWORDS = {
    'Cardiology': ['heart', 'cardiac', 'myocardial', 'infarction', 'artery', 'blood pressure', 'hypertension', 'ecg', 'electrocardiogram', 'pulse', 'arrhythmia', 'angina', 'ventricular', 'atrial', 'aortic', 'coronary'],
    'Neurology': ['brain', 'stroke', 'seizure', 'neurological', 'headache', 'migraine', 'nerve', 'paralysis', 'tremor', 'eeg', 'cognitive', 'dementia', 'spine', 'spinal', 'cerebral'],
    'Pulmonology': ['lung', 'respiratory', 'breath', 'dyspnea', 'cough', 'asthma', 'pneumonia', 'bronchial', 'oxygen', 'spo2', 'wheezing', 'pulmonary', 'chest xray'],
    'Gastroenterology': ['stomach', 'abdominal', 'gastrointestinal', 'nausea', 'vomiting', 'diarrhea', 'colon', 'liver', 'endoscopy', 'colonoscopy', 'digestive', 'bowel', 'ulcer', 'gastric'],
    'Orthopedics': ['bone', 'fracture', 'joint', 'knee', 'spine', 'femur', 'tibia', 'ligament', 'tendon', 'orthopedic', 'arthroscopy', 'hip', 'disc', 'skeletal', 'cartilage'],
    'Oncology': ['cancer', 'tumor', 'carcinoma', 'chemotherapy', 'radiation', 'biopsy', 'metastasis', 'malignant', 'oncology', 'lesion', 'mass', 'lymph node'],
    'Dermatology': ['skin', 'rash', 'lesion', 'dermatitis', 'eczema', 'melanoma', 'epidermis', 'biopsy', 'erythema', 'pruritus', 'wound'],
    'Psychiatry': ['depression', 'anxiety', 'mood', 'psychiatric', 'schizophrenia', 'bipolar', 'insomnia', 'stress', 'mental health', 'suicidal', 'hallucination']
}

MEDICAL_ENTITIES = {
    'Symptoms': [
        'pain', 'fever', 'chest pain', 'shortness of breath', 'dyspnea', 'headache',
        'nausea', 'vomiting', 'fatigue', 'dizziness', 'cough', 'swelling', 'edema',
        'hypertension', 'hypotension', 'arrhythmia', 'rash', 'numbness', 'palpitations'
    ],
    'Anatomy': [
        'heart', 'lung', 'lungs', 'brain', 'liver', 'kidney', 'stomach', 'chest',
        'spine', 'knee', 'abdomen', 'aorta', 'colon', 'artery', 'vein', 'joint', 'skin'
    ],
    'Medications & Treatments': [
        'aspirin', 'metformin', 'lisinopril', 'atorvastatin', 'amoxicillin', 'ibuprofen',
        'paracetamol', 'insulin', 'chemotherapy', 'beta-blocker', 'antibiotics', 'steroids',
        'heparin', 'statins', 'morphine', 'acetaminophen'
    ],
    'Procedures': [
        'ecg', 'electrocardiogram', 'mri', 'ct scan', 'x-ray', 'biopsy', 'endoscopy',
        'colonoscopy', 'surgery', 'catheterization', 'blood test', 'ultrasound', 'angioplasty'
    ]
}

CRITICAL_TERMS = [
    'infarction', 'stroke', 'cardiac arrest', 'severe chest pain', 'acute hemorrhage',
    'respiratory failure', 'sepsis', 'malignant', 'unresponsive', 'anaphylaxis', 'critical'
]

FAVORABLE_TERMS = [
    'stable', 'improved', 'normal', 'recovering', 'resolved', 'benign', 'no distress',
    'cleared', 'intact', 'healthy', 'satisfactory'
]

def analyze_medical_text(text):
    if not isinstance(text, str) or not text.strip():
        return {
            'specialty': 'General Medicine',
            'entities': {'Symptoms': [], 'Anatomy': [], 'Medications & Treatments': [], 'Procedures': []},
            'risk_level': 'Low',
            'clinical_outlook': 'Stable',
            'summary': 'No clinical text provided.',
            'word_count': 0
        }
    
    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower)
    word_count = len(words)
    
    # 1. Detect Medical Specialty
    specialty_scores = {}
    for specialty, keywords in SPECIALTY_KEYWORDS.items():
        score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
        if score > 0:
            specialty_scores[specialty] = score
            
    detected_specialty = max(specialty_scores, key=specialty_scores.get) if specialty_scores else 'General Medicine'
    
    # 2. Extract Entities
    extracted_entities = {}
    for category, entity_list in MEDICAL_ENTITIES.items():
        found = []
        for item in entity_list:
            if re.search(r'\b' + re.escape(item) + r'\b', text_lower):
                found.append(item.title())
        extracted_entities[category] = list(set(found))
        
    # 3. Determine Risk Level & Outlook
    critical_matches = [term for term in CRITICAL_TERMS if re.search(r'\b' + re.escape(term) + r'\b', text_lower)]
    favorable_matches = [term for term in FAVORABLE_TERMS if re.search(r'\b' + re.escape(term) + r'\b', text_lower)]
    
    if critical_matches:
        risk_level = 'High (Urgent Attention Required)'
        clinical_outlook = 'Critical / Guarded'
    elif len(extracted_entities['Symptoms']) >= 3:
        risk_level = 'Moderate (Follow-up Recommended)'
        clinical_outlook = 'Needs Monitoring'
    elif favorable_matches:
        risk_level = 'Low / Normal'
        clinical_outlook = 'Favorable / Stable'
    else:
        risk_level = 'Low / Standard Routine'
        clinical_outlook = 'Stable'
        
    # 4. Generate Clinical Summary
    summary_sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    brief_summary = " ".join(summary_sentences[:2]) if summary_sentences else text[:150]
    
    return {
        'specialty': detected_specialty,
        'specialty_scores': specialty_scores,
        'entities': extracted_entities,
        'risk_level': risk_level,
        'critical_terms_found': critical_matches,
        'favorable_terms_found': favorable_matches,
        'clinical_outlook': clinical_outlook,
        'summary': brief_summary,
        'word_count': word_count
    }
