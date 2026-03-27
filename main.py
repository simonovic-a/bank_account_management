from models.BankAccount import BankAccount

print("1. Create new account.\n"
      "2. Show account info.\n"
      "3. Show all accounts.\n"
      "4. Deposit money\n"
      "5. Withdraw money")

option = None
available_options = [1, 2, 3, 4]

while option is None or option not in available_options:
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

    elif option == 3:
        user = BankAccount()
        user.all_accounts()
        option = None

    elif option == 4:
        user = BankAccount()
        owner_id = int(input("Enter the owner's ID: "))
        money = int(input("Enter the amount to deposit: "))
        user.deposit(owner_id, money)
        option = None

    elif option == 5:
        user = BankAccount()
        owner_id = int(input("Enter the owner's ID: "))
        money = int(input("Enter the amount to withdraw: "))
        user.withdraw(owner_id, money)
        option = None
