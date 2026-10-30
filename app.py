#imports and setup stuff
import pygal 
from pygal.style import *
import lxml
from flask import Flask, render_template, request, flash, url_for, redirect
from datetime import datetime
import os
from dotenv import load_dotenv

#get the api key from .env files that are .gitignore (add the api code from README and put into your own .env folder)
load_dotenv()
API_KEY = os.getenv("API_KEY")

#used to generate the chart in the html page
app = Flask(__name__)

#functions from Alpha Vantage Website 
TIME_SERIES_OPTIONS = {
    "1": ("TIME_SERIES_INTRADAY", "Time Series (60min)"),
    "2": ("TIME_SERIES_DAILY", "Time Series (Daily)"),
    "3": ("TIME_SERIES_WEEKLY", "Weekly Time Series)"),
    "4": ("TIME_SERIES_MONTHLY", "Monthly Time Series")
}


#USER INPUTS
#ask the user to enter the stock symbol for the company they want data for
    #only letters, has to be lest than 7
def get_stock_symbol():
    check_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        user_input = input("\nEnter the stock symbol you are looking for: ").strip()
        user_symbol_choice = user_input.upper()

        is_letters = True
        for i in user_symbol_choice:
            if i not in check_letters:
                all_letters = False

        if len(user_symbol_choice) >= 7 or len(user_symbol_choice) == 0:
            print("Stock symbols must be between 0-7 letters long.")
        elif all_letters == False:
            print("Stock symbols can only contain letters.")
        else:
            return user_symbol_choice

#ask the user for the chart type they would like
def get_chart_type():
    while True:
        print("Chart Types\n-----------------")
        print("1. Bar")
        print("2. Line")
        user_input = input("\nEnter the chart type you want (1,2): ")

        if user_input == "1":
            return None
            #return bar chart with pygal
        elif user_input == "2":
            return None
            #return line chart with pygal
        else:
            print("\nPlease enter either 1 or 2.\n")

#ask the user for the time series function they want the api to use
def get_time_series():
    while True:
        #menu choices
        print("\nSelect the time series for the chart you wish to generate\n---------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")

        user_input_timeseries = input("Enter a choice 1-4: ")
        if user_input_timeseries not in [1,2,3,4]:
            print("\nPlease enter 1,2,3, or 4.")
        else:
            return user_input_timeseries

#ask the user for the beginning date in YYYY-MM-DD format
#make sure the date is in the right format
def get_date_validate(user_input):
    while True:
        user_date_input = input(user_input).strip()
        try:
            validated_user_date = datetime.strptime(user_date_input, "%Y-%m-%d")
            return validated_user_date.date()
        except ValueError:
            print("Please enter a valid date in the YYYY-MM-DD format.")

#get the start date from user 
def get_start_date():
    start_date = get_date_validate("Enter the start date in YYYY-MM-DD format: ")
    return get_end_date(start_date)

#ask the user for the end date in YYYY-MM-DD format
def get_end_date(start_date):
    while True:
        end_date = get_date_validate("Enter the end date in YYYY-MM-DD format: ")
        #the end date should not be before the begin date
        if end_date >= start_date:
            return end_date
        else:
            print("The end date cannot be before the start date.")

#api stuff 
#gets the data using API key from Alpha Vantage Website
def get_api_data(symbol_choice, time_series_choice):
    function_name, data_key = TIME_SERIES_OPTIONS[time_series_choice]

    search_parameters = {"function": function_name, "symbol": symbol_choice, "apikey": API_KEY}

    if time_series_choice == "1":
        search_parameters["interval"] = "60min"

    




#Generate a graph and open the user's default browser




#main function 
def main():
    print("Stock Date Visualizer\n------------------------")

    if not API_KEY:
        print("Please make sure you have a valid API key in the .env file")
        return 

    while True:
        symbol_choice = get_stock_symbol()
        chart_type = get_chart_type()
        time_series_choice = get_time_series()
        start_date = get_start_date()
        end_date = get_start_date(start_date)
        time_series = get_api_data(symbol_choice, time_series_choice)

        
        


main()