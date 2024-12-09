import random, string, json, os, subprocess

if os.path.exists("accounts.json") == False: 
        with open("accounts.json",'x+') as f:
            json.dump({},f) 

account_file = open("accounts.json") # opens the json containing the accounts
account_data = json.load(account_file) # assigns the contents json to a variable

def line(): # Prints a line of "=" signs
    for i in range(50): print("=",end="")
    print()   

def clipboard(password): # Takes the given string which puts it into the clipboard
    try: 
        subprocess.run("clip", text=True, input=password) # uses the subprocess module to put the password into the clipboard
        print("Password has been copied to clipboard.")
    except:
        print("Sorry, an error occured while trying to copy the password.")

def encrypt(text): # Encrypts the given text using caesar cipher
    cipher = ""
    for i in text: cipher += chr(ord(i) + 5 )
    return cipher

def decrypt(cipher): # Deciphers the decrypted text 
    deciphered = ""
    for i in cipher: deciphered += chr(ord(i) - 5 )
    return deciphered

def generate_password(): # Generates a random password consisting of upper and lowercase letters, numbers, and symbols
    print("Password generated.")
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(15)])

def check_name(account_name): # Checks the given account name if it contains a special character
    for i in account_name:
        if i.isalpha() or i.isnumeric():
            pass
        else:
            print("Name cannot contain special characters.")
            return False
    
def check_password(password): # Validates the strength of the password (must be longer than 5, must include uppercase, lowercase, and special characters)
    upper_chars, lower_chars, special_char, digits = 0, 0, 0, 0

    if (len(password) < 6): 
        print("Password must be longer than 5 characters.")
        return False # Invalidates the password if the password is too short
    else:
        for i in password: # Checks if the password contains the number of required characters
            if (i.isupper()): upper_chars += 1
            elif (i.islower()): lower_chars += 1
            elif (i.isdigit()): digits += 1
            else: special_char += 1

    if (upper_chars != 0 and lower_chars != 0 and digits != 0 and special_char != 0):
            print("Password strength is valid.")
            return True
    else:
        if (upper_chars == 0):
            print("Password must have an uppercase character.")
            return False
        elif (lower_chars == 0):
            print("Password must have a lowercase character.")
            return False
        elif (special_char == 0):
            print("Password must have a special character.")
            return False
        elif (digits == 0):
            print("Password must have a digit.")
            return False
        
def create_account_name():
    while True:
        account_name = input("Enter account name \n(No special characters and spaces): ")

        if len(account_name) <= 2:
            print("Name is too short, it must be longer than 2.")
            line()
            continue
        elif check_name(account_name) == False: # Calls the check_name function to validate the name
            line()
            continue
        elif encrypt(account_name) in account_data:
            print("Name is already used, try again.")
            line()
            continue
        else: break

    return account_name

def create_password(): # Asks the user for a password and returns the validated password
    while True:
        password = input("Enter password: ")

        if check_password(password) == False: # If the password is not validated, the function will be called again
            line()
            continue
        else: # Once the password is validated, the user will be asked to type it again for confirmation
            password_again = input("Enter password again: ")
            if password != password_again: 
                print("Passwords do not match, try again.")
                line()
                continue # repeats if passwords do not match
            else: break
            
    return password
    
def pass_safe(account_name): # The actual password manager, it takes the account name of the user to open their data
    encrypted_name = encrypt(account_name) 

    if os.path.exists(f"{encrypted_name}.json") == False: # Creates a json file with the encrypted name as a filename
        with open(f"{encrypted_name}.json",'x+') as f:
            json.dump({},f) # An empty dictionary will be written inside this empty json file

    password_file = open(f"{encrypted_name}.json") # opens the json file of the user containing the password data
    password_data = json.load(password_file) # The contents of the json file will be assigned inside the variable
    
    while True:
        line()
        print("1. Create new password" # Menu
            "\n2. Delete password"
            "\n3. Select password"
            "\n4. View passwords"
            "\n5. Logout")
        action = input("Enter choice [1,2,3,4,5]: ")
        line()

        if action == "1": # Create password
            print("\t\tCreate new password")
            line()
            name = input("Name of password: ")
            if encrypt(name) in password_data: # Checks if the given name is already used
                print("Name is already used, try again.")
                continue # If the name is already used, the user will be taken back to the menu

            print("\n1. Create your own password"
                "\n2. Generate random password")
            choice = input("Enter choice [1,2]: ")
            line()

            if choice == "1": # Create your own password
                line()
                print("\t\tReminder:"
                      "\nPassword must be longer than 5 characters. "
                      "\nInclude upper and lowercase letters, "
                      "\nnumbers, and special characters.")
                line()                
                password = create_password()
                print("Password created")
                password_data[encrypt(name)] = encrypt(password) # The encrypted name and password will be inserted in the dictionary
                with open (f"{encrypted_name}.json",'w') as f: json.dump(password_data,f, indent=4) # The dictionary will be written to the json file
            elif choice =="2": # Generate random password
                password = generate_password()
                password_data[encrypt(name)] = encrypt(password)
                with open (f"{encrypted_name}.json",'w') as f: json.dump(password_data,f, indent=4) 
            else: print("Error input.")   
        
        elif action == "2": # Delete password
            print("\t\tDelete password")
            line()
            name = input("Enter password name: ")
            line()
            if encrypt(name) in password_data: # Checks if the password exists in the file
                choice = input("Are you sure you want to delete this password? Y/N: ").upper() 
                if choice == "Y":
                    del password_data[encrypt(name)]
                    with open (f"{encrypted_name}.json",'w') as f: json.dump(password_data,f, indent=4) # Updates the json file with the changes in the dictionary
                    print("Password deleted successfully.")
                elif choice == "N": print("Deletion cancelled.")
            else: print("Password not found.")
        
        elif action == "3": # Select password
            print("\t\tSelect password")
            line()
            name = input("Enter password name: ")
            line()

            if encrypt(name) in password_data:
                print(f"{name}: {decrypt(password_data[encrypt(name)])}") # Prints the selected password with the name
                clipboard(decrypt(password_data[encrypt(name)])) # Calls the clipboard function to copy the password
            else: print("Password not found.")

        elif action == "4": # View passwords
            print("\t\tView Passwords")
            line()
            for name,password in password_data.items(): print(f"{decrypt(name)}: {decrypt(password)}") # Iterates over the items of the dictionary, printing the keys (name) and values (password)
        
        elif action == "5": # Breaks the loop and goes back to the main function
            print("Account will now close...")
            break 
        
def main(): # Contains the login page
    line()
    print("\t      Welcome to Pass-Safe")

    while True: 
        line()
        print("1. Login" # Menu
            "\n2. Create Account"
            "\n3. Delete Account"
            "\n4. Exit")
        choice = input("Enter choice: ")

        if choice == "1": # Login
            line()
            print("\t\t    Login")
            line()

            account_name = input("Account Name: ")
            account_password = input("Account Password: ")
            line()

            encrypted_name = encrypt(account_name) 
            encrypted_password = encrypt(account_password)

            if encrypted_name in account_data: # checks if the encrypted name exists in the dictionary
                if encrypted_password in account_data.values(): # checks the values of the dictionary to find a matching password
                    print("Access Granted.")
                    pass_safe(account_name) # Calls the password manager including the name of the account to access 
                else:
                    print("Password incorrect.")
            else:
                print("Account name not found.")
        
        elif choice == "2": # Create account
            line()
            print("\t\tCreate Account")
            line()

            account_name = create_account_name()
            line()

            print("\t\tReminder:"
                  "\nPassword must be longer than 5 characters. "
                  "\nInclude upper and lowercase letters, "
                  "\nnumbers, and special characters.")
            line()

            account_password = create_password() 

            account_data[encrypt(account_name)] = encrypt(account_password)
            with open ("accounts.json","w") as f:
                json.dump(account_data, f, indent=4)
            print("Account created successfully!")

        elif choice == "3": # Delete Account
            line()
            print("\t\tDelete Account")
            line()
            
            account_name = input("Account Name: ")
            account_password = input("Account Password: ")
            line()

            if encrypt(account_name) in account_data:
                if encrypt(account_password) in account_data.values():
                    choice = input("Are you sure you want to delete your account? Y/N: ").upper()
                    if choice == "Y":
                        del account_data[encrypt(account_name)] # Deletes the account from the dictionary
                        with open ("accounts.json","w") as f: 
                            json.dump(account_data, f, indent=4) # Updates the account dictionary
                            if os.path.exists(f"{encrypt(account_name)}.json"): # Checks if there is an existing json file for the account's data
                                os.remove(f"{encrypt(account_name)}.json") # If the json file exists it is deleted
                        print("Account is deleted successfully.")
                    elif choice == "N": print("Deletion cancelled.")
                    else: print("Error input, try again.")
                else: print("Password incorrect.")
            else: print("Account name not found.")

        elif choice == "4": # Exit
            print("Program will now close...")
            break 
                
if __name__ == "__main__": main()