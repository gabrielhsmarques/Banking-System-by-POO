from classes import Client, Individual, Account, CurrentAccount, StatementBank, Transaction, Withdrawn, Deposit
import logging
logging.basicConfig(level= logging.INFO, filename= "statement.log", format="%(asctime)s - %(message)s")

def fun_menu():

    menu = """
    ==========Welcome to your bank==========
    
    Menu of the options:

    [cc] Create client
    [ca] Create account
    [d] Deposit
    [w] Withdraw 
    [e] Extract
    [g] Get client
    [dl] Delete client
    [q] Quit
    => """
    return input(menu)

def filter_client(cpf, clients):
    clients_filtereds = [client for client in clients if client.cpf == cpf]
    return clients_filtereds[0] if clients_filtereds else None


def recover_account_client(client):
    if not client.accounts:
        return
    else:
        return client.accounts[0]

def create_client(clients):
    cpf = input("Insert the CPF (just number): ")
    client = filter_client(cpf, clients)

    if client != None:
        print("\n CPF has been registered! ")
        return

    name = input("Insert your full name: ")
    date_of_birth = input("Insert your date_of_birth (dd-mm-aaaa): ")
    address = input("Insert your address (street, number - neighborhood - city/state abbreviations ): ")

    client = Individual(name=name, date_of_birth=date_of_birth, cpf=cpf, address=address)
    
    clients.append(client)
    

    print("\n Client has been created successful! ")

def create_account(clients,number_account, accounts):
    cpf = input("Insert the CPF of the client: ")
    client = filter_client(cpf, clients)
    account = recover_account_client(client)

    if client == None:
        print("\n Client has not founded! The criation process has been closed ")
        return
    
    elif not account:
        account = CurrentAccount.new_account(client = client, number = number_account)
        accounts.append(account)
        client.accounts.append(account)

        logging.info(f"""Account created
                        Number:\t{account.number}
                        Agency:\t{account.agency}
                    """)

        print("\n Account has been created successful! ")
    
    else:
        print("\n Cpf has been registered in other account! ")


def deposit(clients):
    cpf = input("Insert the cpf of the client: ")
    client = filter_client(cpf, clients)

    if client == None:
        print("\n Client was not founded! ")
        return

    value = float(input("Insert the value of the deposit: "))
    transaction = Deposit(value, cpf)

    account = recover_account_client(client)
    if account == None:
        print("\n Client does not have an account! ")
        return

    client.register_transaction(account, transaction)


def withdrawn(clients):
    cpf = input("Insert the cpf of the client: ")
    client = filter_client(cpf, clients)
    
    if client == None:
        print("\n Client was not founded! ")
        return

    value = float(input("Insert the value of the withdrawn: "))
    transaction = Withdrawn(value, cpf)

    account = recover_account_client(client)

    if account == None:
        print("\n Client does not have an account! ")
        return
   
    client.register_transaction(account, transaction)


def view_extract(clients):
    cpf = input("Insert the cpf of the client: ")
    client = filter_client(cpf, clients)

    if client == None:
        print("\n Client was not founded! ")
        return

    account = recover_account_client(client)
    if account == None:
        print("\n Client does not have an account! ")
        return

    print("\n ========== STATEMENT ========== ")
    transactions = account.statement.transactions

    extract = ""
    if transactions == None:
        extract = " There has been not transactions. "
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\n\t${transaction['value']:.2f}"

    print(extract)
    print(f"\t\nBalance:\n\t${account.balance:.2f}")



def delete_clients(clients, accounts):
    cpf = input("Insert the cpf of the client delete: ")
    client = filter_client(cpf, clients)

    if client == None:
        print("Error! Client has not founded!")
    else:
        print("\nClient has founded! Do you have sure want to remove it?\n")
        remove = input("Y or N:\t")
        if remove == "Y":
            clients.remove(client)
            account = recover_account_client(client)

            if account == None:
                print("Client does not have an account!\n")
            else:
                accounts.remove(account)

                logging.info(f"""Client canceled!
                                Cpf:\t{client.cpf}
                                Name:\t{client.name}
                                Number of account:\t{account.number}
                                Agency:\t{account.agency}
                            """)
            
            return print(f"Client deleted successfully!\n")

            
        else:
            print("Operation canceled!")

def get_client(clients, accounts):
    cpf = input("Insert cpf of the client to search for: ")
    client = filter_client(cpf, clients)
                                
    if client == None:
        print("\nSorry, client has not founded!")
    else:
        Individual.individual_print(client)

        account = recover_account_client(client)

        for account in accounts:
            if account != None:
                Account.account_print(account)

def main():
    clients = []
    accounts = []

    while True:
        option = fun_menu()

        if option == "cc":
            create_client(clients)
        
        elif option == "ca":
            number_account = len(accounts) + 1
            create_account(clients, number_account, accounts)

        elif option == "d":
            deposit(clients)
          
        elif option == "w":
            withdrawn(clients)
        
        elif option == "e":
            view_extract(clients)
            
        elif option == "cc":
            create_client(clients)
            
        elif option == "dl":
            delete_clients(clients, accounts)
            
        elif option == "g":
            get_client(clients, accounts)

        elif option == "q":
            break

        else:
            print("Invalid Operation. Please, reselect the desired operation")
if __name__ == "__main__":
    main()    