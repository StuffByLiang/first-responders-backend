from argparse import ArgumentParser
from math import floor
import os
import random
import uuid
import urllib.parse
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from models import Account

# The code below inserts new accounts.

<<<<<<< HEAD
=======

def create_accounts(session, num):
    """Create N new accounts with random account IDs and account balances."""
    print("Creating new accounts...")
    new_accounts = []
    while num > 0:
        account_id = uuid.uuid4()
        account_balance = floor(random.random() * 1_000_000)
        new_accounts.append(Account(id=account_id, balance=account_balance))
        seen_account_ids.append(account_id)
        print(
            "Created new account with id {0} and balance {1}.".format(
                account_id, account_balance
            )
        )
        num = num - 1
    session.add_all(new_accounts)


>>>>>>> f8883b7e7a80106063c6a40104b3e180c86f06de
def create_account(session, account_info, id=None):
    """Create account with a agenerated UUID and stores account_info to accounts table"""
    print("Creating new account")
    account_id = uuid.uuid4() if id is None else id
    new_account = Account(id=account_id, **account_info)
    print(f"Created account with:\n{account_info}")

    session.add(new_account)
    return account_id


def query_account(session, id, fields=None):
    """get fields of account with id"""
    account = session.query(Account).filter(Account.id == id).first()
    print(f"Accessed account of {account.name}")
    # print(account.name, account['age'], account.get_fields())
    return account.get_fields(fields)

def edit_account(session, id, account_info):
    """Edit account with id for the given fields in account_info
    """
    account = session.query(Account).filter(Account.id == id).first()
    for field in account_info.keys():
        account[field] = account_info[field]


def delete_accounts(session, ids):
    """Delete account with primary ids in ids"""
    print("Deleting existing accounts...")
    accounts = session.query(Account).filter(Account.id.in_(ids)).all()

    for account in accounts:
        print("Deleted account {0}.".format(account.id))
        session.delete(account)


def parse_cmdline():
    parser = ArgumentParser()
    parser.add_argument("--url", help="Enter your node's connection string\n")
    opt = parser.parse_args()
    return opt

<<<<<<< HEAD
def get_roach_engine():
    opt = parse_cmdline()
    conn_string = opt.url
=======

def get_roach_engine(conn_string):
>>>>>>> f8883b7e7a80106063c6a40104b3e180c86f06de
    try:
        db_uri = os.path.expandvars(conn_string)
        db_uri = urllib.parse.unquote(db_uri)

        psycopg_uri = (
            db_uri.replace("postgresql://", "cockroachdb://")
            .replace("postgres://", "cockroachdb://")
            .replace("26257?", "26257/htn?")
        )
        print(psycopg_uri)
        # The "cockroachdb://" prefix for the engine URL indicates that we are
        # connecting to CockroachDB using the 'cockroachdb' dialect.
        # For more information, see
        # https://github.com/cockroachdb/sqlalchemy-cockroachdb.
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print("Failed to connect to database.")
        print("{0}".format(e))
    return engine

<<<<<<< HEAD
if __name__ == '__main__':
=======

if __name__ == "__main__":
    # load_dotenv()
    # conn_string = os.environ.get("COCKROACHDB_CONN_STRING")

>>>>>>> f8883b7e7a80106063c6a40104b3e180c86f06de
    test = {
        "name": "Annie Liu",
        "age": 20,
        "address": "2205 Lower Mall",
        "emergency_contact": "Linda Ma",
        "allergies": "peanut,apples,oranges",
        "blood_type": "AB",
        "conditions": "diabetes",
        "medications": "asprin,insulin",
        "bmi": 3,
        "height": 165,
        "weight": 50,
    }

    # For CockroachCloud:
    # postgres://<username>:<password>@<globalhost>:26257/<cluster_name>.defaultdb?sslmode=verify-full&sslrootcert=<certs_dir>/<ca.crt>
<<<<<<< HEAD
    engine = get_roach_engine()
    
    '''Tests'''
    # Create Test Account 
    test_id = run_transaction(sessionmaker(bind=engine), lambda s: create_account(s, test))
=======
    engine = get_roach_engine(conn_string)

    """Tests"""
    # Create Test Account
    test_id = run_transaction(
        sessionmaker(bind=engine), lambda s: create_account(s, test)
    )
>>>>>>> f8883b7e7a80106063c6a40104b3e180c86f06de
    # Get info from test account
    run_transaction(sessionmaker(bind=engine), lambda s: query_account(s, test_id))
    # Delete account
    run_transaction(sessionmaker(bind=engine), lambda s: delete_accounts(s, [test_id]))