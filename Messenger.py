import mysql.connector
import os
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="messenger")
mycursor = mydb.cursor()
global isAdmin
isAdmin = False

def sendByNumber():
    os.system('cls')
    number = input("enter Number:")
    mycursor.execute('SELECT * FROM users WHERE Phone = %s', (number,))
    result = mycursor.fetchone()
    if result:
        print("Sending Message To "+result[3]+" ("+number+")")
        msg = input("Enter Your Message:")
        mycursor.execute("INSERT INTO messages (sender, receiver, isRead, Text) VALUES (%s, %s, %s, %s)", (OurInfo[1], result[1], False, msg,))
        mydb.commit()
        logged()
    else:
        sendByNumber()

def sendByuser():
    os.system('cls')
    number = input("enter username:")
    mycursor.execute('SELECT * FROM users WHERE username = %s', (number,))
    result = mycursor.fetchone()
    if result:
        print("Sending Message To "+result[3]+" ("+result[5]+")")
        msg = input("Enter Your Message:")
        mycursor.execute("INSERT INTO messages (sender, receiver, isRead, Text) VALUES (%s, %s, %s, %s)", (OurInfo[1], result[1], False, msg,))
        mydb.commit()
        logged()
    else:
        sendByuser()

def AdminMessage():
    os.system('cls')
    msg = input("Enter Your Message:")
    mycursor.execute('SELECT * FROM users')
    result = mycursor.fetchall()
    for x in result:
        if x[1] != OurInfo[1]:
            mycursor.execute("INSERT INTO messages (sender, receiver, isRead, Text) VALUES (%s, %s, %s, %s)", (OurInfo[1], x[1], False, msg,))
            mydb.commit()
            logged()

def UnreadMessages():
    os.system("cls")
    mycursor.execute('SELECT * FROM messages WHERE isRead = 0 AND receiver = %s', (OurInfo[1],))
    result = mycursor.fetchall()
    for x in result:
        mycursor.execute('SELECT * FROM users WHERE username = %s', (x[2],))
        result2 = mycursor.fetchone()
        print("New Message From "+x[1]+" ("+result2[5]+"): Message: ["+x[4]+"]")
        mycursor.execute("UPDATE messages SET isRead = 1 WHERE messageID = %s", (x[0],))
        mydb.commit()
    ch = input("Press Enter To Back")
    logged()

def ReadedMessages():
    os.system("cls")
    mycursor.execute('SELECT * FROM messages WHERE isRead = 1 AND receiver = %s', (OurInfo[1],))
    result = mycursor.fetchall()
    for x in result:
        mycursor.execute('SELECT * FROM users WHERE username = %s', (x[2],))
        result2 = mycursor.fetchone()
        print("Message From "+x[1]+" ("+result2[5]+"): Message: ["+x[4]+"]")
    ch = input("Press Enter To Back")
    logged()

def GetMessages():
    os.system("cls")
    print("1.Unread Messages")
    print("2.Readed Messages")
    ch = int(input("enter option:"))

    if ch == 1:
        UnreadMessages()
    elif ch == 2:
        ReadedMessages()
    else:
        GetMessages()

def logged():
    os.system('cls')
    print("********** You Are Logged In **********")
    print("1.Send Message To Number")
    print("2.Send Message To username")
    print("3.Recieved Messages")
    if isAdmin:
        print("4.Send Message To Everyone")

    ch = int(input("Enter your choice: "))
    if ch == 1:
        sendByNumber()
    elif ch == 2:
        sendByuser()
    elif ch == 3:
        GetMessages()
    elif ch == 4:
        AdminMessage()

def login():
    os.system('cls')
    username = input("Enter username:")
    password = input("Enter password:")
    mycursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
    result = mycursor.fetchone()
    if result:
        global OurInfo
        OurInfo = result
        if result[6] == 1:
            global isAdmin
            isAdmin = True
        logged()
    else:
        login()

def signup():
    os.system('cls')
    username = input("Enter username:")
    password = input("Enter password:")
    name     = input("Enter Your Name:")
    phone    = input("Enter Your Number:")
    age      = int(input("Enter Your Age:"))
    mycursor.execute("INSERT INTO users (username, password, Name, Age, Phone) VALUES (%s, %s, %s, %s, %s)", (username, password, name, age, phone))
    mydb.commit()
    login()

while 1:
    print("********** Messenger App **********")
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Wrong Choice!")