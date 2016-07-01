import sqlite3
from flask import g
from app import app
from user import User
from product import Product
from consumption import Consumption
from deposit import Deposit
import random as rand
import datetime
from settings import settings
import logging

DATABASE = 'test/database.db'

def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    closeflag = False
    try:
        db = get_db()
    except RuntimeError:
        logging.info("GUI DB access")
        db = sqlite3.connect(DATABASE)
        closeflag = True

    logging.info("Database query: " + str(query) + " args: " + str(args))
    cur = db.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    if closeflag is True:
        db.close()

    return (rows[0] if rows else None) if one else rows

def get_user(u):
    row = query_db("SELECT * FROM USERS WHERE NAME = ?", [u.name], one=True)
    u = User()
    if row is None:
        return None
    u.id=row[0]
    u.name=row[1]
    u.password=row[2]
    u.longname=row[3]
    u.email=row[4]
    u.isblack=row[5]
    u.isbaron=row[6]
    u.isshown=row[7]
    u.autoblack=row[8]
    u.onlyrfid=row[9]
    u.rfid_id = get_rfid_ids_by_userid(u.id)
    logging.info(u)
    return u

def get_user_by_name(name):
    row = query_db("SELECT * FROM USERS WHERE NAME = ?", [name], one=True)
    u = User()
    if row is None:
        return None
    u.id=row[0]
    u.name=row[1]
    u.password=row[2]
    u.longname=row[3]
    u.email=row[4]
    u.isblack=row[5]
    u.isbaron=row[6]
    u.isshown=row[7]
    u.autoblack=row[8]
    u.onlyrfid=row[9]
    logging.debug(u)
    u.rfid_id = get_rfid_ids_by_userid(u.id)
    return u

def get_user_by_id(id):
    row = query_db("SELECT * FROM USERS WHERE ID = ?", [id], one=True)
    u = User()
    if row is None:
        return None
    u.id=row[0]
    u.name=row[1]
    u.password=row[2]
    u.longname=row[3]
    u.email=row[4]
    u.isblack=row[5]
    u.isbaron=row[6]
    u.isshown=row[7]
    u.autoblack=row[8]
    u.onlyrfid=row[9]
    u.rfid_id = get_rfid_ids_by_userid(u.id)
    logging.debug(u)
    return u

def get_user_by_rfid(rfidid):
    row = query_db("SELECT * FROM rfid WHERE RFID_ID = ?", [rfidid], one=True)
    if row is None:
         return None
    u = get_user_by_id(row[1])
    logging.debug(u)
    return u

def get_users():
    rows = query_db("SELECT * FROM USERS")
    users = []
    for row in rows:
        u = User()
        u.id=row[0]
        u.name=row[1]
        u.password=row[2]
        u.longname=row[3]
        u.email=row[4]
        u.isblack=row[5]
        u.isbaron=row[6]
        u.isshown=row[7]
        u.autoblack=row[8]
        u.onlyrfid=row[9]
        u.rfid_id = get_rfid_ids_by_userid(u.id)
        users.append(u)
    return users


def add_user(u):
    query_db("INSERT INTO USERS (NAME, PASSWORD, LONGNAME, EMAIL) VALUES (? ,? ,?, ?)", (u.name, u.password, u.longname, u.email))
    user_id = get_user_by_name(u.name).id
    set_rfid_to_userid(u.rfid_id, user_id)
    get_db().commit()

def get_rfid_ids_by_userid(user_id):
    rows = query_db("SELECT * FROM Rfid WHERE userid = ?", [user_id])
    rfid_ids = []
    for row in rows:
        rfid_ids.append(row[2])
    return rfid_ids

def set_rfid_to_userid(rfid_ids, user_id):
    new_rfids = rfid_ids.replace(" ","").split(";")

    for rfid_id in new_rfids: # add new rfid_ids
        u = get_user_by_rfid(rfid_id)
        if not u: #rfid id is not assigned to a user, so it should be added
             add_rfid_id(rfid_id, user_id)

    for old_rfid in get_rfid_ids_by_userid(user_id):
        if old_rfid not in new_rfids:
            query_db("DELETE FROM Rfid WHERE rfid_id = ?", (old_rfid, ))


def add_rfid_id(rfid_id, userid):
    rfid_id = rfid_id.lower();
    query_db("INSERT INTO Rfid (userid, rfid_id) values (?, ?)", (userid, rfid_id))

def update_user(u):
    #query_db("UPDATE users SET (NAME, LONGNAME, EMAIL, RFID_ID, ISBLACK, ISBARON, ISSHOWN) VALUES (?, ?, ?, ?, ?, ?, ?) WHERE ID=?", (u.name, u.longname, u.email, u.rfid_id, u.isblack, u.isbaron, u.isshown, u.id))
    query_db("UPDATE users SET NAME=?, LONGNAME=?, EMAIL=?, ISBLACK=?, ISBARON=?, ISSHOWN=?, AUTOBLACK=?, ONLYRFID=? WHERE ID=?", (u.name, u.longname, u.email, u.isblack, u.isbaron, u.isshown, u.autoblack, u.onlyrfid ,u.id))
    set_rfid_to_userid(u.rfid_id, u.id)
    get_db().commit()


def get_products():
    rows = query_db("SELECT * FROM PRODUCTS")
    products = []
    for row in rows:
        p = Product()
        p.id = row[0]
        p.name = row[1]
        p.price = row[2]
        p.isshown = row[3]
        products.append(p)
    return products


def get_product_by_id(id):
    row = query_db("SELECT * FROM PRODUCTS WHERE ID = ?", [str(id)], one=True)
#    print row
    p = Product()
    p.id = row[0]
    p.name = row[1]
    p.price = row[2]
    p.isshown = row[3]
    return p


def get_product_by_name(name):
    row = query_db("SELECT * FROM PRODUCTS WHERE NAME = ?", [str(name)], one=True)
    p = Product()
    p.id = row[0]
    p.name = row[1]
    p.price = row[2]
    p.isshown = row[3]
    return p


def update_product(p):
    query_db("UPDATE products SET NAME=?, PRICE=?, ISSHOWN=? WHERE ID=?", (p.name, p.price, p.isshown, p.id))
    get_db().commit()


def add_product(p):
    query_db("Insert INTO PRODUCTS (NAME, PRICE, ISSHOWN) VALUES (?, ?, ?)", (p.name, p.price, p.isshown))
    get_db().commit()


def get_consumed(user=None, startdate=None, enddate=None):

    if user is None:
        rows = query_db('SELECT * FROM CONSUMED')
    else:
        rows = query_db('SELECT * FROM CONSUMED WHERE CONSUMER=?', [get_user_by_name(user).id])
    consumed = []
    for row in rows:
        #ID|PRODNR|CONSUMER|PRICE|TIME
        c = Consumption()
        c.id = int(row[0])
        c.prodnr = int(row[1])
        c.consumer = int(row[2])
        #2016-01-27 12:59:04
        c.price = float(row[3])
        c.time = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
        if startdate is None or c.time > startdate:
            if enddate is None or c.time < enddate:
                consumed.append(c)
    return consumed


def add_consume(username, productid):

    consumerid = query_db("SELECT ID FROM USERS WHERE NAME = ?", [username], one=True)
    logging.info("consumerid = " + str(consumerid))
    consumerid = int(consumerid[0])
    product = get_product_by_id(productid)
    #INSERT INTO USERS (NAME, PASSWORD, LONGNAME, EMAIL, RFID_ID) VALUES (? ,? ,?, ?, ?)", (u.name, u.password, u.longname, u.email, u.rfid_id))
    query_db("INSERT INTO CONSUMED (PRODNR, CONSUMER, PRICE, TIME) VALUES (?, ?, ?, ?)", (str(product.id), str(consumerid), product.price, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    get_db().commit()

    if settings.autoBlack:
        if get_debt(name=username) > settings.blockLimit:
            u = get_user_by_name(username)
            u.isblack = True
            update_user(u)
    logging.info("consumed")

    return


def get_debt(name=None):
    consumptions = get_consumed(name)
    debt = 0
    for consumption in consumptions:
        debt += consumption.price

    deposits = get_deposits(get_user_by_name(name).id)
    for deposit in deposits:
        debt -= deposit.amount

    debt = round(debt, 2)
    return debt


def get_deposits(userid = None):
    #ID|USERID|AMOUNT|TIME
    if userid == None:
        rows = query_db("SELECT * FROM DEPOSITS")
    else:
        rows = query_db("SELECT * FROM DEPOSITS WHERE USERID = ?", [str(userid)])
    deposits = []
    if rows == None:
        return deposits
    for row in rows:
        d = Deposit()
        d.id = row[0]
        d.userid = row[1]
        d.amount = row[2]
        d.time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
        deposits.append(d)
    return deposits

def add_deposit(username, amount):
    consumerid = query_db("SELECT ID FROM USERS WHERE NAME = ?", [username], one=True)
    consumerid = int(consumerid[0])
    query_db("INSERT INTO DEPOSITS (USERID, AMOUNT, TIME) VALUES (?, ?, ?)", (str(consumerid), amount, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    get_db().commit()
    if settings.autoUnblack:
        if get_debt(name=username) < settings.blockLimit:
            u = get_user_by_name(username)
            u.isblack = False
            update_user(u)
    logging.info("deposit")

    return


##for testing only
def generate_test_users():

    for i in range(1, 30):
        test = User
        test.name = 'test' + str(i)
        test.email = 'test' + str(i) + '@test.at'
        test.password = 'test'
        test.longname = 'Test User' + str(i)
        test.rfid_id = '0x00000000'
        add_user(test)
    return

def generate_test_consumptions():

    #rand.seed(5)
    num_u = len(get_users())
    num_p = len(get_products())
    u = 0
    p = 0
    for i in range(1, 666):
        u = 1 + int(rand.random() * (1.0*num_u))
        p = 1 + int(rand.random() * (1.0*num_p))
        daysa = int(rand.random() * (30.0))
        add_test_consume(u,p,daysa)
    logging.info('trying to add ' +  str(p) + ' to ' + str(u))
    return

def add_test_consume(consumerid, productid, daysago):

    product = get_product_by_id(productid)
    query_db("INSERT INTO CONSUMED (PRODNR, CONSUMER, PRICE, TIME) VALUES (?, ?, ?, ?)", (str(product.id), str(consumerid), product.price, (datetime.datetime.now()-datetime.timedelta(days=daysago)).strftime("%Y-%m-%d %H:%M:%S")))
    get_db().commit()
    return
