import sqlalchemy
from sqlalchemy.orm import Session
from data_model import UserAccounts

engine = sqlalchemy.create_engine('sqlite:///data.db', echo=False)


def get_all_accounts(_user_name="", _account_number="") -> list:
    with Session(autoflush=False, bind=engine) as db:
        accounts = db.query(UserAccounts).filter(sqlalchemy.and_(UserAccounts.is_deleted == False,
                                                                 UserAccounts.user_name.ilike(
                                                                     "%{}%".format(_user_name)),
                                                                 UserAccounts.account_number.ilike("%{}%".format(_account_number)))).all()
    free_list = []
    for i in accounts:
        i = i.__dict__
        del i['_sa_instance_state']
        free_list.append(i)
    return free_list


def create_account(task):
    with Session(autoflush=False, bind=engine) as db:
        db.add(task)
        db.commit()


def delete_account(_id):
    with Session(autoflush=False, bind=engine) as db:
        db_account = db.query(UserAccounts).filter(
            UserAccounts.id == _id).first()
        if db_account is not None:
            db_account.is_deleted = True
            db.commit()


def change_balance(_id, take_or_put, amount):
    if take_or_put.lower() == 'take':
        with Session(autoflush=False, bind=engine) as db:
            db_account = db.query(UserAccounts).filter(
                UserAccounts.id == _id).first()
            if db_account is not None:
                db_account.balance -= amount
                db.commit()
    else:
        with Session(autoflush=False, bind=engine) as db:
            db_account = db.query(UserAccounts).filter(
                UserAccounts.id == _id).first()
            if db_account is not None:
                db_account.balance += amount
                db.commit()


def send_to(_id_sender, _id_taker, amount):
    with Session(autoflush=False, bind=engine) as db:
        db_sender = db.query(UserAccounts).filter(
            UserAccounts.id == _id_sender).first()
        db_taker = db.query(UserAccounts).filter(
            UserAccounts.id == _id_taker).first()
        if db_sender is not None and db_taker is not None:
            db_sender.balance -= amount
            db_taker.balance += amount
            db.commit()


send_to(1, 8, 50)

send_to(2, 3, 30)
