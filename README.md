# Simple-Analytics
A simple analytics REST API created for Suade's technical challenge. Based on 6 csv files, we attempt to efficiently iterate through them appropriately to find the data for the following:

-Total number of items sold that day
-Total number of customers that made an order that day
-Total amount of discount on that day
-Average discount rate applied to the items sold that day
-Average order total for that day
-Total amount of commissions generated that day
-Average amound of commisions generated that day
-Total amount of commisions earned per promotion that day

And return this information as a report.

A REST API was chosen as you could potential extend the application to further utilise the data generated from this API. This is also why the response is simply a JSON response as opposed to an autogenerate analytics dashboard/report.

# Dependecies
This application was written and tested on Ubuntu 18.04. This REST API depends on the following Python-3.6 modules:
- flask
- pandas

# Running the application
After you have clones the project using 
> git clone https://github.com/Doberman0/bpdts-test-app.git

Run the the following bash script to install dependencies
> chmod a+x install_dependencies.sh
> ./install_dependencies.sh 

Create a server on localhost using first changing the execution permissions of app.py by:
> chmod a+x app.py

And then actually running the application:
> ./app.py

You can send commands to the API via writing commands in the terminal. E.g.
> http://localhost:5000/?date=2019-08-01

Note that if you don't enter a date, the application will default to the current date.

# Testing
Run unit tests created using the command:
> python3 -m unittest tests.tests