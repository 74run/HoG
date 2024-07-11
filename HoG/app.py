from flask import Flask, request, render_template, jsonify, render_template_string, session, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime, timedelta

import logging



app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Set the session lifetime to 30 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

PASSWORD = '12345678'



# Replace with your MongoDB connection URI
app.config["MONGO_URI"] = "mongodb+srv://tarunjanapati7:%4074run54I@educationdetaails.x0zu5mp.mongodb.net/client_details?retryWrites=true&w=majority&appName=EducationDetaails"
mongo = PyMongo(app)

# Configure logging
logging.basicConfig(level=logging.WARNING)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form
            
            # Parse and format the birthdate
            birthdate = data.get('birthdate', '')
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d') if birthdate else None
            
            
            date_of_entry = data.get('date_of_entry', '')
            date_of_entry = datetime.strptime(date_of_entry, '%Y-%m-%d') if date_of_entry else None
            
            date_of_exit = data.get('date_of_exit', '')
            date_of_exit = datetime.strptime(date_of_exit, '%Y-%m-%d') if date_of_exit else None
            
            number_of_children = int(data.get('number_of_children', 0))
            
            children = []
            for i in range(1, number_of_children + 1):
                child_name = data.get(f'child_name_{i}', '')
                child_dob = data.get(f'child_dob_{i}', '')
                child_dob = datetime.strptime(child_dob, '%Y-%m-%d') if child_dob else None
                
                children.append({
                    'name': child_name,
                    'date_of_birth': child_dob
                })
            
            
            
            user_details = {
                "client_details" : {
                    
                    "date_of_entry": date_of_entry,
                    "date_of_exit": date_of_exit,
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
                    "children": children,
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
                },
                
                # Extract infant details from the received JSON
                "shelter_infant_details" : {
                    "infant_name": data.get("infant_name", ""),
                    "birthdate": data.get("birthdate", ""),
                    "birth_weight": float(data.get("birth_weight", 0)) if data.get("birth_weight") else None,
                    "weeks_at_delivery": int(data.get("weeks_at_delivery", 0)) if data.get("weeks_at_delivery") else None,
                    "healthy_delivery": data.get("healthy_delivery", ""),
                    "rehospitalization": data.get("rehospitalization", "")
                },
                # Extract children details from the received JSON
                "shelter_children_details" : {
                    "child_name": data.get("child_name", ""),
                    "birthdate": data.get("birthdate", ""),
                    "age": int(data.get("age", 0)) if data.get("age") else None,
                    "grade_level": data.get("grade_level", ""),
                    "trauma_programming_hours": int(data.get("trauma_programming_hours", 0)) if data.get("trauma_programming_hours") else None
                },
                # Extract housing details from the received JSON
                "housing_details" : {
                    "length_stay_shelter": data.get("length_stay_shelter", ""),
                    "reason_leaving_shelter": data.get("reason_leaving_shelter", ""),
                    "moved_to_transitional_housing": data.get("moved_to_transitional_housing", ""),
                    "length_stay_transitional_housing": data.get("length_stay_transitional_housing", ""),
                    "housing_voucher_recipient": data.get("housing_voucher_recipient", ""),
                    "case_management_assistance": data.get("case_management_assistance", "")
                },
                # Extract women served details from the received JSON
                "women_served_details" : {
                    "women_accepted_intake": int(data.get("women_accepted_intake", 0)) if data.get("women_accepted_intake") else None,
                    "incoming_calls_shelter": int(data.get("incoming_calls_shelter", 0)) if data.get("incoming_calls_shelter") else None,
                    "calls_seeking_shelter_women": int(data.get("calls_seeking_shelter_women", 0)) if data.get("calls_seeking_shelter_women") else None,
                    "calls_seeking_shelter_pregnant": int(data.get("calls_seeking_shelter_pregnant", 0)) if data.get("calls_seeking_shelter_pregnant") else None,
                    "pregnant_women_turned_away": int(data.get("pregnant_women_turned_away", 0)) if data.get("pregnant_women_turned_away") else None,
                    "pregnant_women_turned_away_reason": data.get("pregnant_women_turned_away_reason", ""),
                    
                    "community_outreach_activities": int(data.get("community_outreach_activities", 0)) if data.get("community_outreach_activities") else None,
                    "referrals_other_agencies": int(data.get("referrals_other_agencies", 0)) if data.get("referrals_other_agencies") else None,
                    
                    "moved_from_maternity_to_apartments": int(data.get("moved_from_maternity_to_apartments", 0)) if data.get("moved_from_maternity_to_apartments") else None,
                    "moved_to_aftercare_program": int(data.get("moved_to_aftercare_program", 0)) if data.get("moved_to_aftercare_program") else None,
                    "aftercare_program_details": data.get("aftercare_program_details", "")
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

    


@app.route('/client_details', methods=['GET', 'POST'])
def client_details():
    error_message = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['authenticated'] = True
            session.permanent = True  # Make the session permanent
            return redirect(url_for('client_details'))
        else:
            error_message = "Incorrect password. Access denied."
            logging.warning("Attempted access with incorrect password.")
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Client Details</title>
                    <!-- Bootstrap CSS -->
                    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        .center-form {
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }
                        .form-container {
                            width: 300px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container center-form">
                        <div class="form-container">
                            <form action="/client_details" method="POST" id="passwordForm">
                                <div class="form-group">
                                <h5> Please Re-enter the password </h5>
                                <br>
                            
                                    <label for="password">Password</label>
                                    <input type="password" class="form-control" name="password" id="password" placeholder="Enter password" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block">View Client Data</button>
                            </form>
                            {% if error_message %}
                                <p class="text-danger text-center mt-3">{{ error_message }}</p>
                            {% endif %}
                        </div>
                    </div>
                    <!-- Bootstrap JS, Popper.js, and jQuery -->
                    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
                </body>
                </html>
            ''', error_message=error_message)
    
    if session.get('authenticated'):
        try:
            clients = mongo.db.user_details.find()
            clients_list = list(clients)  # Convert to list to pass to the template
            logging.debug(f"Retrieved {len(clients_list)} clients")
            return render_template('client_details.html', clients=clients_list)
        except Exception as e:
            logging.error(f"Error retrieving client details: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Client Details</title>
                <!-- Bootstrap CSS -->
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    .center-form {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .form-container {
                        width: 300px;
                    }
                </style>
            </head>
            <body>
                <div class="container center-form">
                    <div class="form-container">
                        <form action="/client_details" method="POST" id="passwordForm">
                            <div class="form-group">
                           
                                <label for="password">Password</label>
                                <input type="password" class="form-control" name="password" id="password" placeholder="Enter password" required>
                            </div>
                            <button type="submit" class="btn btn-primary btn-block">View Client Data</button>
                        </form>
                    </div>
                </div>
                <!-- Bootstrap JS, Popper.js, and jQuery -->
                <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            </body>
            </html>
        ''')


        
        
@app.route('/delete_client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        obj_id = ObjectId(client_id)
        
        # Fetch the client details
        client_details = mongo.db.user_details.find_one({'_id': obj_id})
        
        if client_details is None:
            return jsonify({'error': 'Client not found'}), 404
        
        # Insert the details into the archive collection
        archive_result = mongo.db.archive.insert_one(client_details)
        
        if archive_result.inserted_id:
            # Delete the client from the original collection
            result = mongo.db.user_details.delete_one({'_id': obj_id})
            
            if result.deleted_count == 1:
                logging.debug(f"Deleted client with id: {client_id} and archived details")
                return jsonify({'message': 'Client deleted and archived successfully'}), 200
            else:
                return jsonify({'error': 'Client deletion failed'}), 500
        else:
            return jsonify({'error': 'Archiving client details failed'}), 500
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
