from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import random

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('labeled_seriousness_dataset.csv')

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/static/hospital_locations.csv')
def hospital_locations():
    return send_from_directory('static', 'hospital_locations.csv')

@app.route('/get_prescription', methods=['GET'])
def get_prescription():
    condition = request.args.get('condition').lower()

    result = df[df['Condition'].str.lower() == condition]
    
    if not result.empty:
        prescriptions = result[['Medicine', 'Dosage', 'Duration_Days']].to_dict(orient='records')
        selected_prescriptions = random.sample(prescriptions, min(3, len(prescriptions)))
        return jsonify(selected_prescriptions)
    else:
        return jsonify({"error": "No medicines found for this condition. Show map instead."})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Process registration data (store in a database, send an email, etc.)
    # For now, we'll just return a success response
    print(f"Received registration data: {data}")
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
