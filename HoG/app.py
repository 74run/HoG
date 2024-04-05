from flask import Flask, request, render_template, jsonify, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%4074run54I@localhost/hog' # Replace with your MySQL connection details
db = SQLAlchemy(app)



class ClientDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

@app.route('/submit_form', methods=['POST', "GET"])
def submit_form():
    if request.method == "POST":
        data = request.form
        client_details = ClientDetails(
            name=data['name'],
            address=data['address'],
            zip_code=data['zip'],
            phone=data['phone']
        )
        
        print(client_details)
        db.session.add(client_details)
        db.session.commit()
        return jsonify({'message': 'Form submitted successfully'}), 200

    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
   