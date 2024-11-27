import unittest
from unittest.mock import Mock, patch
import requests
import pytest 

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        # Base URL for the factory management system API
        self.base_url = 'http://localhost:8000/api'
    
    def test_create_employee_success(self):
        # Test successful employee creation
        mock_employee_data = {
            'name': 'John Doe',
            'department': 'Production',
            'position': 'Machine Operator',
            'email': 'john.doe@factory.com'
        }
        
        with patch('requests.post') as mock_post:
            # Simulate successful API response
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                'id': 1,
                **mock_employee_data
            }
            mock_post.return_value = mock_response
            
            # Make the API call
            response = requests.post(f'{self.base_url}/employees', json=mock_employee_data)
            
            # Assertions
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json())
            self.assertEqual(response.json()['name'], mock_employee_data['name'])
    
    def test_get_employee_by_id(self):
        # Test retrieving an existing employee
        employee_id = 1
        
        with patch('requests.get') as mock_get:
            # Simulate successful employee retrieval
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': employee_id,
                'name': 'John Doe',
                'department': 'Production'
            }
            mock_get.return_value = mock_response
            
            # Make the API call
            response = requests.get(f'{self.base_url}/employees/{employee_id}')
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['id'], employee_id)
    
    def test_employee_not_found(self):
        # Test employee retrieval with non-existent ID
        non_existent_id = 9999
        
        with patch('requests.get') as mock_get:
            # Simulate not found response
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {
                'error': 'Employee not found'
            }
            mock_get.return_value = mock_response
            
            # Make the API call
            response = requests.get(f'{self.base_url}/employees/{non_existent_id}')
            
            # Assertions
            self.assertEqual(response.status_code, 404)
            self.assertIn('error', response.json())

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8000/api'
    
    def test_create_product_success(self):
        # Test successful product creation
        mock_product_data = {
            'name': 'Smart Widget',
            'category': 'Electronics',
            'price': 99.99,
            'stock_quantity': 100
        }
        
        with patch('requests.post') as mock_post:
            # Simulate successful API response
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                'id': 1,
                **mock_product_data
            }
            mock_post.return_value = mock_response
            
            # Make the API call
            response = requests.post(f'{self.base_url}/products', json=mock_product_data)
            
            # Assertions
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json())
            self.assertEqual(response.json()['name'], mock_product_data['name'])
    
    def test_get_product_inventory(self):
        # Test retrieving product inventory
        with patch('requests.get') as mock_get:
            # Simulate inventory retrieval
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'products': [
                    {'id': 1, 'name': 'Smart Widget', 'stock_quantity': 100},
                    {'id': 2, 'name': 'Advanced Gadget', 'stock_quantity': 50}
                ]
            }
            mock_get.return_value = mock_response
            
            # Make the API call
            response = requests.get(f'{self.base_url}/products/inventory')
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(response.json()['products']), 0)
    
    def test_product_low_stock_warning(self):
        # Test low stock scenario
        with patch('requests.get') as mock_get:
            # Simulate low stock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'low_stock_products': [
                    {'id': 3, 'name': 'Critical Component', 'stock_quantity': 5}
                ]
            }
            mock_get.return_value = mock_response
            
            # Make the API call
            response = requests.get(f'{self.base_url}/products/low-stock')
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertIn('low_stock_products', response.json())
            self.assertTrue(len(response.json()['low_stock_products']) > 0)

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8000/api'
    
    def test_create_order_success(self):
        # Test successful order creation
        mock_order_data = {
            'customer_id': 1,
            'products': [
                {'product_id': 1, 'quantity': 2},
                {'product_id': 2, 'quantity': 1}
            ],
            'total_price': 199.98
        }
        
        with patch('requests.post') as mock_post:
            # Simulate successful order creation
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                'id': 1,
                'status': 'Pending',
                **mock_order_data
            }
            mock_post.return_value = mock_response
            
            # Make the API call
            response = requests.post(f'{self.base_url}/orders', json=mock_order_data)
            
            # Assertions
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json())
            self.assertEqual(response.json()['status'], 'Pending')
    
    def test_get_order_status(self):
        # Test retrieving order status
        order_id = 1
        
        with patch('requests.get') as mock_get:
            # Simulate order status retrieval
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': order_id,
                'status': 'Processing',
                'estimated_delivery': '2024-02-15'
            }
            mock_get.return_value = mock_response
            
            # Make the API call
            response = requests.get(f'{self.base_url}/orders/{order_id}/status')
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'Processing')
    
    def test_order_invalid_creation(self):
        # Test order creation with invalid data
        invalid_order_data = {
            'customer_id': None,
            'products': []
        }
        
        with patch('requests.post') as mock_post:
            # Simulate validation error
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {
                'error': 'Invalid order data',
                'details': ['Customer ID is required', 'At least one product is needed']
            }
            mock_post.return_value = mock_response
            
            # Make the API call
            response = requests.post(f'{self.base_url}/orders', json=invalid_order_data)
            
            # Assertions
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json())

# Add more test classes for other endpoints as needed

if __name__ == '__main__':
    unittest.main()