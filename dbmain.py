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

def create_account(session, account_info, id=None):
    """Create account with a agenerated UUID and stores account_info to accounts table"""
    print("Creating new account")
    account_id = uuid.uuid4()
    acc_inf=account_info.copy()
    del acc_inf['id']
    new_account = Account(id=account_id, **acc_inf)
    print(f"Created account with:\n{account_info}")

    session.add(new_account)
    return account_info['id']

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
        print (field)
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

def get_roach_engine():
    opt = parse_cmdline()
    conn_string = opt.url

    load_dotenv()
    conn_string = os.environ.get('ROACH_CONN_STR')
    
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

if __name__ == '__main__':
    test = {
        "id": uuid.uuid4(),
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
    engine = get_roach_engine()
    
    '''Tests'''
    # Create Test Account 
    test_id = run_transaction(sessionmaker(bind=engine), lambda s: create_account(s, test))
    # Get info from test account
    run_transaction(sessionmaker(bind=engine), lambda s: query_account(s, test_id))
    test["name"] = 'Andrew Xie'
    run_transaction(sessionmaker(bind=engine), lambda s: edit_account(s, test_id, test))
    run_transaction(sessionmaker(bind=engine), lambda s: query_account(s, test_id))
    # Delete account
    run_transaction(sessionmaker(bind=engine), lambda s: delete_accounts(s, [test_id]))