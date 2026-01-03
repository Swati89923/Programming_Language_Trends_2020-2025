from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Load data
df = pd.read_csv('normalized_data.csv')
df['Year'] = df['Year'].astype(int)
df['Language'] = df['Language'].astype(str).str.lower()

# Define languages of interest
LANGUAGES = [
    'java', 'javascript', 'c#', 'c++', 'python',
    'kotlin', 'rust', 'swift', 'scala', 'perl', 'matlab'
]

# Define the year range
ALL_YEARS = list(range(2020, 2026))

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory('static', 'styles.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('static', 'script.js')

@app.route('/chart-data')
def chart_data():
    datasets = []
    colors = [
        'red', 'blue', 'green', 'orange', 'purple', 'teal',
        'pink', 'brown', 'black', 'magenta', 'cyan', 'gold'
    ]

    for i, lang in enumerate(LANGUAGES):
        yearly_counts = []
        for year in ALL_YEARS:
            count = df[
                (df['Year'] == year) &
                (df['Language'].str.contains(lang, case=False, regex=False))
            ].shape[0]
            yearly_counts.append(count)

        datasets.append({
            'label': lang,
            'data': yearly_counts,
            'borderColor': colors[i % len(colors)],
            'fill': False,
            'tension': 0.3
        })

    return jsonify({
        'labels': ALL_YEARS,
        'datasets': datasets
    })

if __name__ == '__main__':
    app.run(debug=True)