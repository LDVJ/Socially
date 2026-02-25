def add(num1: int = 5, num2 : int = 2):
    return num1 + num2

class BankBalance():
    def __init__(self, balance = 0): #constructor function of the BankBalance object
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdrawl(self, amount):
        self.balance -= amount
        return self.balance

    def inc_inteest(self, rate):
        self.balance + (self.balance*rate)
        return self.balance
    