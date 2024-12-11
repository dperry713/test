from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sums.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Integer, nullable=False)
    num2 = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'num1': self.num1,
            'num2': self.num2,
            'result': self.result
        }

@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.get_json()
    
    if not data or 'num1' not in data or 'num2' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        num1 = int(data['num1'])
        num2 = int(data['num2'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Numbers must be integers'}), 400
    
    result = num1 + num2
    new_sum = Sum(num1=num1, num2=num2, result=result)
    
    db.session.add(new_sum)
    db.session.commit()
    
    return jsonify(new_sum.to_dict()), 201

@app.route('/sum', methods=['GET'])
def get_all_sums():
    sums = Sum.query.all()
    return jsonify([sum.to_dict() for sum in sums])

@app.route('/sum/result/<int:result>', methods=['GET'])
def get_sums_by_result(result):
    sums = Sum.query.filter_by(result=result).all()
    return jsonify([sum.to_dict() for sum in sums])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
