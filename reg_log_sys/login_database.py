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


#music_post = {"title": 0,
#           "artist": "Arbaaz",
#           "writer": "Zakir",
#           "username": "az16aan",
#           "others": 0}


#print("welcome to blockchain music temporary data storage system, what would you like to do today?")
#print(db.users.find({"_id": 0}))
session = ""
global id_num


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
                global session 
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
        elif fname is "" or lname is "" or username is "" or password is "":
            print("failed to input 1 or more appropriate fields!")
        else: 
            db.user.insert_one({ "firstname":fname,
                                 "lastname":lname,
                                 "username":username,
                                 "password":password,
                                 "Reputation": reputation, 
                                 "karma":karma})
    
            print('registration successful')
            
        
    def add_song(self):
        global session
        music = db.music
        music_title = input("input new title:\n")
        new_lyrics = input("input new lyrics:\n")
        artist = input("input new writer:\n")
        writer = input("input new writer:\n")
        
        index = -1
        other_state = "add new"
        others = ["","","","","","",""]
        while other_state is not "done":
            other_inputs = input("input new others to credit:\n") # loop array
            if other_inputs == "done":
                other_state = "done"
                
            index+=1
            others[index] ==[other_inputs]
        infringement = []
        it_lyrics = music.find({"lyrics"})
        if music.count() != 0:
            for lyrics in it_lyrics:
                to_compare = lyrics["lyrics"]
                similarity_percent = lyrics_similarity(new_lyrics, to_compare)
            
                if similarity_percent > 0.50:
                    infringement.append([lyrics["username"], lyrics["title"], similarity_percent])
                
        db.music.insert_one({ "lyrics": new_lyrics,
                              "title": music_title,
                              "artist": artist,
                              "writer": writer,
                              "username": session,
                              "others": others,
                              "infringement": infringement})
        
        
    def lyrics_similarity(song1, song2):
        return SequenceMatcher(None, song1, song2).ratio()
        

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
        
    elif userin == 'A' or userin =='a':
        tmp.add_song()
        
        
        