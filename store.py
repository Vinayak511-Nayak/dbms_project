from flask import Flask,flash, render_template,redirect,url_for,request
import os

from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'mysecret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vikkinayak'
app.config['MYSQL_DB'] = 'store_database'
mysql = MySQL(app)
db = MySQLdb.connect(host="localhost", user="root", passwd="vikkinayak", db="store_database")
curre=db.cursor()
basedir = os.path.abspath(os.path.dirname(__file__))

login_manager = LoginManager()

login_manager.init_app(app)

from forms import LoginForm, RegisterForm,RiceForm,PaneerForm
current_name=""
@app.route('/',methods =['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data;
        password=form.password.data;
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMER WHERE CNAME = %s AND CPASS = %s', (username, password))
        global current_name
        data = cursor.fetchone()
        if data is not None:
            current_name=username
            return redirect(url_for('store_page'))
            # Redirect to home page

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'



    return render_template('login.html',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form= RegisterForm()

    if form.validate_on_submit():

        username=form.username.data;
        password=form.password.data;
        address=form.address.data;

        curre.execute("""INSERT INTO CUSTOMER(CNAME,CPASS,ADRESS) VALUES(%s,%s,%s)""" ,(username,password,address))
        db.commit()
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

@app.route('/store_page',methods=['GET','POST'])
def store_page():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from item")
    data=cursor.fetchall()
    key_list=[]
    value_list=[]

    for item in data:
        for key,value in item.items():
            key_list.append(key)
            value_list.append(value)

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('INSERT INTO QUANTITY VALUES(%s,%s,%s)',('2','3','60'))

    return render_template('store_page.html',data=data,key_list=key_list,value_list=value_list)


item_price=list()
@app.route('/add_item_cart',methods=['GET','POST'])
def add_item_cart():
    req=request.get_json()
    for item in req.values():
        mycursor = db.cursor()
        sql = "SELECT IT_PRICE FROM ITEM WHERE IT_NAME= %s"
        adr = (item, )
        global item_price
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        for items in myresult:
            item_price.append(items)
            sum_of_items=item_price+0
        curre.execute("""INSERT INTO Cart(Cust_name,ITEM_SELECTED) VALUES(%s,%s)""" ,(current_name,item))
        db.commit()


    return "done"

@app.route('/cart_page',methods=['GET','POST'])
def cart_page():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select ITEM_SELECTED from CART")
    data=cursor.fetchall()
    items_in_cart=[]
    for item in data:
        for key,value in item.items():
            items_in_cart.append(value)
    return render_template('cart_page.html',items_in_cart=items_in_cart)

@app.route('/order',methods=['POST','GET'])
def order():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select ADRESS fROM CUSTOMER")
    data=cursor.fetchall()
    for items in data:
        adress=items
    return render_template('order.html',adress=adress,sum_of_items=sum_of_items)


if __name__ == "__main__":
        app.run(port=9000)
