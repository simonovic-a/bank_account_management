from models.Bank import Bank
from models.BankAccount import BankAccount

print("1. Create new account.\n"
      "2. Show account info.\n"
      "3. Show all accounts.\n"
      "4. Deposit money\n"
      "5. Transfer money\n"
      "6. Withdraw money\n"
      "7. Show transaction history")

option = None

while option is None or option not in [1, 2, 3, 4, 5, 6]:
    option = int(input("Choose an option: "))

    if option == 1:
        user = BankAccount()
        user.owner = input("Enter owner's full name: ")
        user.balance = input("Enter owner's starting balance: ")
        user.new_account()
        option = None

    elif option == 2:
        user = BankAccount()
        account_id = int(input("Enter owner's ID: "))
        user.account_info(account_id)
        option = None

    elif option == 3:
        user = BankAccount()
        user.all_accounts()
        option = None

    elif option == 4:
        user = BankAccount()
        account_id = int(input("Enter owner's ID: "))
        user.account_info(account_id)
        option = None

    elif option == 5:
        bank = Bank()
        account_id = int(input("Enter account ID: "))
        target_id = int(input("Enter target ID: "))
        amount = int(input("Enter transfer amount: "))
        bank.transfer(account_id, target_id, amount)
        option = None

    elif option == 6:
        user = BankAccount()
        owner_id = int(input("Enter the owner's ID: "))
        money = int(input("Enter the amount to withdraw: "))
        user.withdraw(owner_id, money)
        option = None

    elif option == 7:
        user = BankAccount()
        user.transaction_history()
        option = None
