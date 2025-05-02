import re
import time
import random
import datetime
from sklearn.ensemble import RandomForestClassifier

# Constants
MAX_USERS = 5
MAX_ATTEMPTS = 5
MAX_TRANSACTIONS_PER_DAY = 5
MAX_TRANSACTION_AMOUNT = 10000
FRAUD_AMOUNT_LIMIT = 2000
FRAUD_LOCATIONS = {"Local", "Chennai", "TEC"}
INITIAL_BALANCE = 50000

# Data storage
users = {}
transaction_history = {}
login_attempts = {}
wrong_attempts = {}
daily_transaction_count = {}
daily_transaction_amount = {}

# Expanded training data to avoid overfitting
training_data = []
labels = []
for _ in range(100):
    amt = random.randint(100, 10000)
    loc_flag = random.randint(0, 1)
    amt_flag = 1 if amt > FRAUD_AMOUNT_LIMIT else 0
    fraud_label = 1 if (loc_flag or amt_flag) and random.random() > 0.3 else 0
    training_data.append([amt, loc_flag, amt_flag])
    labels.append(fraud_label)

clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(training_data, labels)

def ai_fraud_check(amount, location):
    is_fraud_location = 1 if location not in FRAUD_LOCATIONS else 0
    is_high_amount = 1 if amount > FRAUD_AMOUNT_LIMIT else 0
    input_features = [[amount, is_fraud_location, is_high_amount]]
    prediction = clf.predict(input_features)[0]
    return bool(prediction)

def mask_card(card):
    return "XXXX-XXXX-XXXX-" + card[-4:]

def generate_transaction_id():
    return "TXN" + str(random.randint(100000, 999999))

def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y"), now.strftime("%H:%M:%S")

def welcome():
    print("WELCOME TO CREDIT CARD FRAUD DETECTION SYSTEM WITH AI INTEGRATION")
    while True:
        print("\n1.Register\n2.Login\n3.Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting... Thank you for using our Service ^-^")
            break
        else:
            print("Invalid choice! Please select from the given options.")

def register():
    if len(users) >= MAX_USERS:
        print("Maximum number of registrations reached for today.")
        return

    print("\nNew User Register Here")
    username = input("Enter username: ")
    if not re.match("^[A-Za-z0-9]+$", username):
        print("Invalid username! Only alphabets and numbers are allowed.")
        return

    if username in users:
        print("Username already exists.")
        return

    password = input("Enter password (4 characters): ")
    if len(password) != 4:
        print("Password must be exactly 4 characters.")
        return

    pin = input("Enter 4-digit PIN: ")
    if not pin.isdigit() or len(pin) != 4:
        print("PIN must be exactly 4 digits.")
        return

    card = input("Enter your 16 digit card number: ")
    if not (card.isdigit() and len(card) == 16):
        print("Card number must be exactly 16 digits.")
        return

    users[username] = {
        'password': password,
        'pin': pin,
        'card': card,
        'balance': INITIAL_BALANCE
    }
    transaction_history[username] = []
    login_attempts[username] = 0
    wrong_attempts[username] = 0
    daily_transaction_count[username] = 0
    daily_transaction_amount[username] = 0

    print(f"{username}, Registered Successfully!")
    return

def login():
    print("\nRegistered user login Here")
    username = input("Enter username: ")
    if username not in users:
        rule_1_violation(username, "Invalid Username")
        return

    if wrong_attempts[username] >= MAX_ATTEMPTS:
        print("Too many invalid attempts! Try on the Next Day.")
        print("Thank you for using our Service ^-^")
        return

    password = input("Enter password: ")
    if password != users[username]['password']:
        rule_1_violation(username, "Invalid Password")
        return

    pin = input("Enter 4-digit PIN: ")
    if pin != users[username]['pin']:
        rule_1_violation(username, "Invalid PIN")
        return

    card = input("Enter 16-digit card number: ")
    if card != users[username]['card']:
        rule_1_violation(username, "Invalid Card Number")
        return

    login_attempts[username] += 1
    print(f"{username}, Logged In Successfully!")
    main_menu(username)
    return

def rule_1_violation(username, reason):
    print(f"{reason}")
    if username in wrong_attempts:
        wrong_attempts[username] += 1
    else:
        wrong_attempts[username] = 1

    if wrong_attempts[username] >= MAX_ATTEMPTS:
        print("Too many invalid attempts! Try on the Next Day.")
        print("Thank you for using our Service ^-^")
    else:
        remaining = MAX_ATTEMPTS - wrong_attempts[username]
        print(f"{username}, You have only {remaining} attempts left")

def main_menu(username):
    while True:
        print("\nMAIN MENU")
        print("1.Make Transaction\n2.View Transaction History\n3.Check Balance\n4.Logout")
        choice = input("Choose an option: ")
        if choice == '1':
            make_transaction(username)
        elif choice == '2':
            view_transaction_history(username)
        elif choice == '3':
            check_balance(username)
        elif choice == '4':
            print(f"{username}, Logged out Successfully")
            print("Thank you for using our Service ^-^")
            time.sleep(3)
            return
        else:
            print("Invalid choice!")

def make_transaction(username):
    if daily_transaction_count[username] >= MAX_TRANSACTIONS_PER_DAY or \
       daily_transaction_amount[username] >= MAX_TRANSACTION_AMOUNT:
        print(f"{username}, Exceeded Today's Transaction limit. Please Try on the Next Day.")
        print("Thank you for using our Service ^-^")
        return

    print("\nChoose Transaction Type")
    print("1.Deposit\n2.Withdraw")
    choice = input("Enter choice: ")
    if choice == '1':
        deposit(username)
    elif choice == '2':
        withdraw(username)
    else:
        print("Invalid choice!")
    return

def deposit(username):
    print("\nTransaction Type: Deposit")

    user_card = input("Enter your 16 digit card number: ")
    if user_card != users[username]['card']:
        rule_1_violation(username, "Invalid Card Number")
        return

    pin = input("Enter your PIN: ")
    if pin != users[username]['pin']:
        rule_1_violation(username, "Invalid PIN")
        return

    recipient_card = input("Enter Recipient's 16 digit Card number: ")
    recipient_username = input("Enter Recipient's username: ")

    if (recipient_username not in users or
        users[recipient_username]['card'] != recipient_card or
        recipient_username == username):
        rule_1_violation(username, "Invalid Recipient Information")
        return

    try:
        amount = float(input("Enter amount in R.s: "))
    except ValueError:
        rule_1_violation(username, "Invalid Amount")
        return

    location = input("Enter Location: ")
    if not location.isalpha():
        rule_1_violation(username, "Invalid Location")
        return

    print("\nPayment page: Deposit")
    print("1.Confirm Transaction\n2.Cancel Transaction")
    choice = input("Choose an option: ")
    if choice == '1':
        confirm_transaction(username, "Deposit", amount, location, recipient_card, recipient_username)
    else:
        print("Transaction Cancelled! Returning to MAIN MENU")
        print("Please wait.Loading...")
        time.sleep(3)
    return

def withdraw(username):
    print("\nTransaction Type: Withdraw")

    user_card = input("Enter your 16 digit card number: ")
    if user_card != users[username]['card']:
        rule_1_violation(username, "Invalid Card Number")
        return

    pin = input("Enter your PIN: ")
    if pin != users[username]['pin']:
        rule_1_violation(username, "Invalid PIN")
        return

    try:
        amount = float(input("Enter amount in R.s: "))
    except ValueError:
        rule_1_violation(username, "Invalid Amount")
        return

    location = input("Enter Location: ")
    if not location.isalpha():
        rule_1_violation(username, "Invalid Location")
        return

    print("\nPayment page: Withdraw")
    print("1.Confirm Transaction\n2.Cancel Transaction")
    choice = input("Choose an option: ")
    if choice == '1':
        confirm_transaction(username, "Withdraw", amount, location)
    else:
        print("Transaction Cancelled! Returning to MAIN MENU")
        print("Please wait.Loading...")
        time.sleep(3)
    return

def confirm_transaction(username, txn_type, amount, location, recipient_card=None, recipient_username=None):
    fraud = False
    ai_detected_fraud = ai_fraud_check(amount, location)
    rule_based_fraud = amount > FRAUD_AMOUNT_LIMIT or location not in FRAUD_LOCATIONS
    insufficient_balance = False
    success = True
    status2 = ""

    if ai_detected_fraud or rule_based_fraud:
        fraud = True
        success = False
        status2 = "Fraudulent Detected by AI" if ai_detected_fraud else "Rule-Based Fraud Detected"

    if txn_type == "Withdraw":
        if users[username]['balance'] < amount:
            insufficient_balance = True
            success = False
            status2 = "Insufficient Balance"

    if success:
        users[username]['balance'] -= amount
        if txn_type == "Deposit":
            users[recipient_username]['balance'] += amount

        daily_transaction_count[username] += 1
        daily_transaction_amount[username] += amount

    txn_id = generate_transaction_id()
    date, time_now = get_datetime()
    masked_user_card = mask_card(users[username]['card'])
    masked_recipient_card = mask_card(recipient_card) if recipient_card else None

    transaction = {
        'sno': len(transaction_history[username]) + 1,
        'type': txn_type,
        'amount': amount,
        'location': location,
        'date': date,
        'time': time_now,
        'transaction_id': txn_id,
        'status1': "Transaction Successful !" if success else "Transaction Failed",
        'status2': "No, Fraudulent Detected" if not fraud and not insufficient_balance else status2,
        'available_balance': users[username]['balance'],
        'card': masked_user_card,
        'recipient_card': masked_recipient_card,
        'recipient_username': recipient_username
    }

    transaction_history[username].append(transaction)

    print(f"\nTransaction Details of {username}")
    print(f"Transaction Status: {transaction['status1']}")
    print(f"{transaction['status2']}")
    print(f"Amount {'Deposited' if txn_type == 'Deposit' else 'Withdrawn'} in R.s: {amount:.2f}")
    if txn_type == "Deposit":
        print(f"Recipient's Card number: {masked_recipient_card}")
        print(f"Recipient's username: {recipient_username}")
    print(f"Available Balance: R.s. {users[username]['balance']:.2f}")
    print(f"Date: {date}")
    print(f"Time: {time_now}")
    print(f"Transaction ID: {txn_id}")
    print(f"Card number: {masked_user_card}")
    print("Thank you for using our Service ^-^")

    print("\n1.Back to MAIN MENU")
    input()
    print("Please wait.Loading...")
    time.sleep(3)
    return

def view_transaction_history(username):
    print("\nTransaction History")
    if not transaction_history[username]:
        print(f"No Transaction is done by {username}")
    else:
        for txn in transaction_history[username]:
            print("------")
            print(f"S.no: {txn['sno']}")
            print(f"Date and Time: {txn['date']} {txn['time']}")
            print(f"Transaction Type: {txn['type']}")
            if txn['type'] == "Deposit":
                print(f"Recipient's Card number: {txn['recipient_card']}")
                print(f"Recipient's username: {txn['recipient_username']}")
            print(f"Amount in R.s: {txn['amount']:.2f}")
            print(f"Available Balance: R.s. {txn['available_balance']:.2f}")
            print(f"Transaction ID: {txn['transaction_id']}")
            print(f"Status1: {txn['status1']}")
            if txn['status1'] == "Transaction Failed":
                print(f"Status2: {txn['status2']}")
        print("------")

    print("\n1.Back to MAIN MENU")
    input()
    print("Please wait.Loading...")
    time.sleep(3)
    return

def check_balance(username):
    print(f"\n{username}, Your Current Available Balance in Your Account is R.s.{users[username]['balance']:.2f}")
    print("\n1.Back to MAIN MENU")
    input()
    print("Please wait.Loading...")
    time.sleep(3)
    return

# Entry Point
if __name__ == "__main__":
    welcome()