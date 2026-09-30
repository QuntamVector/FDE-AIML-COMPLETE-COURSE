class BankAccount:
    def __init__(self,owner,balance):
        self.owner= owner
        self.__balance = balance
    def deposit(self,amount):
        self.__balance += amount

    def show_balance(self):
        print(f"balance = R{self.__balance}")

    def set_balance(self,balance):

        if balance >=0:
            self.__balance = balance
        else:
            print("Invalid amount")