import unittest
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory database
datastore = []

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    # Validate the data
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new record
    record = {
        'id': len(datastore) + 1,
        'name': data['name'],
        'email': data['email']
    }
    datastore.append(record)

    return jsonify(record), 201

class TestCreate(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_create(self):
        data = {'name': 'John Doe', 'email': 'johndoe@example.com'}
        response = self.client.post('/create', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')
        self.assertEqual(response.json['email'], 'johndoe@example.com')

    def test_create_invalid_data(self):
        data = {'foo': 'bar'}
        response = self.client.post('/create', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Missing required fields')

    def test_create_empty_data(self):
        response = self.client.post('/create', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Missing required fields')

if __name__ == '__main__':
    unittest.main()