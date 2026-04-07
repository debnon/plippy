
from StandardUser import StandardUser


userDict: dict = dict()
def createUser(username: str, funds: int):
    
    if userDict.get(username) is not None:
        print("This user is already present")
        return
    
    userDict[username] = funds

def updateUser(username: str, funds: int):

    if userDict.get(username) is None: 
        print("This user does not exist")
        return

    userDict[username] = funds

createUser("chloe", 10)
createUser("ben", 11)
createUser("ben", 11)
updateUser("ben", 20)

print(userDict["chloe"])
print(userDict["ben"])

# class User:

#     self.User()

#     self.__init__()

user1 = StandardUser('hello')
print(user1.name)

user2 = StandardUser()
print(user2.name)
user2.getName()
print(user2.getName())
# user.User()
# User.User()

# 1: import ClassName does not work, from ClassName import ClassName does work 
# (importing module rather than class from module?)