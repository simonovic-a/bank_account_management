from models.Db import Db


class BankAccount(Db):

    def __init__(self):
        super().__init__()
        self.__owner = None
        self.__balance = None

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, new_name):
        split_name = new_name.split()
        if len(split_name) < 2:
            raise ValueError("Name must contain first and last name.")
        self.__owner = split_name

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, money):
        self.__balance = money

    def new_account(self):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("INSERT INTO accounts (owner, balance) VALUES (%s, %s)",
                       (self.__owner, self.__balance))
        con.commit()
        cursor.close()

    def account_info(self, account_id):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT * from accounts WHERE id = %s", (account_id,))
        info = cursor.fetchone()
        owner_id = info["id"]
        owner = info["owner"]
        balance = info["balance"]
        print(f"ID: {owner_id} | Name: {owner} | Balance: {balance}")

    def all_accounts(self):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM accounts")
        all_accounts = cursor.fetchall()
        for account in all_accounts:
            owner_id = account["id"]
            owner = account["owner"]
            balance = account["balance"]
            print(f"Owner ID: {owner_id} | Name: {owner} | Balance: {balance}")

    def deposit(self, owner_id, money):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (owner_id,))
        result = cursor.fetchone()

        if result is None:
            print("Account not found.")
            return

        current_balance = result["balance"]
        new_balance = current_balance + money

        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, owner_id))
        con.commit()
        cursor.close()

        print(f"Successfully deposited {money}. New balance: {new_balance}")

    def withdraw(self, owner_id, money):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE id=%s", (owner_id,))
        result = cursor.fetchone()

        if result is None:
            print("Account not found.")
            return

        current_balance = result["balance"]

        new_balance = current_balance - money

        if new_balance < 0:
            print(f"Insufficient funds. Your balance is {current_balance}")
            return

        cursor.execute("UPDATE accounts SET balance = %s where id = %s", (new_balance, owner_id))
        print(f"Successfully withdrew {money}. New balance: {new_balance}")
