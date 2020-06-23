#!flask/bin/python3
from flask import Flask
from flask import request
from flask import jsonify
import datetime
import pandas as pd # Using pandas as its efficient

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

@app.route('/')
def index():
	try:
		date = toDate(request.args.get('date', default = datetime.date.today().isoformat()))
	except ValueError as ex:
		return jsonify({'error': str(ex)}), 400   # jsonify, if this is a json api
	# Total number of items sold that day
	order_ids = set()
	unique_customers_set = set() # Total number of customers that made an order that day
	total_discount = 0
	number_of_discounts = 0
	total_amount = 0 # Total amount ordered that day (is it per item?)
	# Get all the orders placed that day
	orders_csv = pd.read_csv('data/orders.csv')
	for row in range(orders_csv.shape[0]): 
		if orders_csv.iloc[row]['created_at'][:10] == str(date):
			order_ids.add(orders_csv.iloc[row]['id'])
			unique_customers_set.add(orders_csv.iloc[row]['customer_id'])
	# Getting the numbers of items sold that day
	total_num_items = 0
	order_lines_csv = pd.read_csv('data/order_lines.csv')
	for row in range(order_lines_csv.shape[0]):
		if order_lines_csv.iloc[row]['order_id'] in order_ids:
			total_num_items += 1
			total_discount += float(order_lines_csv.iloc[row]['discounted_amount'])
			number_of_discounts += 1
	return jsonify({'total_num_items': str(total_num_items), 'total number of customers who ordered': len(unique_customers_set), 'Total discount': total_discount, 'Average discount': total_discount/number_of_discounts}), 200

if __name__ == '__main__':
    app.run(debug=True)