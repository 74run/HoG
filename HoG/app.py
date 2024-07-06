from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime
import logging

app = Flask(__name__)

# Replace with your MongoDB connection URI
app.config["MONGO_URI"] = "mongodb+srv://tarunjanapati7:%4074run54I@educationdetaails.x0zu5mp.mongodb.net/client_details?retryWrites=true&w=majority&appName=EducationDetaails"
mongo = PyMongo(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form
            
            # Parse and format the birthdate
            birthdate = data.get('birthdate', '')
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d') if birthdate else None
            
            user_details = {
                "client_details" : {
                    "name": data.get('name', ''),
                    "address": data.get('address', ''),
                    "zip_code": data.get('zip', ''),
                    "phone": data.get('phone', ''),
                    "birthdate": birthdate,
                    "age": int(data.get('age', 0)) if data.get('age') else None,
                    "sex": data.get('sex', ''),
                    "race": data.get('race', ''),
                    "ethnicity": data.get('ethnicity', ''),
                    "marital_status": data.get('marital_status', ''),
                    "length_stay_previous_address": data.get('length_stay_previous_address', ''),
                    "country_of_origin": data.get('country_of_origin', ''),
                    "times_in_shelter": int(data.get('times_in_shelter', 0)) if data.get('times_in_shelter') else None,
                    "length_stay_previous_shelter": data.get('length_stay_previous_shelter', ''),
                    "number_of_children": int(data.get('number_of_children', 0)) if data.get('number_of_children') else None,
                    "education_level": data.get('education_level', ''),
                    "employment_status": data.get('employment_status', ''),
                    "income_amount_intake": float(data.get('income_amount_intake', 0)) if data.get('income_amount_intake') else None,
                    "income_source_intake": data.get('income_source_intake', ''),
                    "income_amount_exit": float(data.get('income_amount_exit', 0)) if data.get('income_amount_exit') else None,
                    "income_1_year_exit": float(data.get('income_1_year_exit', 0)) if data.get('income_1_year_exit') else None,
                    "weeks_pregnant": int(data.get('weeks_pregnant', 0)) if data.get('weeks_pregnant') else None,
                    "prenatal_care_prior_intake": data.get('prenatal_care_prior_intake', ''),
                    "father_involvement": data.get('father_involvement', ''),
                    "father_education_level": data.get('father_education_level', ''),
                    "father_occupation": data.get('father_occupation', ''),
                    "father_income": float(data.get('father_income', 0)) if data.get('father_income') else None,
                    "domestic_violence_survivor": data.get('domestic_violence_survivor', ''),
                    "veteran_status": data.get('veteran_status', '')
                },
                "health_details" : {
                    "highbp": data.get("highbp", ""),
                    "diabetes": data.get("diabetes", ""),
                    "heartdisease": data.get("heartdisease", ""),
                    "livebirths": data.get("livebirths", ""),
                    "miscarriages": int(data.get("miscarriages", 0)) if data.get("miscarriages") else None,
                    "diagdisabilty": data.get("diagdisabilty", ""),
                    "rehosp": data.get("rehosp", ""),
                    "doula": data.get("doula", ""),
                    "highriskpreg": data.get("highriskpreg", ""),
                    "vaginalbirth": data.get("vaginalbirth", "")
                }
            }

            mongo.db.user_details.insert_one(user_details)
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
        clients = mongo.db.user_details.find()
        clients_list = list(clients)  # Convert to list to pass to the template
        logging.debug(f"Retrieved {len(clients_list)} clients")
        return render_template('client_details.html', clients=clients_list)
    except Exception as e:
        logging.error(f"Error retrieving client details: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        obj_id = ObjectId(client_id)
        result = mongo.db.user_details.delete_one({'_id': obj_id})

        if result.deleted_count == 1:
            logging.debug(f"Deleted client with id: {client_id}")
            return jsonify({'message': 'Client deleted successfully'}), 200
        else:
            return jsonify({'error': 'Client not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting client: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/edit_client/<client_id>', methods=['PUT'])
def edit_client(client_id):
    try:
        data = request.json
        
        birthdate = data.get('birthdate', '')
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d') if birthdate else None
        
        update_fields = {
            "client_details.name": data.get('name', ''),
            "client_details.address": data.get('address', ''),
            "client_details.zip_code": data.get('zip', ''),
            "client_details.phone": data.get('phone', ''),
            "client_details.birthdate": birthdate,
            "client_details.age": int(data.get('age', 0)) if data.get('age') else None,
            "client_details.sex": data.get('sex', ''),

        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.user_details.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Client updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating client: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/edit_health_client/<client_id>', methods=['PUT'])
def edit_health_client(client_id):
    try:
        data = request.json
        
        birthdate = data.get('birthdate', '')
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d') if birthdate else None
        
        update_fields = {
            "health_details.highbp": data.get("highbp", ""),
            "health_details.diabetes": data.get("diabetes", ""),
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.user_details.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Client updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating client: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
