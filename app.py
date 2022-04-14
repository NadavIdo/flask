import json
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

# ----Sqlite3 start
con = sqlite3.connect('example.db', check_same_thread=False)
cur = con.cursor()         #החיבור בין התוכנית ל data base מאפשר להריץ משפטי SQL #


def initDB():
    try:# Create table
        cur.execute('''CREATE TABLE Customers (Customerid int,name text, tel text)''')
    except:
        pass
        # print("table already exist")
    
    # cur.execute("INSERT INTO Customers VALUES (3,'itay','456')")# Insert a row of data
 
    # Save (commit) the changes
    con.commit()
initDB()
 # ----Sqlite3 end


api = Flask(__name__)
 

@api.route('/')
def test():
    return 'test - the web site is working'
 

@api.route('/customers')
def displayAllCustomers():
    res = []
    for i in cur.execute("SELECT *  FROM Customers"):
        # print(i)
        res.append({"id": i[0], "name": i[1],"tel": i[2]})
    return (json.dumps(res))
    

@api.route('/dispalynice')
def displaynice():
    res = []
    for i in cur.execute("SELECT rowid, name,tel  FROM Customers"):
        # print(i)
        res.append({"id": i[0], "name": i[1],"tel": i[2]})
    # return (json.dumps(res))
    return render_template('displaycustomers.html', Customers=res)

@api.route('/template')
def displaymain():
    return render_template('main.html')


@api.route('/delcustomer',methods=['POST'])
def delcustomer():
    customerid = request.form.get('customerid')
    cur.execute(f"DELETE FROM Customers where rowid ={customerid}")
    con.commit()
    return render_template('displaycustomers.html')

@api.route('/add',methods=['GET'])
def addform():

    # cur.execute("INSERT INTO Customers VALUES (3,'itay','456')")
    # con.commit()
    return render_template('add.html')

@api.route('/adddata',methods=['POST'])
def addcustomer():
    customerName = request.form.get('name')
    customerTel = request.form.get('tel')
    # print(customerName, customerTel)
    
    if(len(customerName) > 2):
        cur.execute(f"INSERT INTO Customers VALUES (3,'{customerName}','{customerTel}')")
        con.commit()
        msg =f"Success: {customerName} added"
    else: msg ="name should be more then 2 chars..."
    return render_template('add.html',msg=msg)


#@api.route('/details')
#def details():
#    return 'test - the web site is working'


if __name__ == '__main__':
    api.run(debug=True)