import random
import sqlite3
import datetime
from os import system, name
import time

conn = sqlite3.connect('banking_system.sqlite')

class Customer:
    def __init__(self, customer_id = None):
    # Constructor:
        if customer_id != None:
            self.__retrieve_customer_data(customer_id)
        elif customer_id == None:
            self.get_user_info()
            db_customer_flag = self.__dbload_customer_info()
            if db_customer_flag:
                self.flag = True

    def open_account(self, account_type):
        self.ledger = []
        self.account_type = account_type
        self.account_number = self.__generate_account_num()
        self.open_date = datetime.date.today()
        self.balance = 0.0

        db_account_flag = self.__dbload_account_info(account_type)

        if not db_account_flag:     # Flag will be False if account was not created because account exists
            return False
        else:
            welcome_message(self.first_name, self.account_type, self.account_number)

    def __generate_account_num(self):
        return random.randrange(1000000, 9999999)

    def get_user_info(self):
        self.first_name = input("First name: ")
        self.middle_name = input("Middle name: ")
        self.last_name = input("Last name: ")
        self.ssn = input("Social Security Number: ")
        self.address = input("Address - please include city/state/zip: ")
        self.phone_num = input("Phone number: ")
        self.email_address = input("Email address: ")
        self.cus_open_date = datetime.date.today()
        self.user_name = input("Select a username: ")

        while True:
            self.password = input("Enter a password: ")
            clear()
            password_test = input("Enter the password again: ")

            if self.password == password_test: break
            else: print("The passwords do not match! Please try again.")

    def deposit_funds(self, amount):
        print()

    def withdraw_funds(self, amount):
        print()

    def update_user_info(self):
        print()

    def authentication(self):
        print()

    def get_balance(self, amount, account_type):
        current_balance = 0.0

        for item in self.ledger.items():
            current_balance += item['amount']

        return current_balance

    def check_funds(self, amount):
        if amount >= self.get_balance(amount, self.account_type):
            return True
        else:
            return False

    def __dbload_customer_info(self):
    # This private method loads the new customer information into the Customer Table in the banking_system.
    # database. It links the Customer and Manager Tables by customer_id, loads the user_name and password
    # credentials into the Online_Accounts Table, and lastly links the Online_Accounts and Customer Tables
    # by the customer_id.
        cur = conn.cursor()

        cur.execute('''SELECT id FROM Customer WHERE Customer.first_name = ?
                    AND Customer.ssn = ?''', (self.first_name, self.ssn))
        customer_id = cur.fetchone()[0]

        if customer_id == self.customer_id:
            return True                     # Return True if customer profile already exists

        cur.execute('''INSERT INTO Customer (first_name, middle_name, last_name, ssn,
                    address, email_address, phone_num, cus_open_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (self.first_name, self.middle_name, self.last_name, self.ssn,\
                          self.address, self.email_address, self.phone_num, self.cus_open_date))

        cur.execute('''SELECT id FROM Customer WHERE Customer.first_name = ?
                    AND Customer.ssn = ?''', (self.first_name, self.ssn))
        customer_id = cur.fetchone()[0]

        cur.execute('''INSERT OR REPLACE INTO Manager (customer_id) 
                    VALUES (?)''', (customer_id, ))

        cur.execute('''INSERT OR REPLACE INTO Online_Accounts (customer_id, user_name, password)
                    VALUES (?, ?, ?)''', (customer_id, self.user_name, self.password))

        conn.commit()
        cur.close()
        return False                    # Return flag as False if customer did not exist and load successful

    def __dbload_account_info(self, account_type):
    # This private method !!!!UFINISHED!!! - Modify this method to be called at any point to update the db...
    # Or perhaps another method should take of updating. This one handles creating new records and updating
    # the Manager Table keys. At the moment this bank only allows ONE TYPE OF ACCOUNT PER CUSTOMER!
        cur = conn.cursor()

        # CHECK TO SEE IF AN ACCOUNT ALREADY EXISTS. IF YES THEN RETURN A FLAG.

        if account_type.lower() == "checking":
            cur.execute('''SELECT Checking.id FROM Checking JOIN Manager JOIN Customer
                WHERE Checking.id = Manager.checking_id AND Manager.customer_id = Customer.id
                AND Customer.ssn = ?''', (self.ssn, ))
            checking_id = cur.fetchone()[0]
            if isinstance(checking_id, int):
                return False                                     # Return False if cannot proceed because account found

        elif account_type.lower() == "savings":
            cur.execute('''SELECT Savings.id FROM Savings JOIN Manager JOIN Customer
                WHERE Savings.id = Manager.savings_id AND Manager.customer_id = Customer.id
                AND Customer.ssn = ?''', (self.ssn,))
            savings_id = cur.fetchone()[0]
            if isinstance(savings_id, int):
                return False                                    # Return False if cannot proceed because account found

        # IF YOU HAVE MADE IT THIS FAR THEN AN ACCOUNT DOES NOT EXIST. LET'S LOAD ONE INTO THE DATABASE

        cur.execute('''SELECT id FROM Customer WHERE Customer.first_name = ? AND Customer.last_name = ?
                AND Customer.ssn == ?''', (self.first_name, self.last_name, self.ssn, ))
        customer_id = cur.fetchone()[0]

        if account_type.lower() == "checking":
            cur.execute('''INSERT OR REPLACE INTO Checking (account_number, balance, ledger, open_date) VALUES
                        ( ?, ?, ?, ?)''', (self.account_number, self.balance, str(self.ledger), self.open_date))
            cur.execute('SELECT id FROM Checking WHERE account_number = ? ', (self.account_number, ))
            checking_id = cur.fetchone()[0]

            cur.execute('''UPDATE Manager SET checking_id = ? 
                        WHERE Manager.customer_id = ?''', (checking_id, customer_id))

        elif account_type.lower() == "savings":
            cur.execute('''INSERT OR REPLACE INTO Savings (account_number, balance, ledger, open_date) VALUES
                                    ( ?, ?, ?, ?)''', (self.account_number, self.balance, str(self.ledger), self.open_date))
            cur.execute('SELECT id FROM Savings WHERE account_number = ? ', (self.account_number, ))
            savings_id = cur.fetchone()[0]

            cur.execute('''UPDATE Manager SET savings_id = ? 
                        WHERE Manager.customer_id= ?''', (savings_id, customer_id))

        conn.commit()
        cur.close()
        return True                                           # Account created = True, new account has been created

    def __retrieve_customer_data(self, customer_id):
    # This private method retrieves customer data from the Customer Table using the passed in customer_id
        cur = conn.cursor()

        cur.execute('''SELECT first_name, middle_name, last_name, ssn, address, email_address,
                    phone_num, cus_open_date FROM Customer WHERE Customer.id = ? ''', (customer_id, ))
        customer_info = cur.fetchone()

        self.customer_id = customer_id
        self.first_name = customer_info[0]
        self.middle_name = customer_info[1]
        self.last_name = customer_info[2]
        self.ssn = customer_info[3]
        self.address = customer_info[4]
        self.email_address = customer_info[5]
        self.phone_num = customer_info[6]
        self.cus_open_date = customer_info[7]

        cur.close()

    def __retrieve_account_data(self, customer_id, account_type):
    # This private method retrieves account data from the [account_type] Table using the passed in parameters to
    # reference the proper Table and
        cur = conn.cursor()

        if account_type == 'checking':
            cur.execute('''SELECT account_number, balance, ledger FROM Checking JOIN Manager 
                    WHERE Manager.customer_id = ? AND Manager.checking_id = Checking.id''', (customer_id, ))
            info = cur.fetchone()
        elif account_type == 'savings':
            cur.execute('''SELECT account_number, balance, ledger FROM Savings JOIN Manager 
                    WHERE Manager.customer_id = ? AND Manager.savings_id = Savings.id''', (customer_id, ))
            info = cur.fetchone()

        self.account_number = info[0]
        self.balance = info[1]
        self.ledger = info[2]
        cur.close()

    def __del__(self):
        print()

##############################################################################
        
def new_customer_display():
    clear()
    print(f"Welcome! Let's get you set up with a user profile first.")
    customer = Customer()                                                 # Instantiate

    return customer

def existing_customer_menu(customer):
    clear()
    print(f"How may we help you today, {customer.first_name}?")
    print("1. Open a new account")
    print("2. Deposit funds")
    print("3. Withdraw funds")
    print("4. Transfer funds")
    print("5. Check balance")
    print("6. Sign Out")
    response = input("\nPlease make a selection: ")
    return response

def welcome_message(first_name, account_type, account_number):
    clear()
    print(f"Welcome {first_name}! Please wait while we create your account.")
    time.sleep(5)
    print(f"\nCongratulations, {first_name}! Your account has been created.")
    print(f"Your new {account_type} account number is: {account_number}")
    time.sleep(10)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def log_in():
    while True:
        clear()
        while True:
            clear()
            username = input("Enter User name: ")
            flag = authenticate_username(username)
            if flag:
                break
            else:
                print("Username does not exist! Please try again.")
                time.sleep(2)
                continue

        attempts_left = 5
        while True:
            clear()
            if attempts_left < 3:
                print(f"You have {attempts_left} attempts left!")
            password = input("Enter Password: ")
            customer_id = authenticate_pass_fetch(username, password)
            if customer_id is False:
                attempts_left -= 1
                if attempts_left == 0:
                    print("Too many failed attempts!")
                    attempts_left = 5
                    time.sleep(2)
                    break
                else:
                    print(f"Invalid credentials! Please try again.")
                    time.sleep(2)
                    continue
            else:
                return customer_id

def authenticate_username(username):
    cur = conn.cursor()
    cur.execute('SELECT customer_id FROM Online_Accounts WHERE user_name = ?', (username, ))
    try:
        customer_id = cur.fetchone()[0]
    except:
        customer_id = False

    cur.close()
    return str(customer_id).isnumeric()

def authenticate_pass_fetch(username, password):
    cur = conn.cursor()
    cur.execute('SELECT customer_id FROM Online_Accounts WHERE user_name = ? AND password = ?', (username, password))
    try:
        customer_id = cur.fetchone()[0]
    except:
        customer_id = False

    cur.close()
    return customer_id if str(customer_id).isnumeric() else False

def link_online_account():
    print()

def create_online_account(username, password):
    cur = conn.cursor()

    cur.execute('INSERT OR IGNORE INTO Online_Accounts (user_name, password) VALUES (?, ?)', (username, password))

    conn.commit()
    cur.close()
    return True
