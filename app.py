#imports and setup stuff
import pygal 
from pygal.style import *
import requests
import webbrowser
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
    "3": ("TIME_SERIES_WEEKLY", "Weekly Time Series"),
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
                is_letters = False

        if len(user_symbol_choice) > 7 or len(user_symbol_choice) == 0:
            print("Stock symbols must be between 1-7 letters long.")
        elif is_letters == False:
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
            return "bar"
            #return bar chart with pygal
        elif user_input == "2":
            return "line"
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
        if user_input_timeseries not in ["1","2","3","4"]:
            print("\nPlease enter 1, 2,3, or 4.")
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
    return get_date_validate("Enter the start date in YYYY-MM-DD format: ")
    

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

    url = f"https://www.alphavantage.co/query?function={function_name}&symbol={symbol_choice}&apikey={API_KEY}"
    if time_series_choice == "1":
        url += "&interval=60min"

    response = requests.get(url)
    data = response.json()

    if "Error Message" in data:
        print(f"No data was found for the symbol {symbol_choice}. Please check your spelling.")
        return None
    if data_key not in data:
        print("There was an error getting your data from Alpha Vantage. Please try again.")
        return None

    return data[data_key]

def sort_api_data(time_series_choice, start_date, end_date):
    dates = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []

    all_dates = sorted(time_series_choice.keys())

    for date in all_dates:
        date_only = datetime.strptime(date[:10], "%Y-%m-%d").date()

        if date_only >= start_date and date_only <= end_date:
            prices = time_series_choice[date]

            dates.append(date)
            open_values.append(float(prices["1. open"]))
            high_values.append(float(prices["2. high"]))
            low_values.append(float(prices["3. low"]))
            close_values.append(float(prices["4. close"]))

    #data for chart 
    stock_data = {"open": open_values, "high": high_values, "low": low_values, "close": close_values }

    return dates, stock_data


#Generate a graph and open the user's default browser

def draw_graph(dates, stock_data, symbol_choice, start_date, end_date, chart_type):
    chart_colors = Style(colors=("#FF3B1A", "#0C83F2", "#1AFF6A", "#EDDF1F"))
    if chart_type == "bar":
        chart_object = pygal.Bar(x_label_rotation=45, height=400, style=chart_colors)
    else:
        chart_object = pygal.Line(x_label_rotation=45, height=400, style=chart_colors)

    chart_object.title = f"Stock Data for {symbol_choice}: {start_date} to {end_date}"
    chart_object.x_labels = dates
    chart_object.add("Open", stock_data["open"])
    chart_object.add("High", stock_data["high"])
    chart_object.add("Low", stock_data["low"])
    chart_object.add("Close", stock_data["close"])

    chart_object.render_in_browser()


#send the chart to the base.html and iopen it in the user browser

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
        end_date = get_end_date(start_date)
        time_series = get_api_data(symbol_choice, time_series_choice)

        if time_series:
            dates, stock_data = sort_api_data(time_series, start_date, end_date)

        if dates: 
            draw_graph(dates, stock_data, symbol_choice, start_date, end_date, chart_type)

        else: 
            print("No data was found for that date range. Please try again.")

        prompt_user = input("Would you like to view more stock data? (y/n):").strip().lower()
        if prompt_user != "y":
            print("Goodbye!")
            break

main()