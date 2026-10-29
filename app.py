#imports and setup stuff
import pygal
import lxml
from datetime import datetime
import os
from dotenv import load_dotenv

#get the api key from .env files that are .gitignore (add the api code from README and put into your own .env folder)
load_dotenv()
API_KEY = os.getenv("API_KEY")







#USER INPUTS
#ask the user to enter the stock symbol for the company they want data for
    #only letters, has to be lest than 7
def get_stock_symbol():
    while True:
        user_input = input("\nEnter the stock symbol you are looking for: ").strip()
        user_input_caps = user_input.upper()

        if len(user_input_caps) >= 7:
            print("Stock symbols must be 7 letters or less.")
        

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

        user_input = input("Enter a choice 1-4: ")
        if user_input not in [1,2,3,4]:
            print("\nPlease enter 1,2,3, or 4.")
        else:
            return user_input
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

    #the end date should not be before the begin date
#Generate a graph and open the user's default browser




#main function 
def main():
    print("Stock Date Visualizer\n------------------------")

    #test for now 
    #get_start_date()
    get_chart_type()


main()