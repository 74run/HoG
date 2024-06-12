from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://TJ562:password@TJ562.mysql.pythonanywhere-services.com/TJ562$hog'
db = SQLAlchemy(app)

class ClientDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    birthdate = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    race = db.Column(db.String(100))
    ethnicity = db.Column(db.String(100))
    marital_status = db.Column(db.String(50))
    length_stay_previous_address = db.Column(db.String(100))
    country_of_origin = db.Column(db.String(100))
    times_in_shelter = db.Column(db.Integer)
    length_stay_previous_shelter = db.Column(db.String(100))
    number_of_children = db.Column(db.Integer)
    education_level = db.Column(db.String(100))
    employment_status = db.Column(db.String(100))
    income_amount_intake = db.Column(db.Float)
    income_source_intake = db.Column(db.String(100))
    income_amount_exit = db.Column(db.Float)
    income_1_year_exit = db.Column(db.Float)
    weeks_pregnant = db.Column(db.Integer)
    prenatal_care_prior_intake = db.Column(db.String(100))
    father_involvement = db.Column(db.String(3))
    father_education_level = db.Column(db.String(100))
    father_occupation = db.Column(db.String(100))
    father_income = db.Column(db.Float)
    domestic_violence_survivor = db.Column(db.String(3))
    veteran_status = db.Column(db.String(3))

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form
            birthdate_str = data['birthdate']
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            client_details = ClientDetails(
                name=data['name'],
                address=data['address'],
                zip_code=data['zip'],
                phone=data['phone'],
                birthdate=birthdate,
                age=int(data['age']),
                sex=data['sex'],
                race=data['race'],
                ethnicity=data['ethnicity'],
                marital_status=data['marital_status'],
                length_stay_previous_address=data['length_stay_previous_address'],
                country_of_origin=data['country_of_origin'],
                times_in_shelter=int(data['times_in_shelter']),
                length_stay_previous_shelter=data['length_stay_previous_shelter'],
                number_of_children=int(data['number_of_children']),
                education_level=data['education_level'],
                employment_status=data['employment_status'],
                income_amount_intake=float(data['income_amount_intake']),
                income_source_intake=data['income_source_intake'],
                income_amount_exit=float(data['income_amount_exit']),
                income_1_year_exit=float(data['income_1_year_exit']),
                weeks_pregnant=int(data['weeks_pregnant']),
                prenatal_care_prior_intake=data['prenatal_care_prior_intake'],
                father_involvement=data['father_involvement'],
                father_education_level=data['father_education_level'],
                father_occupation=data['father_occupation'],
                father_income=float(data['father_income']),
                domestic_violence_survivor=data['domestic_violence_survivor'],
                veteran_status=data['veteran_status']
            )

            db.session.add(client_details)
            db.session.commit()
            return jsonify({'message': 'Form submitted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client_details')
def client_details():
    clients = ClientDetails.query.all()
    return render_template('client_details.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
