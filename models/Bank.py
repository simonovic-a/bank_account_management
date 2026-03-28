from datetime import datetime

from models.Db import Db


class Bank(Db):

    def __init__(self):
        super().__init__()

    def transfer(self, account_id, target_id, amount):
        con = self._get_connection()
        cursor = con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        account_balance = cursor.fetchone()

        if account_balance["balance"] < amount:
            print("Insufficient funds.")
            return

        new_balance = account_balance["balance"] - amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))

        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (target_id,))
        target_balance = cursor.fetchone()
        new_balance = target_balance["balance"] + amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, target_id))

        transaction_time = datetime.now()
        cursor.execute("INSERT INTO transaction_history (account_id, type, amount, target_account, created_at) "
                       "VALUES (%s, %s, %s, %s, %s)", (account_id, "Transfer", amount, target_id, transaction_time))
        print(f"Transfer successful: {amount} transferred from account {account_id} to account {target_id}.")
        con.commit()
        cursor.close()
