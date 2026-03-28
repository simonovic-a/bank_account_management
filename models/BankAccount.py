from datetime import datetime

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
        self.__owner = " ".join(split_name)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        self.__balance = amount

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

    def deposit(self, owner_id, amount):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (owner_id,))
        result = cursor.fetchone()

        if result is None:
            print("Account not found.")
            return

        current_balance = result["balance"]
        new_balance = current_balance + amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, owner_id))

        transaction_time = datetime.now()
        cursor.execute("INSERT INTO transaction_history (account_id, type, amount, created_at) VALUES (%s, %s, %s, %s)",
                       (owner_id, "Deposit", amount, transaction_time))
        con.commit()

        cursor.close()

        print(f"Successfully deposited {amount}. New balance: {new_balance}")

    def withdraw(self, owner_id, amount):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE id=%s", (owner_id,))
        result = cursor.fetchone()

        if result is None:
            print("Account not found.")
            return

        current_balance = result["balance"]

        new_balance = current_balance - amount

        if new_balance < 0:
            print(f"Insufficient funds. Your balance is {current_balance}")
            return

        cursor.execute("UPDATE accounts SET balance = %s where id = %s", (new_balance, owner_id))

        transaction_time = datetime.now()
        cursor.execute("INSERT INTO transaction_history (account_id, type, amount, created_at) VALUES (%s, %s, %s, %s)",
                       (owner_id, "Withdraw", amount, transaction_time))

        print(f"Successfully withdrew {amount}. New balance: {new_balance}")

    def transaction_history(self):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM transaction_history")
        transactions = cursor.fetchall()
        con.commit()
        cursor.close()
        for transaction in transactions:
            print(
                f"Transaction ID: {transaction["id"]} | Account ID: {transaction["account_id"]} | Type: {transaction["type"]}"
                f" | Amount: {transaction["amount"]} | Target account: {transaction["target_account"]} | Created at: {transaction["created_at"]}")
