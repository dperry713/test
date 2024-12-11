import unittest
import json
from app import app, db, Sum

class TestSumAPI(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_add_sum(self):
        response = self.client.post('/sum',
                                  data=json.dumps({'num1': 2, 'num2': 2}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 4)
    
    def test_get_sums_by_result(self):
        # Add some test data
        with app.app_context():
            sums = [
                Sum(num1=2, num2=2, result=4),
                Sum(num1=3, num2=1, result=4),
                Sum(num1=1, num2=2, result=3)
            ]
            db.session.add_all(sums)
            db.session.commit()
        
        # Test getting sums with result = 4
        response = self.client.get('/sum/result/4')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertTrue(all(sum['result'] == 4 for sum in data))
    
    def test_get_sums_by_result_not_found(self):
        # Test with a result that doesn't exist
        response = self.client.get('/sum/result/999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()
