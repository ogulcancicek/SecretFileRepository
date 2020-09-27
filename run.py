import base64
import sqlite3

password = "123456"



passw = input("Passoword:")


if (passw == password):
    db = sqlite3.connect("safe.db")
    try:
        db.execute("CREATE TABLE safe (fullname TEXT NOT NULL,filetype TEXT NOT NULL,filecontent TEXT NOT NULL)")
        print("Your safe table has been created.")
    except:
        print("You have alreay a safe table.")



    while True:
        print("""
s - store a file 
o - open a file 
d - delete a file
q - exit
        """)
        rsp = input("Operation: ")

        if rsp == "q":
            db.close()
            break

        elif rsp == "s":
            PATH = input("Type in full path of the file(Example: /Users/ogulcan/Desktop/image.jpg):")
            filename = input("Filename:")
            filetype = input("Filetype:")
            FULLNAME = filename + "." + filetype
            with open(PATH,"rb") as f:
                binary = f.read()
            encrypted_file_string = base64.b64encode(binary).decode("utf-8")
            
            db.execute("Insert into safe (fullname,filetype,filecontent) VALUES (?,?,?)",(FULLNAME,filetype,encrypted_file_string))
            db.commit()

        elif rsp == "o":
            filetype = input("Filetype:")
            filename = input("Filename:")
            FULLNAME = filename + "." + filetype

            cursor = db.execute("Select * From safe Where fullname = ?",(FULLNAME,))

            for row in cursor:
                file_binary = row[2].encode()

            with open(FULLNAME,"wb") as f:
                f.write(base64.b64decode(file_binary))
        
        elif rsp == "d":
            filetype = input("Filetype:")
            filename = input("Filename:")
            FULLNAME = filename + "." + filetype

            db.execute("Delete From safe Where fullname = ?",(FULLNAME,))
            db.commit()

else:
    print("Invalid username or password. Please try again.")



