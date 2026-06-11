# CLI-Password-Manager
For this project Ive created a project manager in a Kali Linux VM environment using tools such as Pyerclip, Getpass, Sqlite3, Hashlib, and Base64.
Security Concepts-
-Fernet AES-128-cbc + HMAC = Password encryption
-PBKDF2 = This is for encrypting the hashed master password.
-Salting = Prevents rainbow table attacks
-SQLite3 = This stores the encrypted passwords and credentials.
-Key stretching = This process makes brute force nearly impossible.
BLOCK 1
1. Importing hashlib and getpass into the environment terminal.
•	This will be used to hash the password and hide the password input.
•	Now save.
•	Why we do the imports first is, so we have a solid foundation for Python to read, to avoid (NameError) messages.
2. Defining the master password input using def setup_master_password():
•	Allows users to type their password in.
•	Based on the imports of hashlib and getpass, the original password will then be discarded to prevent it from being stored longer than necessary.
3. Create password input using: password = getpass("enter password:")
1.	import hashlib
2.	import getpass
3.	def setup_master_password():
4.	password = getpass.getpass("Enter password:")
5.	hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
Notes:
•	Import hashlib and getpass function as a foundation for the lines to come, to prevent any error messages from occurring, to allow smooth execution of each line to be added.
•	Line 4 allows users to type their password in, based on the imports of hashlib and getpass, to change it into a hash and hide it, then later discard it to prevent it from being stored longer than necessary.
•	Line 3 is what is used to define the getpass library, its function and its contents.
•	Line 5 then uses line 4 to execute its own code. Hashlib is the library while pbkdf2_hmac is the function that holds SHA256 to then encode the password using password.encode(), and the salt adds the salting to the password which is then repeated 600,000 times making it almost impossible to brute force. 
That's where the discarded password comes in, so all that's left is the hash, which can be used the next time the user logs in, without having to save the readable text in the system and return the hash to memory.
Test 1: Now let's run this block command to ensure everything is working.

Block 2 Now let's import our base64 module to add encryption to passwords stored within the manager, as well as Fernet.
Why:
•	We will be using base64 paired with Fernet to create a key from the master password hash. This way each password stored in this system will have the same key instead of a randomly generated one each time, so you don't lose access to the already stored passwords. And since the key stays the same it can also be used to decrypt the password when needed.

BLOCK 2

	Now that we are done with Block 1, we add the lines for Block 2. In the imports, we add:
•	import base64
•	import os
•	from cryptography.fernet import Fernet
Block 2 — The lines for key encryption:
def get_fernet_key(hash):
•	This just defines that the hash will be used as an encryption key.
Block 2 note:
•	Don't trust verify is why we specify the key cap at [:32], to ensure nothing changes upstream despite pbkdf2 being 32 bytes by default.
•	raw_key = hash[:32]
•	key = base64.urlsafe_b64encode(raw_key)
•	return key
BLOCK 3 
 Here we are creating the SQLite3 database to store the hash and salt for the master password and for the username.
•	con = sqlite3.connect("password_manager.db")
•	cur = con.cursor()
This command allows you to return a cursor object that lets you execute SQL commands and fetch query results in the next lines for the two master and user tables.
•	The IF NOT EXIST is just to create the master table if it doesn't already exist.
Alteration Block 2:
•	raw_key = hashlib.sha256(hashed + salt + b"context").digest()
•	This fixes our previous mistake of not adding salt, making randomization before pointless, and added b"context" to add a domain separation string to ensure the key generated can only be used on this password manager.
BLOCK 4
	Now that we have configured the first 3 blocks let’s do Block 4.
def add_password(username, service, password, key):
•	We know this is just defining what kind of password we are saving.
2. Our second step is to pull the encryption key we created in Block 2 to use on the login and password. For this we use encrypt_password(password, key).
3. As you can see from the screenshot this block is quite similar to Block 3 except for the execute line where we used: "INSERT INTO passwords VALUES (?, ?, ?)"
You may ask why question marks instead of adding the parameters all together as we did in Block 3. This is because Python would run it as one big string, so whatever the user types becomes part of the SQL command itself, which is a vulnerability and can allow for SQL injections. Adding the ? sends the values as sealed data packages instead and the database engine handles it separately.
BLOCK 5
	Similar steps to Block 4.
def get_password(service, key):
•	This just gets the password we added for use and uses the created key to decrypt the password.
2. As for lines 2 and 3 it’s the same as the last 2 blocks.
3. The execution for this block is different of course. Instead, we are using: "SELECT username, password FROM passwords WHERE service = ?", (service,))
•	This just explains what we are specifically requesting, aka the password and username, inside a secure area that holds the service attached to the password. The service in parentheses is the type of service name we want like Minecraft.com or Netflix.com.
4. Next we are going to be using a new command I haven't used yet which is: row = cur.fetchone() — This is used to fetch the next row from the resulted set of a previously executed SQL query. For example, we already created our table in Block 4, this command is just used to fetch it using. 
- if row:
username = row[0]
f = Fernet(key)
decrypted_password = f.decrypt(row[1]).decode()
return username, decrypted_password

- The point of this setup looks complicated
but is extremely easy to understand

In the code logic, the user doesn't input a username to match row[0]. Instead, the user inputs a service name (like Netflix.com), the database finds that row, and then the code automatically extracts whatever username is sitting in row[0] and decrypts the password in row[1].
- return none is just if the info provided
is wrong the output is nothing
BLOCK 6
Set up for the master password using. 
Master_data = get_master_credentials()
This block focuses on the creation of the master password that will access the entire database. If no master password exists, it will then be created based on the code inputs. This section also allows the incorrect password prompt to appear to ensure the correct user is being granted access.
BLOCK 7
	- This block is just the login page setup
using while True:

Print("\n-- Password Manager --")
Print("1. Add a new password")
Print("2. Get existing password")
Print("3. Quit")

choice = Input("Choose an option (1-3):")
-Line 2 for line 2 this is just is just the
blank line of spacing above the
menu just to make it look nicer

-Line 3 is the option that’s given and that you
can choose to add a new password

-Line 4 is were you can request an existing password

-Line 5 is simply how you quit out of the terminal

-Next
we have if choice == "3" goodbye this
is just the output the user would
get for selection option 3

-ss elif

-This provides the outcome for choosing
Option 1, which gives you the option to add
your username, password, and service.

-The add-password(service, username, password, key)
just saves all the data you've entered into the
database and encrypts the password

Choice 2

-This choice is the result of
choosing option 2 just allows you to
Obtain the already added password
with the result = get-password(service, key)
-Lastly, the last few lines are also self-explanatory, just asking to get the information stored in row 0 and 1, which we talked about before, are the username and password row. If the service name provided is correct, print the username and password. If the service is not available, print service not found.
-This fully completes our setup and explanation for this CLI Password Manager.
https://github.com/user-attachments/assets/1ea2afc4-4079-400c-bac2-a3001c505271
 ## Research & Sources:
~Python Official Documentation: hashlib (Secure hashes and message digests)](https://docs.python.org/3/library/hashlib.html) 
~Python Official Documentation: sqlite3 (DB-API 2.0 interface for SQLite databases)](https://docs.python.org/3/library/sqlite3.html) 
~Python Official Documentation: json (JSON encoder and decoder)](https://docs.python.org/3/library/json.html) 
~Fernet Encryption Specification (GitHub/fernet)](https://github.com/fernet/spec/blob/master/Spec.md) 
~Stack Overflow: Simple way to encode a string according to a password](https://stackoverflow.com/) 
~The Python Code: How to Build a Password Manager in Python](https://thepythoncode.com/) * [GeeksforGeeks: SQL Injection Prevention with Parameterized Queries](https://www.geeksforgeeks.org/) 
~GeeksforGeeks: How to Insert If Not Exists in SQL](https://www.geeksforgeeks.org/) 
~GeeksforGeeks: Create a JSON Representation of a Folder Structure](https://www.geeksforgeeks.org/) 
~SQLite Database Security: Best Practices and Techniques](https://sqlite.org/)
