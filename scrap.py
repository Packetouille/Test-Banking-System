import sqlite3

#conn = sqlite3.connect('banking_system.sqlite')
cur = conn.cursor()

first_name = 'Andres'
last_name = 'Londono'
ssn = '123-45-6789'
account_number = 12345678
balance = 0.0
ledger = [{'amount': 200, 'description': 'Transferred to Savings'}]
open_date = '03-09-2021'

cur.execute('''SELECT id FROM Customer WHERE Customer.first_name = ? AND Customer.last_name = ?
        AND Customer.ssn = ? ''', (first_name, last_name, ssn))
customer_id = cur.fetchone()[0]
print(customer_id)

cur.execute('''INSERT OR REPLACE INTO Checking (account_number, balance, ledger, open_date) VALUES
            ( ?, ?, ?, ?)''', (account_number, balance, str(ledger), open_date))
cur.execute('SELECT id FROM Checking WHERE account_number = ? ', (account_number,))
checking_id = cur.fetchone()[0]

cur.execute('''INSERT OR REPLACE INTO Manager (customer_id, checking_id) 
            VALUES ( ?, ? )''', (customer_id, checking_id,))

conn.commit()
cur.close()
