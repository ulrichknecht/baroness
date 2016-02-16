import sqlite3
from flask import g
from app import app
from user import User
from product import Product
from consumption import Consumption
import random as rand
import datetime

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
        print "GUI DB acces"
        db = sqlite3.connect(DATABASE)
        closeflag = True

    print query
    print args
    #print "Sqlite: " + query % args
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
    u.rfid_id=row[5]
    u.isblack=row[6]
    u.isbaron=row[7]
    u.isshown=row[8]
    print u
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
    u.rfid_id=row[5]
    u.isblack=row[6]
    u.isbaron=row[7]
    u.isshown=row[8]
    print u
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
        u.rfid_id=row[5]
        u.isblack=row[6]
        u.isbaron=row[7]
        u.isshown=row[8]
        users.append(u)
    return users


def add_user(u):
    query_db("INSERT INTO USERS (NAME, PASSWORD, LONGNAME, EMAIL, RFID_ID) VALUES (? ,? ,?, ?, ?)", (u.name, u.password, u.longname, u.email, u.rfid_id))
    get_db().commit()


def update_user(u):
    #query_db("UPDATE users SET (NAME, LONGNAME, EMAIL, RFID_ID, ISBLACK, ISBARON, ISSHOWN) VALUES (?, ?, ?, ?, ?, ?, ?) WHERE ID=?", (u.name, u.longname, u.email, u.rfid_id, u.isblack, u.isbaron, u.isshown, u.id))
    query_db("UPDATE users SET NAME=?, LONGNAME=?, EMAIL=?, RFID_ID=?, ISBLACK=?, ISBARON=?, ISSHOWN=? WHERE ID=?", (u.name, u.longname, u.email, u.rfid_id, u.isblack, u.isbaron, u.isshown, u.id))
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

    if user is None and startdate is None and enddate is None:
        rows = query_db('SELECT * FROM CONSUMED')

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
        consumed.append(c)

    return consumed

def add_consume(username, productid):

    consumerid = query_db("SELECT ID FROM USERS WHERE NAME = ?", [username], one=True)
    print "consumerid = "
    print consumerid
    consumerid = int(consumerid[0])
    product = get_product_by_id(productid)
    #INSERT INTO USERS (NAME, PASSWORD, LONGNAME, EMAIL, RFID_ID) VALUES (? ,? ,?, ?, ?)", (u.name, u.password, u.longname, u.email, u.rfid_id))
    query_db("INSERT INTO CONSUMED (PRODNR, CONSUMER, PRICE, TIME) VALUES (?, ?, ?, ?)", (str(product.id), str(consumerid), product.price, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    get_db().commit()
    print "consumed"

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
    print 'trying to add ' +  str(p) + ' to ' + str(u)
    return

def add_test_consume(consumerid, productid, daysago):

    product = get_product_by_id(productid)
    query_db("INSERT INTO CONSUMED (PRODNR, CONSUMER, PRICE, TIME) VALUES (?, ?, ?, ?)", (str(product.id), str(consumerid), product.price, (datetime.datetime.now()-datetime.timedelta(days=daysago)).strftime("%Y-%m-%d %H:%M:%S")))
    get_db().commit()
    return