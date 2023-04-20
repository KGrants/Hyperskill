import random
import sys
from conn_details import conn
from conn_details import cur


def first_screen():
    options = ["1. Create an account", "2. Log into account", "3. Exit"]
    print("", *options, sep="\n")  # Print menu
    return input(">").strip()  # Get user input


def second_screen():
    options = ["1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit"]
    print("", *options, sep="\n")  # Print menu
    return input(">").strip()  # Get user input


def card_sequence():
    cur.execute('''SELECT COALESCE(max(id), 0) 
                   FROM card''')
    return int(cur.fetchone()[0])


def luhn(st):
    int_list = [int(i) for i in st]
    for i in range(0, len(int_list), 2):
        int_list[i] = int_list[i] * 2
    int_list = [i if i < 10 else i - 9 for i in int_list]
    return 10 - sum(int_list) % 10 if sum(int_list) % 10 != 0 else 0


def luhn_check(st):
    card_no = st[:-1]
    int_list = [int(i) for i in card_no]
    for i in range(0, len(int_list), 2):
        int_list[i] = int_list[i] * 2
    int_list = [i if i < 10 else i - 9 for i in int_list]
    return 1 if (sum(int_list)+int(st[-1])) % 10 == 0 else 0


def generate_pin():
    pin_code = ""
    for i in range(4):
        pin_code += str(random.randint(0, 9))
    return pin_code


def print_balance(card_no):
    cur.execute("""SELECT balance 
                   FROM card 
                   WHERE 1=1
                   AND number = '%s'""" % card_no)
    print(cur.fetchone()[0])


def get_balance(card_no):
    cur.execute("""SELECT balance 
                   FROM card 
                   WHERE 1=1
                   AND number = '%s'""" % card_no)
    return cur.fetchone()[0]


def exit_bank():
    print("\nBye!")
    conn.close()
    sys.exit()


def table_card_check():
    cur.execute('''CREATE TABLE IF NOT EXISTS card
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0)''')
    conn.commit()


def add_income(card_no):
    # get input to add to balance
    print("Enter income:")
    cash = int(input(">").strip())

    # validate if input is larger than zero
    if cash <= 0:
        print("Error has occurred.\nYou can't deposit 0 or negative amount.")
        add_income(card_no)
        return

    # get current balance to add cash to
    curr_balance = get_balance(card_no)

    cur.execute("""UPDATE card 
                   SET balance = '%s'
                   WHERE 1=1 
                   AND number = '%s'""" % (cash+curr_balance, card_no))
    conn.commit()
    print("Income was added!")


def transfer(card_no):
    # get current balance to add cash to
    curr_balance = get_balance(card_no)
    print("Enter card number:")
    trf_to = input(">").strip()
    cur.execute("""SELECT number
                   FROM card
                   WHERE 1=1
                   AND number = '%s'""" % trf_to)
    check = cur.fetchone()
    if luhn_check(trf_to) == 0:
        print("Probably you made a mistake in the card number. Please try again!")
        return
    elif check is None:
        print("Such a card does not exist.")
        return
    elif check[0] == card_no:
        print("You can't transfer money to the same account!")
        return

    print("Enter how much money you want to transfer:")
    trf = int(input(">").strip())
    if trf > curr_balance:
        print("Not enough money!")
        return
    rec_balance = get_balance(trf_to)
    cur.execute("""UPDATE card 
                   SET balance = '%s'
                   WHERE 1=1 
                   AND number = '%s'""" % (curr_balance-trf, card_no))
    cur.execute("""UPDATE card 
                   SET balance = '%s'
                   WHERE 1=1 
                   AND number = '%s'""" % (rec_balance + trf, trf_to))
    conn.commit()
    print("Success!")
    return


def close_account(card_no):
    cur.execute("""DELETE FROM card 
                   WHERE 1 = 1
                   AND number = '%s'""" % card_no)
    conn.commit()
    print("The account has been closed!")
    return
