import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales input figures from user
    """
    while True:
        print("please enter sales data from the last market.")
        print("Data should be six numbers separated by commas")
        print("example: 10,20,30,40,50,60\n")
        data_str = input("Enter sales data here: ")
        print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")

        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Validates the data from user input
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 numbers required.\nYou provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid Data: {e}. Please try again. \n")
        return False
    return True


def update_sales_worksheet(data):
    """
    updates sales worksheet with user input data
    """
    print("updating sales data...")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Successfullt updated worksheet")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)