# Write your code here
import random
import sqlite3


connection = sqlite3.connect('card.s3db')
cur = connection.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0);''')
connection.commit()


class Session:
    
    all_data = {}

    def __init__(self):
        self.card_number = None
        self.card_password = None
        self.bin_card = '400000'
        self.account_identifier = None
        self.checksum = None
        self.balance = 0
        self.id = 1
        self.balance_db = None
        self.cn_list = []
        self.close_statement = 'The account has been closed!'

    def fit_luhn(self, card_number):
        self.cn_list = list(map(int, str(card_number)))
        for i in range(len(self.cn_list) - 1):
            if i % 2 == 0:
                self.cn_list[i] *= 2
                if self.cn_list[i] > 9:
                    self.cn_list[i] -= 9
        if sum(self.cn_list) % 10 == 0:
            return True
        else:
            return False

    def check_balance(self, card_number):
        cur.execute('''SELECT
                        balance
                       FROM
                        card
                       WHERE
                        number = {};'''.format(str(card_number)))
        self.balance_db = cur.fetchone()
        connection.commit()
        print('Balance: {}'.format(self.balance_db[0]))

    def add_income(self, card_number):
        deposit = int(input('Enter income:'))
        self.all_data[card_number]['balance'] += deposit
        cur.execute('''UPDATE card
                       SET balance = {}
                       WHERE number = {}'''.format(str(self.all_data[card_number]['balance']),
                                                   str(card_number)))
        connection.commit()
        print('Income was added!')

    def do_transfer(self, card_number):
        print('Transfer')
        transfer_card = int(input('Enter card number:'))
        if transfer_card == card_number:
            print('You can\'t transfer money to the same account')
            return None
        elif not(self.fit_luhn(transfer_card)):
            print('Probably you made a mistake in the card number. Please try again!')
            return None
        elif transfer_card not in self.all_data:
            print('Such a card does not exist.')
            return None
        transfer_money = int(input('Enter how much money you want to transfer:'))
        if transfer_money > self.all_data[card_number]['balance']:
            print('Not enough money!')
            return None
        else:
            self.all_data[card_number]['balance'] -= transfer_money
            self.all_data[transfer_card]['balance'] += transfer_money
            cur.execute('''UPDATE card
                       SET balance = {}
                       WHERE number = {}'''.format(str(self.all_data[card_number]['balance']),
                                                   str(card_number)))
            cur.execute('''UPDATE card
                       SET balance = {}
                       WHERE number = {}'''.format(str(self.all_data[transfer_card]['balance']),
                                                   str(transfer_card)))
            connection.commit()
            print('Success!')

    def close_account(self, card_number):
        cur.execute('DELETE FROM card WHERE number = {}'.format(card_number))
        connection.commit()
        print(self.close_statement)

    def create_a_card(self):   
        
        self.account_identifier = ''
        self.card_number = ''   
        self.card_password = '' 
        self.checksum = 0
        
        for _ in range(9):
            self.account_identifier += random.choice('123456789')
                        
        card_number_list = list(map(int, self.bin_card + self.account_identifier))
            
        for i in range(len(card_number_list)):
            if i % 2 == 0:
                card_number_list[i] = card_number_list[i] * 2
                if card_number_list[i] > 9:
                    card_number_list[i] = card_number_list[i] - 9
            else:
                if card_number_list[i] > 9:
                    card_number_list[i] = card_number_list[i] - 9
                    
        digits_sum = sum(card_number_list)
        
        while digits_sum % 10 != 0:
            digits_sum += 1
            self.checksum += 1
        
        self.card_number = int(self.bin_card + self.account_identifier + str(self.checksum))
        
        for _ in range(4):
            self.card_password += random.choice('123456789')
        self.card_password = int(self.card_password)

        cur.execute('INSERT INTO card(id, number, pin, balance) VALUES({}, {}, {}, {});'.format(str(self.id),
                                                                                                str(self.card_number),
                                                                                                str(self.card_password),
                                                                                                str(self.balance)))
        connection.commit()
        self.id += 1
        return self.card_number, self.card_password
    
    def menu(self):
        while True:
            print('1. Create an account', '2. Log into account', '0. Exit', sep='\n')

            point = int(input())

            if point == 1:
                new_card = self.create_a_card()
                while True:
                    if new_card[0] in self.all_data:
                        new_card = self.create_a_card()
                    else:
                        break
                self.all_data[self.card_number] = {'number': self.card_number,
                                                   'password': self.card_password,
                                                   'balance': self.balance}
                print('Your card has been created')
                print('Your card number: ', new_card[0], sep='\n')
                print('Your card PIN:', new_card[1], sep='\n')
                
            elif point == 2:
                login_card_number = int(input('Enter your card number:'))
                login_card_password = int(input('Enter your PIN:'))
                if not(login_card_number in self.all_data) \
                   or self.all_data[login_card_number]['password'] != login_card_password:
                    print('Wrong card number or PIN!')
                elif login_card_number in self.all_data \
                        and self.all_data[login_card_number]['password'] == login_card_password:
                    print('You have successfully logged in!')
                    while True:
                        print('1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out',
                              '0.Exit', sep='\n')
                        point2 = int(input())
                        if point2 == 1:
                            self.check_balance(login_card_number)
                        elif point2 == 2:
                            self.add_income(login_card_number)
                        elif point2 == 3:
                            self.do_transfer(login_card_number)
                        elif point2 == 4:
                            self.close_account(login_card_number)
                        elif point2 == 5:
                            print('You have successfully logged out!')
                            break
                        elif point2 == 0:
                            print('Bye!')
                            exit()
                            
            elif point == 0:
                print('Bye!')
                break
                

lil_session = Session()
lil_session.menu()
