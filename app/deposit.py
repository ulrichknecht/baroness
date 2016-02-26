import datetime as dt

class Deposit:

    def __init__(self):
        #ID|USERID|AMOUNT|TIME
        self.id = 0
        self.userid = 0
        self.amount = 0.0
        self.time = dt.datetime