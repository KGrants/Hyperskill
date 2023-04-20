import functions
from conn_details import conn
from conn_details import cur

# Check if card table exists, create if necessary
functions.table_card_check()


class BankAccount:
    card_no = ""
    pin_code = ""

    def __init__(self):
        self.card_no = "400000" + str(functions.card_sequence()).zfill(9)
        check_num = functions.luhn(self.card_no)
        self.card_no = self.card_no + str(check_num)
        self.pin_code = functions.generate_pin()

        # Insert into database
        cur.execute("INSERT INTO card (number, pin) VALUES (?, ?)",
                    (self.card_no, self.pin_code))
        conn.commit()

        print("Your card has been created")
        print("Your card number:\n{0}".format(self.card_no))
        print("Your card PIN:\n{0}".format(self.pin_code))


def login():
    card_no = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    cur.execute("""SELECT NUMBER, PIN FROM CARD WHERE NUMBER = '%s'""" % card_no)
    comb = cur.fetchone()
    if (card_no, pin_code) != comb:
        print("Wrong card number or PIN!")
    else:
        print("You have successfully logged in!")
        account_actions(card_no)


def account_actions(card_no):
    while True:
        user_inp = functions.second_screen()
        func_dict = {"1": functions.print_balance,
                     "2": functions.add_income,
                     "3": functions.transfer,
                     "4": functions.close_account,
                     "0": functions.exit_bank}
        if user_inp == "0":
            functions.exit_bank()
        elif user_inp == "5":
            break
        if user_inp not in func_dict.keys():
            print("This option does not exist.\nLogging out.")
            return
        else:
            func_dict[user_inp](card_no)
            if user_inp == "4":
                break


def main():
    while True:
        user_input = functions.first_screen()
        if user_input == "1":
            bank_account = BankAccount()
        elif user_input == "2":
            login()
        else:
            functions.exit_bank()


if __name__ == '__main__':
    main()
