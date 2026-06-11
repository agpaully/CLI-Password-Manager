import hashlib
import getpass
import base64
import os
import sqlite3
from cryptography.fernet import Fernet

def setup_master_password():
    password = getpass.getpass("Create your Master Password: ")
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
    
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("INSERT INTO master VALUES (?, ?)", (hashed, salt))
    con.commit()
    con.close()
    del password

def get_master_credentials():
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("SELECT hash, salt FROM master LIMIT 1")
    row = cur.fetchone()
    con.close()
    return row if row else None

def verify_and_get_key(input_password, stored_hash, salt):
    test_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 600000)
    if test_hash == stored_hash:
        raw_key = hashlib.sha256(test_hash + salt + b"password_manager").digest()
        return base64.urlsafe_b64encode(raw_key)
    return None

def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode())

def decrypt_password(password, key):
    return Fernet(key).decrypt(password).decode()

def setup_database():
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS master(hash BLOB, salt BLOB)")
    cur.execute("CREATE TABLE IF NOT EXISTS passwords(service TEXT, username TEXT, password BLOB)")
    con.commit()
    con.close()

def add_password(service, username, password, key):
    encrypted = encrypt_password(password, key)
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, username, encrypted))
    con.commit()
    con.close()

def get_password(service, key):
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM passwords WHERE service = ?", (service,))
    row = cur.fetchone()
    con.close()
    if row:
        username = row[0]
        try:
            decrypted_password = decrypt_password(row[1], key)
            return username, decrypted_password
        except Exception:
            return None
    return None

setup_database()

master_data = get_master_credentials()

if not master_data:
    print("Hey<3 set up your Master Password.")
    setup_master_password()
    print("Master Password set successfully! Restarting script...")
    exit()
else:
    stored_hash, stored_salt = master_data
    while True:
        master_input = getpass.getpass("Enter Master Password to unlock: ")
        key = verify_and_get_key(master_input, stored_hash, stored_salt)
        if key:
            print("Database unlocked successfully<3")
            break
        else:
            print("Incorrect password. Try again.")

  while True:
    print("\n--- Password manager ---")
    print("1. Add a new password")
    print("2. Get an existing password")
    print("3. Quit")
    choice = input("Choose an option (1-3): ")

    if choice == "3":
        print("Goodbye!")
        break

    elif choice == "1": 
        service = input("Enter service name: ")  
        username = input("Enter username: ") 
        password = input("Enter password: ")
        add_password(service, username, password, key)
        print("Password saved successfully<3")

    elif choice == "2": 
        service = input("Enter service name: ")
        result = get_password(service, key)
        if result:
            print(f"Username: {result[0]}")
            print(f"Password: {result[1]}")
        else:
            print("Service not found or key invalid.")    
