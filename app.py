#!flask/bin/python3
from flask import Flask
from flask import request
from flask import jsonify
import datetime
import pandas as pd # Using pandas as its efficient
from typing import List
from typing import Dict 


app = Flask(__name__)

def toDate(date_string): 
	'''
	Strips the what you've entered for the date to it's YYYY-MM-DD format 
	(E.g. getting rid of time)
	'''
	try:
		return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
	except ValueError:
		raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))

def totalOrderForDay(orders_in_a_day: Dict[str, List[float]]) -> float:
	'''
	orders_in_a_day is a dictionary structured as such: 
	{order_id: [total_amount per order line associated with order_id]}
	Returns {order_id: total amount per order_id}
	'''
	return {order_id:sum(orders_in_a_day[order_id]) for order_id in orders_in_a_day}

def calculateAverageOrderTotalForDay(orders_in_a_day: Dict[str, List[float]]) -> float:
	'''
	orders_in_a_day is a dictionary structured as such: 
	{order_id: [total amount everything in that order]}
	'''
	average_totals = [sum(orders_in_a_day[order_id])/len(orders_in_a_day[order_id]) for order_id in orders_in_a_day]
	return sum(average_totals)/len(average_totals)

@app.route('/', methods=['GET'])
def controller():
	'''
	This function is a singleton (?) function which gets all the necessary data
	from the CSV files/data given and returns a json object containing all the 
	necessary information.
	'''

	# Parse the date from the url
	try:
		date = toDate(request.args.get('date', default = datetime.date.today().isoformat()))
	except ValueError as ex:
		return jsonify({'error': str(ex)}), 400   # jsonify, if this is a json api
	
	# Variables to store the necessary information
	# Using Python's in built types as the CSV files are relatively small
	order_ids = set() # ids of orders taken on the day
	unique_customers_set = set() # Total number of customers that made an order that day
	total_discount = 0
	number_of_discounts = 0 # same as total number of items ordered
	total_discount_rate = 0 # Total amount ordered that day (is it per item?)
	#To calculate the total amount of commission 
	orders_vendors = {} # Key:order_id, val:[vendor_id]
	total_commission = 0
	
	# Get all the orders placed that day
	orders_csv = pd.read_csv('data/orders.csv')
	for row in range(orders_csv.shape[0]): 
		if orders_csv.iloc[row]['created_at'][:10] == str(date):
			order_ids.add(orders_csv.iloc[row]['id'])
			unique_customers_set.add(orders_csv.iloc[row]['customer_id'])
			# To check commissions
			if orders_csv.iloc[row]['id'] not in orders_vendors:
				orders_vendors[orders_csv.iloc[row]['id']] = orders_csv.iloc[row]['vendor_id']
			else:
				orders_vendors[orders_csv.iloc[row]['id']] += orders_csv.iloc[row]['vendor_id']

	# Get the commission rates
	commissions_csv = pd.read_csv('data/commissions.csv')
	commission_rates = [0 for _ in range(10)] # index is the vendor_id-1
	for row in range(commissions_csv.shape[0]):
		if commissions_csv.iloc[row]['date'] == str(date):
			commission_rates[commissions_csv.iloc[row]['vendor_id'] - 1] = commissions_csv.iloc[row]['rate']  

	# Getting the numbers of items sold that day
	total_num_items = 0
	order_lines_csv = pd.read_csv('data/order_lines.csv')
	orders_in_a_day = {} # Key: order_id, val: list of total orders in the order organising the orders into buckets
	for row in range(order_lines_csv.shape[0]):
		order_id = order_lines_csv.iloc[row]['order_id'] 
		
		if order_id in order_ids:
			total_num_items += 1

			total_discount += float(order_lines_csv.iloc[row]['total_amount']) - float(order_lines_csv.iloc[row]['discounted_amount'])
			
			total_discount_rate += float(order_lines_csv.iloc[row]['discount_rate'])
			
			number_of_discounts += 1
			
			# Now, we bucket the orders by adding them to orders_in_a_day
			row_total_amount = [float(order_lines_csv.iloc[row]['total_amount'])]
			if order_id not in orders_in_a_day:
				orders_in_a_day[order_id] = row_total_amount
			else:
				orders_in_a_day[order_id] = orders_in_a_day[order_id] + row_total_amount

	# Find the total amount of commissions
	# I assume it's total amount (per order) * commission rate
	total_amounts = totalOrderForDay(orders_in_a_day)
	for order_id in total_amounts:
		total_commission += commission_rates[orders_vendors[order_id] - 1] * total_amounts[order_id] 
	
	response = jsonify({'total_num_items': str(total_num_items),
	 'total number of customers who ordered': len(unique_customers_set),
	 'Total discount': total_discount,
	 'Average discount': total_discount_rate/number_of_discounts,
	 'Average Total in a day': calculateAverageOrderTotalForDay(orders_in_a_day),
	 'Total commission for the day': total_commission, 
	 'Average amount of commission for the day': total_commission/len(orders_in_a_day)})
	
	return response, 200

if __name__ == '__main__':
    app.run(debug=True)