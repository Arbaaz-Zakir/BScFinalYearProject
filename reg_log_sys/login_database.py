from pymongo import MongoClient
from difflib import SequenceMatcher 

client = MongoClient("mongodb://localhost:27017/")
db = client.blockchain
#post_ex = {"_id": 0,
#           "firstname": "Arbaaz",
#           "lastname": "Zakir",
#           "username": "az16aan",
#           "Reputation": 0,
#           "karma": 0}
#db.user.insert_one(post_ex)

#print("welcome to blockchain music temporary data storage system, what would you like to do today?")
#print(db.users.find({"_id": 0}))
global session
global id_num
#while state != 'exit':
 #   tmp.show_cmds()


class Temp:
    def show_cmds(self):
        print("[L] login\n")
        print("[R] register\n")
        print("[A] add new song\n")
        print("[E] exit\n")
        print("[C] show commands\n")


    def login(self, username, passwd):
        users = db.users
        login_user = users.find_one({'username': username})
        
        if login_user:
            if login_user["password"] == passwd:
                session = username
                print ('welcome back: ' + session)
                
        print('invalid user/password')
    
    def register(self):
        num = 0
        fname = input("enter first name:\n")
        lname = input("enter last name:\n")
        username = input("enter user name:\n")
        password = input("enter password:\n")
        reputation = 0
        karma = 0
        
        users = db.users
        existing_user = users.find_one({'username': username})
        if existing_user:
            print('username taken')
        
        else: 
            db.user.insert_one({ "firstname":fname,
                                 "lastname":lname,
                                 "username":username,
                                 "password":password,
                                 "Reputation": reputation, 
                                 "karma":karma})
    
            print('regestration sucessful')
            


#if __name__ == '__main__':     
tmp = Temp()
tmp.show_cmds()
#userin = input("command\n")
state= 'cmd'
while state is not 'exit':
    userin = input("Input command: ")
    if userin == 'R' or userin =='r':
        tmp.register()  
        
    elif userin == 'L' or userin =='l':
        given_username = input("enter username: ")
        given_password = input("enter password: ")
        tmp.login(given_username, given_password)
        
    elif userin == 'C' or userin =='c':
        tmp.show_cmds()
    
    elif userin == 'E' or userin =='e':
        print("thank you, goodbye")
        state = 'exit'
        
        
        
        
        