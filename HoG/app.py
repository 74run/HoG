from flask import Flask, request, render_template, jsonify, render_template_string, session, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from pymongo import MongoClient

import bcrypt



import logging
import uuid

import random
import string


app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Set the session lifetime to 30 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

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


# Initialize the password if it doesn't exist
if mongo.db.password.count_documents({}) == 0:
    hashed_password = bcrypt.hashpw(b'12345678', bcrypt.gensalt())
    mongo.db.password.insert_one({'password': hashed_password})

@app.route('/')
def index():
    return render_template('forms.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        stored_password = mongo.db.password.find_one({}, {'_id': 0, 'password': 1})['password']

        if bcrypt.checkpw(current_password.encode('utf-8'), stored_password):
            if new_password == confirm_password:
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                mongo.db.password.update_one({}, {'$set': {'password': hashed_new_password}})
                success_message = "Password changed successfully!"
                return render_template('change_password.html', success_message=success_message)
            else:
                error_message = "New passwords do not match."
        else:
            error_message = "Current password is incorrect."
        
        return render_template('change_password.html', error_message=error_message)
    
    return render_template('change_password.html')

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
    return render_template('child_demo.html', name=name, birthdate=birthdate,user_id=user_id)

@app.route('/infants_demographics_form')
def Infants_demo_form():
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
    return render_template('Infant_demo.html',user_id=user_id, name=name, birthdate=birthdate)

@app.route('/exit_info_form')
def exit_info_form():
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
    return render_template('exit_info.html', user_id=user_id, name=name, birthdate=birthdate)


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
                    "typeofdiabetes": data.get("typeofdiabetes", ""),
                    "heartdisease": data.get("heartdisease", ""),
                    "livebirths": data.get("livebirths", ""),
                    "miscarriages": int(data.get("miscarriages", 0)) if data.get("miscarriages") else None,
                    "diagdisabilty": data.get("diagdisabilty", ""),
                    "othermedcondition": data.get("othermedcondition", ""),

            }
    
        mongo.db.users.update_one(
        {"user_id": user_id},
        {"$set": {"demographics_form1": demographics_data}},
        upsert=True
        )
        return redirect(url_for('success', user_id=user_id))

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
            "rehosp": data.get("rehosp", ""),
            "reasonforhosp": data.get("reasonforhosp", ""),
            "date_of_rehosp": data.get("date_of_rehosp", ""),
            "doula": data.get("doula", ""),
            "highriskpreg": data.get("highriskpreg", ""),
            "vaginalbirth": data.get("vaginalbirth", "")
            # Add your specific form fields here
        }

        # Remove empty fields to avoid updating with empty strings
        demo_data = {k: v for k, v in demo_data.items() if v}

        mongo.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"maternity_info": demo_data}}
        )
        return jsonify({'message': 'Demographics form 2 submitted successfully'}), 200
    except Exception as e:
        logging.error(f"Error submitting demographics form 2: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/submit_child_demographics', methods=['POST'])
def submit_child_demographics():
    data = request.form
    user_id = data.get('user_id')

    # Validate the user_id by checking if the user exists in the database
    user = mongo.db.users.find_one({'user_id': user_id})
    if not user:
        return jsonify({'error': 'User ID not found.'}), 404
    
    try:
        # Initialize an empty list to hold child details
        children_details = []

        # Assuming the form sends arrays for each child attribute
        child_names = data.getlist("child_name[]")
        birthdates = data.getlist("birthdate[]")
        ages = data.getlist("age[]")
        grade_levels = data.getlist("grade_level[]")
        trauma_programming_hours = data.getlist("trauma_programming_hours[]")

        # Iterate through each array simultaneously using zip
        for name, birthdate, age, grade_level, hours in zip(child_names, birthdates, ages, grade_levels, trauma_programming_hours):
            child_detail = {
                "child_name": name,
                "birthdate": birthdate,
                "age": int(age) if age else None,
                "grade_level": grade_level,
                "trauma_programming_hours": int(hours) if hours else None
            }
            children_details.append(child_detail)

        # Update the user document with the list of child details
        mongo.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"child_demo_data": children_details}}
        )
        
        return redirect(url_for('success', user_id=user_id))
    except PyMongoError as e:
        logging.error(f"Database error submitting child demographics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_infants_demographics', methods=['POST'])
def submit_infants_demographics():
    data = request.form
    print("the data is:", data)
    user_id = data.get('user_id')

    # Validate the user_id by checking if the user exists in the database
    user = mongo.db.users.find_one({'user_id': user_id})
    if not user:
        return jsonify({'error': 'User ID not found.'}), 404
    
    try:
        infant_details = []

        # Assuming the form sends arrays for each infant attribute
        infant_names = data.getlist("infant_name[]")
        birth_dates = data.getlist("birthdate[]")  # Changed to plural form for consistency
        birth_weights = data.getlist("birth_weight[]")
        weeks_at_delivery = data.getlist("weeks_at_delivery[]")
        healthy_deliveries = data.getlist("healthy_delivery[]")
        medical_concerns_on_birth = data.getlist("medicalconcernsonbirth[]")
        rehospitalizations = data.getlist("rehospitalization[]")

        # Iterate through each array simultaneously using zip
        for name, birth_date, birth_weight, weeks, healthy_delivery, medical_concern, rehospitalization in zip(
            infant_names, birth_dates, birth_weights, weeks_at_delivery, healthy_deliveries, 
            medical_concerns_on_birth, rehospitalizations
        ):
            infant_detail = {
                "infant_name": name,
                "birthdate": birth_date,
                "birth_weight": int(birth_weight) if birth_weight else None,
                "weeks_at_delivery": int(weeks) if weeks else None,
                "healthy_delivery": healthy_delivery,
                "medical_concerns_on_birth": medical_concern,
                "rehospitalization": rehospitalization
            }
            infant_details.append(infant_detail)

        
        # Update the user document with the new infant details
        update_result = mongo.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"infant_data": infant_details}}
        )
        
        return redirect(url_for('success', user_id=user_id))
    except Exception as e:
        logging.error(f"Error submitting infants demographics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_exit_info', methods=['POST'])
def submit_exit_info():
    data = request.form
    user_id = data.get('user_id')

    # Validate the user_id by checking if the user exists in the database
    user = mongo.db.users.find_one({'user_id': user_id})
    if not user:
        return jsonify({'error': 'User ID not found.'}), 404

    try:
        # Extract form data and handle potential missing fields
        exit_info = {
            "length_stay_shelter": data.get("length_stay_shelter", ""),
            "reason_leaving_shelter": data.get("reason_leaving_shelter", ""),
            "doe_from_maternity_shelter": data.get("doe_from_maternity_shelter", ""),
            "wheredidugo": data.get("wheredidugo", ""),
            "moved_to_transitional_housing": data.get("moved_to_transitional_housing", ""),
            "housingreason": data.get("housingreason", ""),
            "commnityhousingaddr": data.get("commnityhousingaddr", ""),
            "length_stay_transitional_housing": data.get("length_stay_transitional_housing", ""),
            "housing_voucher_recipient": data.get("housing_voucher_recipient", ""),
            "case_management_assistance": data.get("case_management_assistance", "")
        }

        # Update the user document with the exit information
        mongo.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"exit_info": exit_info}}
        )

        return redirect(url_for('success', user_id=user_id))

    except Exception as e:
        logging.error(f"Error submitting exit information: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit_women_served_details', methods=['POST'])
def submit_women_served_details():
    data = request.form
    
    try:
        women_details = {
            "women_accepted_intake": int(data.get('women_accepted_intake', 0)),
            "incoming_calls_shelter": int(data.get('incoming_calls_shelter', 0)),
            "calls_seeking_shelter_women": int(data.get('calls_seeking_shelter_women', 0)),
            "calls_seeking_shelter_pregnant": int(data.get('calls_seeking_shelter_pregnant', 0)),
            "pregnant_women_turned_away": int(data.get('pregnant_women_turned_away', 0)),
            "pregnant_women_turned_away_reason": data.get('pregnant_women_turned_away_reason', ''),
            "community_outreach_activities": int(data.get('community_outreach_activities', 0)),
            "referrals_other_agencies": int(data.get('referrals_other_agencies', 0)),
            "moved_from_maternity_to_apartments": int(data.get('moved_from_maternity_to_apartments', 0)),
            "moved_to_aftercare_program": int(data.get('moved_to_aftercare_program', 0))
        }
        mongo.db.women_served_details.insert_one(women_details)
        return redirect(url_for('success'))

    except Exception as e:
        logging.error(f"Error submitting women served details: {e}")
        return jsonify({'error': str(e)}), 500

    
    
    
    


@app.route('/client_details', methods=['GET', 'POST'])
def client_details():
    error_message = None
    if request.method == 'POST':
        password = request.form.get('password')
        stored_password = mongo.db.password.find_one({}, {'_id': 0, 'password': 1})['password']
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            session['authenticated'] = True
            session.permanent = True  # Make the session permanent
            return redirect(url_for('client_details'))
        else:
            error_message = "Incorrect password. Access denied."
            logging.warning("Attempted access with incorrect password.")
    
    if session.get('authenticated'):
        try:
            users = list(mongo.db.users.find({}))
            women_served_details = list(mongo.db.women_served_details.find({}))
            return render_template('client_details.html', users=users, women_served_details=women_served_details)
        except Exception as e:
            logging.error(f"Error retrieving client details: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('password_prompt.html', error_message=error_message)    
        
@app.route('/delete_client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        obj_id = ObjectId(client_id)
        
        # Fetch the client details
        client_details = mongo.db.users.find_one({'_id': obj_id})
        
        if client_details is None:
            return jsonify({'error': 'Client not found'}), 404
        
        # Insert the details into the archive collection
        archive_result = mongo.db.archive.insert_one(client_details)
        
        if archive_result.inserted_id:
            # Delete the client from the original collection
            result = mongo.db.users.delete_one({'_id': obj_id})
            
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

    
# Edit Demographics Form 1
@app.route('/edit_client/<client_id>', methods=['PUT'])
def edit_client(client_id):
    try:
        data = request.json
        
        birthdate = data.get('birthdate', '')
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d') if birthdate else None
        
        update_fields = {
            "demographics_form1.name": data.get('name', ''),
            "demographics_form1.address": data.get('address', ''),
            "demographics_form1.zip_code": data.get('zip', ''),
            "demographics_form1.phone": data.get('phone', ''),
            "demographics_form1.birthdate": birthdate,
            "demographics_form1.age": int(data.get('age', 0)) if data.get('age') else None,
            "demographics_form1.sex": data.get('sex', ''),
            "demographics_form1.race": data.get('race', ''),
            "demographics_form1.ethnicity": data.get('ethnicity', ''),
            "demographics_form1.marital_status": data.get('marital_status', ''),
            "demographics_form1.length_stay_previous_address": data.get('length_stay_previous_address', ''),
            "demographics_form1.country_of_origin": data.get('country_of_origin', ''),
            "demographics_form1.times_in_shelter": int(data.get('times_in_shelter', 0)) if data.get('times_in_shelter') else None,
            "demographics_form1.length_stay_previous_shelter": data.get('length_stay_previous_shelter', ''),
            "demographics_form1.number_of_children": int(data.get('number_of_children', 0)) if data.get('number_of_children') else None,
            "demographics_form1.education_level": data.get('education_level', ''),
            "demographics_form1.employment_status": data.get('employment_status', ''),
            "demographics_form1.income_amount_intake": float(data.get('income_amount_intake', 0)) if data.get('income_amount_intake') else None,
            "demographics_form1.income_source_intake": data.get('income_source_intake', ''),
            "demographics_form1.income_amount_exit": float(data.get('income_amount_exit', 0)) if data.get('income_amount_exit') else None,
            "demographics_form1.income_1_year_exit": float(data.get('income_1_year_exit', 0)) if data.get('income_1_year_exit') else None,
            "demographics_form1.weeks_pregnant": int(data.get('weeks_pregnant', 0)) if data.get('weeks_pregnant') else None,
            "demographics_form1.prenatal_care_prior_intake": data.get('prenatal_care_prior_intake', ''),
            "demographics_form1.father_involvement": data.get('father_involvement', ''),
            "demographics_form1.father_education_level": data.get('father_education_level', ''),
            "demographics_form1.father_occupation": data.get('father_occupation', ''),
            "demographics_form1.father_income": float(data.get('father_income', 0)) if data.get('father_income') else None,
            "demographics_form1.domestic_violence_survivor": data.get('domestic_violence_survivor', ''),
            "demographics_form1.veteran_status": data.get('veteran_status', ''),
            "demographics_form1.highbp": data.get('highbp', ''),
            "demographics_form1.diabetes": data.get('diabetes', ''),
            "demographics_form1.heartdisease": data.get('heartdisease', ''),
            "demographics_form1.livebirths": int(data.get('livebirths', 0)) if data.get('livebirths') else None,
            "demographics_form1.miscarriages": int(data.get('miscarriages', 0)) if data.get('miscarriages') else None,
            "demographics_form1.diagdisabilty": data.get('diagdisabilty', '')
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.users.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Client updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating client: {e}")
        return jsonify({'error': str(e)}), 500


# Edit Maternal Information
@app.route('/edit_maternal_info/<client_id>', methods=['PUT'])
def edit_maternal_info(client_id):
    try:
        data = request.json
        
        update_fields = {
            "form2_data.rehosp": data.get('rehosp', ''),
            "form2_data.doula": data.get('doula', ''),
            "form2_data.highriskpreg": data.get('highriskpreg', ''),
            "form2_data.vaginalbirth": data.get('vaginalbirth', '')
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.users.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Maternal information updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating maternal information: {e}")
        return jsonify({'error': str(e)}), 500

# Edit Infant Information
@app.route('/edit_infant/<client_id>', methods=['PUT'])
def edit_infant(client_id):
    try:
        data = request.json
        
        update_fields = {
            "infant_data.infant_name": data.get('infant_name', ''),
            "infant_data.birthdate": data.get('birthdate', ''),
            "infant_data.birth_weight": float(data.get('birth_weight', 0)) if data.get('birth_weight') else None,
            "infant_data.weeks_at_delivery": int(data.get('weeks_at_delivery', 0)) if data.get('weeks_at_delivery') else None,
            "infant_data.healthy_delivery": data.get('healthy_delivery', ''),
            "infant_data.rehospitalization": data.get('rehospitalization', '')
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.users.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Infant details updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating infant details: {e}")
        return jsonify({'error': str(e)}), 500

# Edit Child Information
@app.route('/edit_child/<client_id>', methods=['PUT'])
def edit_child(client_id):
    try:
        data = request.json
        
        update_fields = {
            "child_demo_data.child_name": data.get('child_name', ''),
            "child_demo_data.birthdate": data.get('birthdate', ''),
            "child_demo_data.age": int(data.get('age', 0)) if data.get('age') else None,
            "child_demo_data.grade_level": data.get('grade_level', ''),
            "child_demo_data.trauma_programming_hours": int(data.get('trauma_programming_hours', 0)) if data.get('trauma_programming_hours') else None
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.users.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Child details updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating child details: {e}")
        return jsonify({'error': str(e)}), 500

# Edit Exit Information
@app.route('/edit_exit_info/<client_id>', methods=['PUT'])
def edit_exit_info(client_id):
    try:
        data = request.json
        
        update_fields = {
            "exit_info.length_stay_shelter": data.get('length_stay_shelter', ''),
            "exit_info.reason_leaving_shelter": data.get('reason_leaving_shelter', ''),
            "exit_info.moved_to_transitional_housing": data.get('moved_to_transitional_housing', ''),
            "exit_info.length_stay_transitional_housing": data.get('length_stay_transitional_housing', ''),
            "exit_info.housing_voucher_recipient": data.get('housing_voucher_recipient', ''),
            "exit_info.case_management_assistance": data.get('case_management_assistance', '')
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.users.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Exit information updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating exit information: {e}")
        return jsonify({'error': str(e)}), 500

# Edit Women Served Details
@app.route('/edit_women_served/<client_id>', methods=['PUT'])
def edit_women_served(client_id):
    try:
        data = request.json
        
        update_fields = {
            "women_served_details.women_accepted_intake": data.get('women_accepted_intake', ''),
            "women_served_details.incoming_calls_shelter": data.get('incoming_calls_shelter', ''),
            "women_served_details.calls_seeking_shelter_women": data.get('calls_seeking_shelter_women', ''),
            "women_served_details.calls_seeking_shelter_pregnant": data.get('calls_seeking_shelter_pregnant', ''),
            "women_served_details.pregnant_women_turned_away": data.get('pregnant_women_turned_away', ''),
            "women_served_details.pregnant_women_turned_away_reason": data.get('pregnant_women_turned_away_reason', ''),
            "women_served_details.community_outreach_activities": data.get('community_outreach_activities', ''),
            "women_served_details.referrals_other_agencies": data.get('referrals_other_agencies', ''),
            "women_served_details.moved_from_maternity_to_apartments": data.get('moved_from_maternity_to_apartments', ''),
            "women_served_details.moved_to_aftercare_program": data.get('moved_to_aftercare_program', ''),
            "women_served_details.aftercare_program_details": data.get('aftercare_program_details', '')
        }
        
        # Remove None values to prevent overwriting fields with None
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        mongo.db.women_served_details.update_one({'_id': ObjectId(client_id)}, {'$set': update_fields})
        return jsonify({'message': 'Women served details updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating women served details: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/success')
def success():
    user_id = request.args.get('user_id')
    return render_template('success.html', user_id=user_id)



if __name__ == '__main__':
    app.run(debug=True)
