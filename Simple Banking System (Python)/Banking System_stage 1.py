import random
import os 

pin_dict = {}
balance_dict = {}
acc_no_seq = 0

def first_screen():
    return input("1. Create an account\n2. Log into account\n0. Exit\n")

def second_screen():
   return input("1. Balance\n2. Log out\n0. Exit")

class Bank_Account():
    card_no = ""
    pin_code = ""
    
    def __init__(self):
        global acc_no_seq
        global pin_dict
        global balance_dict
        
        check_num = random.randint(0,9)
        self.card_no = "400000"+str(acc_no_seq).zfill(9)+str(check_num)
        self.pin_code = str(random.randint(0,9999))
        acc_no_seq += 1
        pin_dict[self.card_no] = self.pin_code
        balance_dict[self.card_no] = 0

        print("Your card has been created")
        print("Your card number:\n{0}".format(self.card_no))
        print("Your card PIN:\n{0}".format(self.pin_code))      

def login():
    global pin_dict
    card_no = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    if card_no not in pin_dict.keys() or pin_dict[card_no] != pin_code:
        print("Wrong card number or PIN!")
    else:
        print("You have successfully logged in!")
        account_actions(card_no)

def account_actions(card_no):
    global balance_dict
    while True:
        user_input = second_screen()
        if user_input == "0":
            print("Bye!")
            exit()
        elif user_input == "1":
            print(balance_dict[card_no])
        else:
            return

while True:
    user_input = first_screen()
    if user_input == "1":
        bank_account = Bank_Account()
    elif user_input == "2":
        login()
    elif user_input == "0":
        print("Bye!")
        exit()
    else:
        print("Unhandled Error!")
        exit()
