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
        data_str = input("Enter sales data here: \n")
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


def calculate_surplus_data(sales_row):
    """
    compares sales with premade to get surplus
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(f"stock row: {stock_row}")
    print(f"sales row: {sales_row}")
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
    return surplus_data


def update_surplus_worksheet(surplus):
    """
    Update surplus data in worksheet
    """
    print("Updating Surplus Data...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus)
    print("Uppdate successfull!")


def update_worksheet(data, worksheet):
    """
    update worksheet
    """
    print(f"Updating {worksheet}")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully")


def get_last_five_entries_sales():
    """
    Get the last five entries of each sandwich to calculate 
    an average to decrease spill"
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate stock and add 10%
    """
    print("Calculating stock data!\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    the main functions of the programme
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    print(stock_data)


print("welcome to love sandwiches data automation")
main()
