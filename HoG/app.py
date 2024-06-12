from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo
from datetime import datetime

import logging

app = Flask(__name__)

# Replace the following with your MongoDB connection URI
app.config["MONGO_URI"] = "mongodb+srv://tarunjanapati7:%4074run54I@educationdetaails.x0zu5mp.mongodb.net/?retryWrites=true&w=majority&appName=EducationDetaails"
mongo = PyMongo(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form
            birthdate_str = data['birthdate']
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            
            client_details = {
                "name": data['name'],
                "address": data['address'],
                "zip_code": data['zip'],
                "phone": data['phone'],
                "birthdate": birthdate,
                "age": int(data['age']),
                "sex": data['sex'],
                "race": data['race'],
                "ethnicity": data['ethnicity'],
                "marital_status": data['marital_status'],
                "length_stay_previous_address": data['length_stay_previous_address'],
                "country_of_origin": data['country_of_origin'],
                "times_in_shelter": int(data['times_in_shelter']),
                "length_stay_previous_shelter": data['length_stay_previous_shelter'],
                "number_of_children": int(data['number_of_children']),
                "education_level": data['education_level'],
                "employment_status": data['employment_status'],
                "income_amount_intake": float(data['income_amount_intake']),
                "income_source_intake": data['income_source_intake'],
                "income_amount_exit": float(data['income_amount_exit']),
                "income_1_year_exit": float(data['income_1_year_exit']),
                "weeks_pregnant": int(data['weeks_pregnant']),
                "prenatal_care_prior_intake": data['prenatal_care_prior_intake'],
                "father_involvement": data['father_involvement'],
                "father_education_level": data['father_education_level'],
                "father_occupation": data['father_occupation'],
                "father_income": float(data['father_income']),
                "domestic_violence_survivor": data['domestic_violence_survivor'],
                "veteran_status": data['veteran_status']
            }

            mongo.db.client_details.insert_one(client_details)
            return jsonify({'message': 'Form submitted successfully'}), 200
        except Exception as e:
            logging.error(f"Error submitting form: {e}")
            return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client_details')
def client_details():
    try:
        clients = mongo.db.client_details.find()
        clients_list = list(clients)  # Convert to list to pass to the template
        logging.debug(f"Retrieved {len(clients_list)} clients")
        return render_template('client_details.html', clients=clients_list)
    except Exception as e:
        logging.error(f"Error retrieving client details: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)