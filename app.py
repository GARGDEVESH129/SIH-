from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Registration model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    options = db.Column(db.String(200))  # Store options as a comma-separated string

    def __repr__(self):
        return f'<Registration {self.name}>'

# Load datasets
df = pd.read_csv('labeled_seriousness_dataset.csv')
hospital_df = pd.read_csv('hospital_data.csv')

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/get_prescription', methods=['GET'])
def get_prescription():
    condition = request.args.get('condition').lower()
    result = df[df['Condition'].str.lower() == condition]
    
    if not result.empty:
        prescriptions = result[['Medicine', 'Dosage', 'Duration_Days']].to_dict(orient='records')
        selected_prescriptions = random.sample(prescriptions, min(3, len(prescriptions)))
        return jsonify(selected_prescriptions)
    else:
        return jsonify({"error": "No medicines found for this condition. Showing nearby hospitals on the map."})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_registration = Registration(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        hospital=data['hospital'],
        options=','.join(data['options'])  # Convert list of options to a comma-separated string
    )
    db.session.add(new_registration)
    db.session.commit()
    print(f"Received registration data: {data}")
    return jsonify({"success": True, "hospital": data['hospital']})

@app.route('/hospital_details/<hospital_name>', methods=['GET'])
def hospital_details_by_name(hospital_name):
    filtered_data = hospital_df[hospital_df['name'] == hospital_name].to_dict(orient='records')
    return render_template('hospital_details.html', data=filtered_data)

@app.route('/register', methods=['GET'])
def registration_page():
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
