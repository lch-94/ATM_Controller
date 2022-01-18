class CardInfo:
    def __init__(self, card_num, card_pin, valid_thru_month=None, 
                valid_thru_year=None, card_cvc=None, user_name=None):
        self.card_num = card_num
        self.card_pin = card_pin
        self.valid_thru_month = valid_thru_month
        self.valid_thru_year = valid_thru_year
        self.cvc = card_cvc
        self.is_valid = False
        self.user_name = user_name

        self.list_account = []


    def add_test_account(self, name, balance):
        account = Account(name, balance)
        self.list_account.append(account)


    def check_PIN_validataion(self, card_pin):
        if card_pin == self.card_pin:
            self.is_valid = True

        return self.is_valid


class ATM:
    def __init__(self):
        self.list_CardInfo = []


    def add_test_cardInfo(self):
        with open("test_card_info.csv", "r") as f:
            for line in f:
                card_num = line.rstrip().split(",")[0]
                card_pin = line.rstrip().split(",")[1]
                cardInfo = CardInfo(card_num, card_pin)
                
                with open("test_account_info.csv", "r") as f2:
                    for line2 in f2:
                        account_csv_info = line2.rstrip().split(",")

                        if account_csv_info[0] == card_num:
                            cardInfo.add_test_account(account_csv_info[1],
                                                    int(account_csv_info[2]))

                self.list_CardInfo.append(cardInfo)

        if len(self.list_CardInfo) != 0:
            print(f"[*] test setting loaded,  {len(self.list_CardInfo)}")


class Account:
    def __init__(self, name, balance):
        self.balance = balance
        self.name = name

    def get_balance(self):
        return self.balance
    

    def deposit(self, dep_dollar):
        #if type(dep_dollar) != int:
        self.balance += dep_dollar

        return self.balance
        

    def withdraw(self, wit_dollar):
        if self.balance >= wit_dollar:
            self.balance -= wit_dollar
        else:
            print("There is not enough balance in this account")
        
        return self.balance        


def InsertCard(card_num, card_pin, valid_thru_month=None, 
                valid_thru_year=None, card_cvc=None, user_name=None):
    cardInfo = CardInfo(card_num, card_pin, card_num, 
                valid_thru_month, valid_thru_year, card_cvc, user_name)


def print_cmd():
    print("--------- cmd ---------")
    print("  1. See Balance")
    print("  2. Deposit")
    print("  3. Withdraw")
    print("  4. exit")

    cmd = int(input("Input cmd Number : "))

    return cmd


def select_account(cardInfo):
    print("Your Account list :" )
    for i, account in enumerate(cardInfo.list_account):
        print(f"  {i+1}. {account.name}")
        
    account_num = int(input("Select Account number : "))

    if account_num <= len(cardInfo.list_account) \
        and account_num >= 1:
        return cardInfo.list_account[account_num - 1]
    else :
        return None


def PIN_number(atm, cardInfo_input):
    card = None
    for cardInfo_node in atm.list_CardInfo:
        if cardInfo_node.card_num == cardInfo_input.card_num:
            if cardInfo_node.check_PIN_validataion(cardInfo_input.card_pin):
                card = cardInfo_node
                print(f"PIN validation success")
            else:
                print(f"PIN validation failed")
            break
    else:
        print(f"{cardInfo_input.card_num} not in ATM")

    return card


def do_atm_job(account):
    cmd = ""
    while cmd != 4:
        cmd = print_cmd()
        if cmd == 1:
            print(f"Your {account.name} account Balance : {account.balance}")
        elif cmd == 2:
            amount = int(input("  Input the amount to be deposited : "))
            account.deposit(amount)
            print(f"  Balance after deposit : {account.balance}")
        elif cmd == 3:
            amount = int(input("  Input the amount to be withdrawn : "))
            account.withdraw(amount)
            print(f"  Balance after withdrawal : {account.balance}")
        elif cmd == 4:
            print(f"exit")


def main():
    # setting local ATM
    atm = ATM()

    # test card
    atm.add_test_cardInfo()

    # InsertCard 
    card_num = input("Input Card Number : ")
    card_pin = input("Input PIN Number : ")
    cardInfo_input = CardInfo(card_num, card_pin)

    # PIN number check
    card = PIN_number(atm, cardInfo_input)
    if card == None:
        exit(0)

    # Select Account
    account = select_account(card)
    if account == None:
        print("Wrong account info")
        exit(0)

    # See Balance/Deposit/Withdraw
    do_atm_job(account)
    

if __name__ == "__main__":
    main()
