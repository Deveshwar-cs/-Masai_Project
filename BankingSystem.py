import os
from datetime import datetime

# File paths
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# Utility functions
def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            for line in file:
                account_number, name, password, balance = line.strip().split(',')
                accounts[account_number] = {
                    'name': name,
                    'password': password,
                    'balance': float(balance)
                }
    return accounts

def save_account(account_number, name, password, balance):
    with open(ACCOUNTS_FILE, 'a') as file:
        file.write(f"{account_number},{name},{password},{balance}\n")

def log_transaction(account_number, transaction_type, amount):
    with open(TRANSACTIONS_FILE, 'a') as file:
        date = datetime.now().strftime('%Y-%m-%d')
        file.write(f"{account_number},{transaction_type},{amount},{date}\n")

def display_menu():
    print("\n=== Banking System ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    return input("Enter your choice: ")

def create_account(accounts):
    account_number = input("Enter a unique account number: ")
    if account_number in accounts:
        print("Account number already exists. Try again.")
        return

    name = input("Enter your name: ")
    password = input("Set your password: ")
    balance = float(input("Enter initial deposit amount: "))

    accounts[account_number] = {
        'name': name,
        'password': password,
        'balance': balance
    }

    save_account(account_number, name, password, balance)
    print("Account created successfully!")

def login(accounts):
    account_number = input("Enter your account number: ")
    if account_number not in accounts:
        print("Account does not exist. Try again.")
        return

    password = input("Enter your password: ")
    if accounts[account_number]['password'] != password:
        print("Incorrect password. Try again.")
        return

    print(f"Welcome, {accounts[account_number]['name']}!")
    user_dashboard(accounts, account_number)

def user_dashboard(accounts, account_number):
    while True:
        print("\n--- Dashboard ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Transaction History")
        print("5. Change Password")
        print("6. Close Account")
        print("7. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            print(f"Your balance is: {accounts[account_number]['balance']}")
        elif choice == '2':
            deposit(accounts, account_number)
        elif choice == '3':
            withdraw(accounts, account_number)
        elif choice == '4':
            view_transaction_history(account_number)
        elif choice == '5':
            change_password(accounts, account_number)
        elif choice == '6':
            close_account(accounts, account_number)
            break
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def deposit(accounts, account_number):
    amount = float(input("Enter deposit amount: "))
    accounts[account_number]['balance'] += amount
    log_transaction(account_number, "Deposit", amount)
    update_accounts_file(accounts)
    print("Deposit successful!")

def withdraw(accounts, account_number):
    amount = float(input("Enter withdrawal amount: "))
    if amount > accounts[account_number]['balance']:
        print("Insufficient balance. Transaction failed.")
    else:
        accounts[account_number]['balance'] -= amount
        log_transaction(account_number, "Withdrawal", amount)
        update_accounts_file(accounts)
        print("Withdrawal successful!")

def update_accounts_file(accounts):
    with open(ACCOUNTS_FILE, 'w') as file:
        for account_number, details in accounts.items():
            file.write(f"{account_number},{details['name']},{details['password']},{details['balance']}\n")

def view_transaction_history(account_number):
    print("\n--- Transaction History ---")
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'r') as file:
            transactions = [line.strip() for line in file if line.startswith(account_number)]
        if transactions:
            for transaction in transactions:
                print(transaction)
        else:
            print("No transactions found.")
    else:
        print("No transactions found.")

def change_password(accounts, account_number):
    current_password = input("Enter your current password: ")
    if accounts[account_number]['password'] != current_password:
        print("Incorrect password. Try again.")
        return

    new_password = input("Enter your new password: ")
    accounts[account_number]['password'] = new_password
    update_accounts_file(accounts)
    print("Password changed successfully!")

def close_account(accounts, account_number):
    confirm = input("Are you sure you want to close your account? (yes/no): ")
    if confirm.lower() == 'yes':
        del accounts[account_number]
        update_accounts_file(accounts)
        print("Account closed successfully.")
    else:
        print("Account closure canceled.")

# Main function
def main():
    accounts = load_accounts()

    while True:
        choice = display_menu()

        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            login(accounts)
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
