import banking
import datetime
import time

while True:
    banking.clear()
    print(datetime.date.today())
    user_entry = input("Welcome! Are you an existing customer (yes/no): ")

    if user_entry.lower() == 'yes':
        customer_id = banking.log_in()
        customer = banking.Customer(customer_id)            # Instantiate
        break
    if user_entry.lower() == 'no':
        customer = banking.new_customer_display()           # Instantiate
        if customer.flag:
            banking.clear()
            print("Customer profile exists! Please log in.")
            customer.__del__()
            time.sleep(3)
            continue
        else:
            break

while True:
    response = banking.existing_customer_menu(customer)

    if response == '1':
        banking.clear()
        account_type = input("What type of account do you want to open (Checking/Savings): ")
        open_acc = customer.open_account(account_type)

        if not open_acc:            # open_acc is False if account was not open because one was already found
            print(f"You already have a {account_type} account with us!")
            time.sleep(3)
            continue

    elif response == '2':
        banking.clear()
        deposit_amnt = input("Please enter amount to deposit: ")
        customer.deposit_funds(deposit_amnt)
        break
    elif response == '5':
        print('CHECK BALANCE')
        quit()
    elif response == '6':
        banking.clear()
        print("Thank you for your business! Have a nice day!")
        break
