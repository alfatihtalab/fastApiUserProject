from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

database_name = "userdb"
database_path = "postgresql://{}:{}@{}/{}".format('postgres', '1773237*', 'localhost:5432', database_name)
engine = create_engine(database_path)
session = Session(engine)


def setup_db():
    SQLModel.metadata.create_all(engine)
    create_accounts()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    email: Optional[str] = None
    account_id: int = Field(default=None, foreign_key="account.id")

    def insert(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class AccountType(str, Enum):
    developer = "developer"
    admin = "admin"
    simple = "simple"


class Account(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    type: AccountType


class Item(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    price: float
    category_id: str = Field(default=None, foreign_key="category.id")

    def insert(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str

    def insert(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


def create_accounts():
    with Session(engine) as session:
        statement = select(Account)
        result = session.exec(statement)
        print(result.all() )
        if not result:
            acc1 = Account(id=1001, type=AccountType.developer)
            acc2 = Account(id=1002, type=AccountType.admin)
            acc3 = Account(id=1003, type=AccountType.simple)
            session.add_all([acc1, acc2, acc3])
            session.commit()
        else:
            session.close()
            print('ok')
