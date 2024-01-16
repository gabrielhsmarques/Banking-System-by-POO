from abc import ABC, abstractclassmethod, abstractproperty
import logging
logging.basicConfig(level= logging.INFO, filename= "statement.log", format="%(asctime)s - %(message)s")

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def register_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)
        


class Individual(Client):
    def __init__(self, name, date_of_birth, cpf, address):
        super().__init__(address)
        self.name = name
        self.date_of_birth = date_of_birth
        self.cpf = cpf

        logging.info(f"""client created!
                    Name:\t{self.name}
                    Cpf:\t{self.cpf}
                    Date of birth:\t{self.date_of_birth}
                    Address:\t{self.address}""")
        
    def individual_print(self):
        print(f"""client founded!: 
            Name:\t{self.name}
            Cpf:\t{self.cpf}
            Date of birth:\t{self.date_of_birth}
            Address:\t{self.address}
          """)
        


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._statement = StatementBank()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def statement(self):
        return self._statement
    

    def withdrawn(self, value):
        balance = self.balance
        exceeded_balance = value > balance

        if exceeded_balance:
            print("\n Operation failed! You not have balance sufficient. ")

        elif value > 0:
            self._balance -= value
            print("\n Withdrawn has been successful! ")
            return True

        else:
            print("\n Operation failed! The value informed is invalid. ")

        return False

    def deposit(self, value):
        if value > 0:
            self._balance += value
            print("\n Deposit has been successful! ")
        else:
            print("\n Operation failed! The value informed is invalid. ")
            return False

        return True
    
    def account_print(self):
        print(f"""  account(s) of client: 
                    Number: {self.number}
                    Agency: {self.agency}
            """)



class CurrentAccount(Account):
    def __init__(self, number, client, limit=500, limit_of_withdrawals=3):
        super().__init__(number, client)
        self._limit = limit
        self._limit_of_withdrawals = limit_of_withdrawals

    def withdrawn(self, value):
        number_of_withdrawals = len(
            [transaction for transaction in self.statement.transactions if transaction["type"] == Withdrawn.__name__]
        )

        exceeded_limit = value > self._limit
        exceeded_withdrawals = number_of_withdrawals >= self._limit_of_withdrawals

        if exceeded_limit:
            print("\n Operation failed. You have exceeded the limit value. ")

        elif exceeded_withdrawals:
            print("\n Operation failed. You have exceeded the limit of withdrawals ")

        else:
            return super().withdrawn(value)

        return False

    def __str__(self):
        return f"""\
            Owner:\t{self._client.name}
            Agency:\t{self._agency}
            C/C:\t{self._number}
        """


class StatementBank:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
            }
        )


class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass


class Withdrawn(Transaction, Client):
    def __init__(self, value, cpf):
        self._value = value
        self.cpf = cpf
        

    @property
    def value(self):
        return self._value

    def register(self, account):
        transaction_successful = account.withdrawn(self.value)

        if transaction_successful:
            account.statement.add_transaction(self)
            logging.info(f"""Transaction
                        Cpf:\t{self.cpf}
                        withdrawn:\t{self.value}""")


class Deposit(Transaction, Client):
    def __init__(self, value, cpf):
        self._value = value
        self.cpf = cpf

    @property
    def value(self):
        return self._value

    def register(self, account):
        transaction_successful = account.deposit(self.value)

        if transaction_successful:
            account.statement.add_transaction(self)
            logging.info(f"""Transaction
                        Cpf:\t{self.cpf}
                        deposit:\t{self.value}""")