document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Theme Toggle Logic ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('medi_nlp_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('medi_nlp_theme', newTheme);
    });

    // --- 2. Tab Navigation Logic ---
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');

            if (targetTab === 'tab-analytics') {
                loadAnalyticsData();
            }
        });
    });

    // --- 3. Sample Prompts Loader ---
    const presetContainer = document.getElementById('preset-container');
    const textInput = document.getElementById('text-input');

    fetch('/api/sample-data')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.samples) {
                presetContainer.innerHTML = '';
                data.samples.forEach(sample => {
                    const btn = document.createElement('button');
                    btn.className = 'btn-preset';
                    btn.textContent = sample.label;
                    btn.addEventListener('click', () => {
                        textInput.value = sample.text;
                    });
                    presetContainer.appendChild(btn);
                });
            }
        })
        .catch(err => console.error("Error loading samples:", err));

    // --- 4. Single Text Analyzer Logic ---
    const btnAnalyze = document.getElementById('btn-analyze');
    const btnClear = document.getElementById('btn-clear');
    const resultsEmpty = document.getElementById('results-empty');
    const resultsContent = document.getElementById('results-content');
    const sentimentBadge = document.getElementById('sentiment-badge');

    btnAnalyze.addEventListener('click', () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter or select text for analysis.');
            return;
        }

        btnAnalyze.disabled = true;
        btnAnalyze.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        })
        .then(res => res.json())
        .then(data => {
            btnAnalyze.disabled = false;
            btnAnalyze.innerHTML = '<i class="fa-solid fa-microscope"></i> Analyze Text';

            if (!data.success) {
                alert('Error: ' + (data.error || 'Failed to analyze text'));
                return;
            }

            renderResults(data);
        })
        .catch(err => {
            btnAnalyze.disabled = false;
            btnAnalyze.innerHTML = '<i class="fa-solid fa-microscope"></i> Analyze Text';
            alert('Network error while processing request.');
            console.error(err);
        });
    });

    btnClear.addEventListener('click', () => {
        textInput.value = '';
        resultsContent.classList.add('hidden');
        resultsEmpty.classList.remove('hidden');
        sentimentBadge.className = 'badge badge-neutral';
        sentimentBadge.textContent = 'Awaiting Input';
    });

    function renderResults(data) {
        resultsEmpty.classList.add('hidden');
        resultsContent.classList.remove('hidden');

        // Sentiment badge & text
        const sent = data.sentiment.toLowerCase();
        sentimentBadge.className = `badge badge-${sent}`;
        sentimentBadge.textContent = sent.toUpperCase();

        document.getElementById('res-sentiment').textContent = sent;
        document.getElementById('res-sentiment').className = `metric-val text-capitalize text-${sent.slice(0, 3)}`;
        document.getElementById('res-confidence').textContent = `${data.confidence}%`;

        // Medical Specialty & Risk Level
        const med = data.medical_analysis;
        document.getElementById('res-specialty').textContent = med.specialty || 'General';
        
        const riskEl = document.getElementById('res-risk');
        riskEl.textContent = med.risk_level;
        if (med.risk_level.includes('High')) {
            riskEl.className = 'metric-val text-neg';
        } else if (med.risk_level.includes('Moderate')) {
            riskEl.className = 'metric-val text-neu';
        } else {
            riskEl.className = 'metric-val text-pos';
        }

        // Probability Progress Bars
        const probs = data.probabilities;
        const posProb = probs.positive || 0;
        const neuProb = probs.neutral || 0;
        const negProb = probs.negative || 0;

        document.getElementById('bar-positive').style.width = `${posProb}%`;
        document.getElementById('val-positive').textContent = `${posProb}%`;

        document.getElementById('bar-neutral').style.width = `${neuProb}%`;
        document.getElementById('val-neutral').textContent = `${neuProb}%`;

        document.getElementById('bar-negative').style.width = `${negProb}%`;
        document.getElementById('val-negative').textContent = `${negProb}%`;

        // Medical Entities
        const entitiesContainer = document.getElementById('entities-container');
        entitiesContainer.innerHTML = '';

        const entityCategories = med.entities || {};
        let hasEntities = false;

        for (const [catName, tagList] of Object.entries(entityCategories)) {
            if (tagList.length > 0) {
                hasEntities = true;
                const catDiv = document.createElement('div');
                catDiv.className = 'entity-cat';

                const title = document.createElement('span');
                title.className = 'cat-title';
                title.textContent = catName;
                catDiv.appendChild(title);

                const tagListDiv = document.createElement('div');
                tagListDiv.className = 'tag-list';

                tagList.forEach(item => {
                    const tag = document.createElement('span');
                    tag.className = 'tag';
                    tag.textContent = item;
                    tagListDiv.appendChild(tag);
                });

                catDiv.appendChild(tagListDiv);
                entitiesContainer.appendChild(catDiv);
            }
        }

        if (!hasEntities) {
            entitiesContainer.innerHTML = '<div class="text-muted" style="font-size:0.85rem">No clinical entities identified in this excerpt.</div>';
        }

        // Brief Summary
        document.getElementById('res-summary').textContent = med.summary || data.text;
    }

    // --- 5. Batch Explorer Logic ---
    const btnLoadDataset = document.getElementById('btn-load-dataset');
    const batchTableBody = document.getElementById('batch-table-body');
    const batchStatsContainer = document.getElementById('batch-stats-container');

    btnLoadDataset.addEventListener('click', () => {
        btnLoadDataset.disabled = true;
        btnLoadDataset.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Batch...';

        fetch('/api/batch-predict', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                btnLoadDataset.disabled = false;
                btnLoadDataset.innerHTML = '<i class="fa-solid fa-database"></i> Run Batch Prediction (data.csv)';

                if (data.success && data.results) {
                    renderBatchResults(data);
                }
            })
            .catch(err => {
                btnLoadDataset.disabled = false;
                btnLoadDataset.innerHTML = '<i class="fa-solid fa-database"></i> Run Batch Prediction (data.csv)';
                alert('Failed to load batch dataset.');
                console.error(err);
            });
    });

    function renderBatchResults(data) {
        batchStatsContainer.classList.remove('hidden');
        document.getElementById('batch-total').textContent = data.summary.total_processed;
        document.getElementById('batch-pos').textContent = data.summary.positive_count;
        document.getElementById('batch-neu').textContent = data.summary.neutral_count;
        document.getElementById('batch-neg').textContent = data.summary.negative_count;

        batchTableBody.innerHTML = '';

        data.results.forEach(row => {
            const tr = document.createElement('tr');
            const sent = row.predicted_sentiment.toLowerCase();

            tr.innerHTML = `
                <td><strong>${row.id}</strong></td>
                <td title="${row.full_sentence}">${row.sentence}</td>
                <td><span class="badge badge-${sent}">${sent}</span></td>
                <td><strong>${row.confidence}%</strong></td>
                <td><span class="text-accent" style="font-weight:600">${row.specialty}</span></td>
                <td><small>${row.risk_level.split(' ')[0]}</small></td>
            `;
            batchTableBody.appendChild(tr);
        });
    }

    // --- 6. Analytics & Charts Logic ---
    let distChart = null;

    function loadAnalyticsData() {
        fetch('/api/dataset-stats')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    renderCharts(data.sentiment_counts);
                    renderMetricsTable(data.metrics);
                }
            })
            .catch(err => console.error("Error loading analytics:", err));
    }

    function renderCharts(counts) {
        const ctx = document.getElementById('chart-sentiment-dist').getContext('2d');
        if (distChart) distChart.destroy();

        distChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Neutral', 'Positive', 'Negative'],
                datasets: [{
                    data: [counts.neutral || 0, counts.positive || 0, counts.negative || 0],
                    backgroundColor: ['#0d9488', '#10b981', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#131b2e'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#cbd5e1', font: { family: 'Inter', weight: '600' } }
                    }
                }
            }
        });
    }

    function renderMetricsTable(metrics) {
        const container = document.getElementById('classification-metrics-table');
        if (!metrics || !metrics.report) {
            container.innerHTML = '<div class="text-muted">Metrics not available. Run train.py to refresh.</div>';
            return;
        }

        const report = metrics.report;
        container.innerHTML = `
            <div class="metric-row-box">
                <span class="metric-label">Overall Accuracy</span>
                <span class="metric-val text-accent">${metrics.accuracy}%</span>
            </div>
            <div class="metric-row-box">
                <span class="metric-label">Positive Class Precision / Recall</span>
                <span class="metric-val">${(report.positive.precision * 100).toFixed(1)}% / ${(report.positive.recall * 100).toFixed(1)}%</span>
            </div>
            <div class="metric-row-box">
                <span class="metric-label">Neutral Class Precision / Recall</span>
                <span class="metric-val">${(report.neutral.precision * 100).toFixed(1)}% / ${(report.neutral.recall * 100).toFixed(1)}%</span>
            </div>
            <div class="metric-row-box">
                <span class="metric-label">Negative Class Precision / Recall</span>
                <span class="metric-val">${(report.negative.precision * 100).toFixed(1)}% / ${(report.negative.recall * 100).toFixed(1)}%</span>
            </div>
        `;
    }

    // Auto-load analytics stats on initial load
    loadAnalyticsData();
});
