import sqlalchemy
from sqlalchemy.orm import Session
from data_model import UserAccounts

engine = sqlalchemy.create_engine('sqlite:///data.db', echo=False)


def get_all_accounts(_user_name="", _account_number="", _id="") -> list:
    with Session(autoflush=False, bind=engine) as db:
        if _id != '':
            accounts = db.query(UserAccounts).filter(sqlalchemy.and_(UserAccounts.is_deleted == False,
                                                                     UserAccounts.user_name.ilike(
                                                                         "%{}%".format(_user_name)),
                                                                     UserAccounts.account_number.ilike(
                                                                         "%{}%".format(_account_number)),
                                                                     UserAccounts.id.like(_id))).all()
        else:
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


def create_account(acc):
    with Session(autoflush=False, bind=engine) as db:
        db.add(acc)
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


def update_user_name(_id, new_name):
    with Session(autoflush=False, bind=engine) as db:
        db_user = db.query(UserAccounts).filter(UserAccounts.id == _id).first()
        db_user.user_name = new_name
        db.commit()
