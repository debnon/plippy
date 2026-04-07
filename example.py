
from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError

from StandardUser import StandardUser
from db import SessionLocal, init_db
from models import User


def save_user(user: StandardUser) -> User:
    with SessionLocal() as session:
        db_user = User(name=user.name, funds=user.funds)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


user2 = StandardUser("ben")
print(user2.name)
print(user2.getName())

print(user2.funds)
user2.deposit(Decimal("100.96"))
print(user2.funds)

try:
    init_db()
    saved_user = save_user(user2)
    print(f"Saved user {saved_user.id}: {saved_user.name} with funds {saved_user.funds}")
except SQLAlchemyError as exc:
    print("Database connection failed. Set DATABASE_URL to a running Postgres instance.")
    print(f"Details: {exc.__class__.__name__}: {exc}")

# 1: import ClassName does not work, from ClassName import ClassName does work 
# (importing module rather than class from module?)