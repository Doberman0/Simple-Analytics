import unittest
import requests
import json

# Import the app itself
from app import app

class Tests(unittest.TestCase):
	def test_sanity_check(self):
		expected_response = {
		  "Average Total in a day": 1243008.83, 
		  "Average amount of commission for the day": 2314804.1, 
		  "Average discount": 0.13, 
		  "Total commission for the day": 20833236.94, 
		  "Total discount": 12626637.36, 
		  "Total promotional commission": 1341854.2, 
		  "total number of customers who ordered": 9, 
		  "total_num_items": 121
		}

		response = requests.get('http://localhost:5000/?date=2019-08-01')

		self.assertEqual(json.loads(response.content), expected_response)

	def test_not_in_date(self):
		expected_response = {
		  "Average Total in a day": 0, 
		  "Average amount of commission for the day": 0, 
		  "Average discount": 0, 
		  "Total commission for the day": 0, 
		  "Total discount": 0, 
		  "Total promotional commission": 0, 
		  "total number of customers who ordered": 0, 
		  "total_num_items": 0
		}

		response = requests.get('http://localhost:5000/?date=2018-08-01')

		self.assertEqual(json.loads(response.content), expected_response)

	def test_invalid_date(self):
		expected_response = {
  		"error": "abc is not valid date in the format YYYY-MM-DD"
		}

		response = requests.get('http://localhost:5000/?date=abc')

		self.assertEqual(json.loads(response.content), expected_response)

	def test_date_not_provided(self):
		expected_response = {
		  "Average Total in a day": 0, 
		  "Average amount of commission for the day": 0, 
		  "Average discount": 0, 
		  "Total commission for the day": 0, 
		  "Total discount": 0, 
		  "Total promotional commission": 0, 
		  "total number of customers who ordered": 0, 
		  "total_num_items": 0
		}

		response = requests.get('http://localhost:5000/')

		self.assertEqual(json.loads(response.content), expected_response)

if __name__ == "__main__":
    unittest.main()