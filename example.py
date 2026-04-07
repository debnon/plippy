
from decimal import Decimal

from StandardUser import StandardUser


user2 = StandardUser()
print(user2.name)
user2.getName()
print(user2.getName())

print(user2.funds)
user2.deposit(Decimal("100.96"))
print(user2.funds)

# 1: import ClassName does not work, from ClassName import ClassName does work 
# (importing module rather than class from module?)