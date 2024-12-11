Factory Management System Test Suite
This test suite validates the functionality of the Factory Management System API endpoints using Python's unittest framework.

Test Coverage
The test suite covers three main areas:

1. Employee Management
Create new employees
Retrieve employee details
Handle non-existent employee scenarios
2. Product Management
Create new products
Check inventory levels
Monitor low stock warnings
3. Order Management
Create new orders
Track order status
Validate order data
Running the Tests
To run the test suite:

python -m pytest tester/management_test.py
python -m unittest tester/management_test.py
Test Configuration
Base API URL: http://localhost:8000/api
The tests use mocking to simulate API responses
Each test class focuses on a specific domain (Employees, Products, Orders)
Test Classes
TestEmployeeEndpoints

Tests employee creation and retrieval
Validates API responses and error handling
TestProductEndpoints

Tests product management functionality
Validates inventory tracking and stock alerts
TestOrderEndpoints

Tests order processing workflows
Validates order status tracking and error cases
Dependencies
Python 3.x
requests
pytest
unittest
unittest.mock
Adding New Tests
To extend the test suite:

Create a new test class for your domain
Follow the existing pattern of using setUp() for common initialization
Use descriptive test method names
Implement proper assertions and mocking
Best Practices
Each test focuses on a single functionality
Mock external API calls to ensure reliable testing
Include both success and failure scenarios
Use clear assertions to validate expected behavior
