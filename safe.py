#starting a simple secured database that is password protected and stores sensitive data.
import sqlite3
from hashlib import sha256
import os


def create_adminpassword(PASSWORD):
    return sha256(PASSWORD.encode('utf-8')).hexdigest()

def check(attempt):
    admin_file = open('admin.txt', 'r')
    PASSWORD = admin_file.read()
    attempt = sha256(attempt.encode('utf-8')).hexdigest()

    if attempt == PASSWORD:
        return True
    else:
        return False

def adminfile():
    file_exists = os.path.isfile('admin.txt')

    if not file_exists:
        if os.path.exists('password_manager.db'):
            os.remove('password_manager.db')
        admin_p = input('create your ADMIN password? \n')
        admin_file = open('admin.txt', 'w')
        admin_file.write(create_adminpassword(admin_p))
        return 
    else:
        admin_file = open('admin.txt', 'r')
        return admin_file.read()

    


def create_password(pass_key, service, admin_pass, passw = ''):
    return sha256(passw.encode('utf-8') + admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]


def get_HexKey(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_HexKey(admin_pass, service)
    cursor = conn.execute("SELECT * FROM KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    pass_key = ""
    for row in cursor:
        pass_key = row[0]
    
    return create_password(pass_key, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_HexKey(admin_pass, service)
    command = ('INSERT OR IGNORE INTO KEYS (PASS_KEY) VALUES (' +  ('"' + secret_key + '"') + ');')
    conn.execute(command)
    conn.commit()

    return create_password(secret_key, service, admin_pass)




adminfile()

connect = input("What is your ADMIN password?: \n")

while check(connect) == False:
    check(connect)
    connect = input("Please enter your password again: \n" )
    if connect == 'q':
        break
    
conn = sqlite3.connect('password_manager.db')

try:
    conn.execute('''CREATE TABLE KEYS 
    (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
    print("YOUR SAFE HAS BEEN CREATED!\nWhat would you like to store in it today?")
except:
    print('you have a safe.')

while True:
    print('-'*15)
    print('HERE ARE YOUR OPTIONS:')
    print('-'*15)
    print('q: to quit\nstore: to store passwords\nget: to get passwords\n')
    print('-'*15)
    action = input('~ ')

    action = action.lower()
    if action == 'q':
        break
    elif action == 'store':
        service = input('what is the service that you are creating a password for?\n')
        print("\n" + service.capitalize() + "password created: \n" + add_password(service, connect))
    elif action == 'get':
        service = input('what service are you trying to get the password to?\n')
        print("\n" + service.capitalize() + "password\n" + get_password(connect, service))
        
