from flask import Flask, request, render_template, jsonify, render_template_string, session, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime, timedelta

import logging
import uuid

import random
import string


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


def generate_user_id():
    return ''.join(random.choices(string.digits, k=6))

def generate_unique_user_id():
    while True:
        user_id = generate_user_id()
        if not mongo.db.users.find_one({"user_id": user_id}):
            return user_id


        
        
@app.route('/')
def index():
    return render_template('forms.html')


@app.route('/demographics_form1')
def demographics_form():
    return render_template('demographics.html')

@app.route('/demographics_form2')
def demo2_form():
    user_id = request.args.get('user_id')
    user = mongo.db.users.find_one({'user_id': user_id}, {'_id': 0, 'demographics_form1.name': 1, 'demographics_form1.birthdate': 1})

    if user:
        user_info = user.get('demographics_form1', {})
        name = user_info.get('name')
        birthdate = user_info.get('birthdate')
        if isinstance(birthdate, datetime):
            birthdate = birthdate.strftime('%Y-%m-%d')
    else:
        name = None
        birthdate = None

    return render_template('demo2.html', user_id=user_id, name=name, birthdate=birthdate)


@app.route('/child_demogrphics_form')
def child_demo_form():
    return render_template('child_demo.html')

@app.route('/infants_demographics_form')
def Infants_demo_form():
    return render_template('Infant_demo.html')

@app.route('/exit_info_form')
def exit_info_form():
    return render_template('exit_info.html')


@app.route('/women_served_details')
def women_served_details_form():
    return render_template('women_served_details.html')


@app.route('/validate_user', methods=['POST'])
def validate_user():
    data = request.json
    user_id = data.get('userId')

    # Find the user in the database
    user = mongo.db.users.find_one({'user_id': user_id}, {'_id': 0, 'demographics_form1.name': 1, 'demographics_form1.birthdate': 1})

    if user:
        user_info = user.get('demographics_form1', {})
        # Convert birthdate to string format if it's a datetime object
        birthdate = user_info.get('birthdate')
        if isinstance(birthdate, datetime):
            user_info['birthdate'] = birthdate.strftime('%Y-%m-%d')
        return jsonify({'valid': True, 'user_info': user_info}), 200
    else:
        return jsonify({'valid': False}), 404



# Form Submission Routes
@app.route('/submit_demographics_form1', methods=['POST'])
def submit_demographics_form1():
    data = request.form
    
    
    try:
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
            
        user_id = generate_unique_user_id()  # Generate a unique identifier for the user
        demographics_data = {
                    "user_id": user_id,
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
                    "veteran_status": data.get('veteran_status', ''),
                    "highbp": data.get("highbp", ""),
                    "diabetes": data.get("diabetes", ""),
                    "heartdisease": data.get("heartdisease", ""),
                    "livebirths": data.get("livebirths", ""),
                    "miscarriages": int(data.get("miscarriages", 0)) if data.get("miscarriages") else None,
                    "diagdisabilty": data.get("diagdisabilty", ""),
        
            
            }
    
        mongo.db.users.update_one(
        {"user_id": user_id},
        {"$set": {"demographics_form1": demographics_data}},
        upsert=True
        )
        return jsonify({'message': 'Demographics form 1 submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting demographics form 1: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_demographics_form2', methods=['POST'])
def submit_demographics_form2():
    data = request.form
    
    user_id = data.get('user_id')

    # Validate the user_id by checking if the user exists in the database
    user = mongo.db.users.find_one({'user_id': user_id})
    if not user:
        return jsonify({'error': 'User ID not found.'}), 404
    try:
        demo_data = {
            "user_id": user_id,
            "rehosp": data.get("rehosp", ""),
            "doula": data.get("doula", ""),
            "highriskpreg": data.get("highriskpreg", ""),
            "vaginalbirth": data.get("vaginalbirth", "")
            # Add your specific form fields here
        }
        mongo.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"form2_data": demo_data}}
        )
        return jsonify({'message': 'Demographics form 2 submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting demographics form 2: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_child_demographics', methods=['POST'])
def submit_child_demographics():
    data = request.form
    try:
        child_demo_details = {
            "child_name": data.get("child_name", ""),
            "birthdate": data.get("birthdate", ""),
            "age": int(data.get("age", 0)) if data.get("age") else None,
            "grade_level": data.get("grade_level", ""),
            "trauma_programming_hours": int(data.get("trauma_programming_hours", 0)) if data.get("trauma_programming_hours") else None
        }
        mongo.db.child_demographics.insert_one(child_demo_details)
        return jsonify({'message': 'Child demographics submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting child demographics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_infants_demographics', methods=['POST'])
def submit_infants_demographics():
    data = request.form
    try:
        infant_details = {
            "infant_name": data.get("infant_name", ""),
            "birthdate": data.get("birthdate", ""),
            "birth_weight": float(data.get("birth_weight", 0)) if data.get("birth_weight") else None,
            "weeks_at_delivery": int(data.get("weeks_at_delivery", 0)) if data.get("weeks_at_delivery") else None,
            "healthy_delivery": data.get("healthy_delivery", ""),
            "rehospitalization": data.get("rehospitalization", "")
        }
        mongo.db.infant_demographics.insert_one(infant_details)
        return jsonify({'message': 'Infants demographics submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting infants demographics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_exit_info', methods=['POST'])
def submit_exit_info():
    data = request.form
    try:
        exit_info = {
            "length_stay_shelter": data.get("length_stay_shelter", ""),
            "reason_leaving_shelter": data.get("reason_leaving_shelter", ""),
            "moved_to_transitional_housing": data.get("moved_to_transitional_housing", ""),
            "length_stay_transitional_housing": data.get("length_stay_transitional_housing", ""),
            "housing_voucher_recipient": data.get("housing_voucher_recipient", ""),
            "case_management_assistance": data.get("case_management_assistance", "")
            # Add your specific form fields here
        }
        mongo.db.exit_info.insert_one(exit_info)
        return jsonify({'message': 'Exit information submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting exit information: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_women_served_details', methods=['POST'])
def submit_women_served_details():
    data = request.form
    try:
        women_details = {
            # Add your specific form fields here
        }
        mongo.db.women_served_details.insert_one(women_details)
        return jsonify({'message': 'Women served details submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting women served details: {e}")
        return jsonify({'error': str(e)}), 500
    
    
    
    
    
    
    
    


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
