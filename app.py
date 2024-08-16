# Create an empty server and run it while debug is on
from flask import *
import pymysql

def db_connection():
    return pymysql.connect(host='localhost',user='root',password='',database='tenders_db')
app = Flask(__name__)
app.secret_key = '6079'

@app.route('/')
def select():
    return render_template('select.html')


@app.route('/login',methods =['POST','GET'])
def login():
    if request.method =='POST':
        email = request.form[('email')]
        password = request.form['password']

        connection =db_connection()
        cursor = connection.cursor()

        sql = "select * from users where user_email = %s and password = %s"
        data = (email,password)

        cursor.execute(sql,data)

        # Check whether the user is available or not
        count = cursor.rowcount
        if count == 0:
            return render_template('Login.html',message1 = 'Invalid Credentials')
        
        else:
            user = cursor.fetchone()
            session['key'] = user[2]
            session['user_type'] = user[0]
            user_type = user[0]
            if user_type == "consumer":
                return redirect ('/home')
            else:
                return redirect ('/supplier')
    else:
        return render_template("Login.html",message2 = 'Login Here')

@app.route('/register',methods =['POST','GET'])
def register():
    # Step 1:Check whether it is POST or GET
    if request.method == 'POST':
        # Step 2:Request data
        user_type = request.form['user_type']
        companyname = request.form['companyName']
        companyemail = request.form['companyEmail']
        phone = request.form['companyPhoneNumber']
        password = request.form['password']
        confirm = request.form['confirm_password']

        

        # Database connection
        connection = db_connection()
        # Cursor():Give connection ability to run sql
        cursor = connection.cursor()
        sql ='insert into users(user_type,company_name,user_email,phone,password) values(%s,%s,%s,%s,%s)'
        data = (user_type,companyname,companyemail,phone,password)


        # Password Checks
        if password != confirm :
            return render_template('registration.html', message = "Your Password doesn't match")
        
        elif len(password) < 8:
            return render_template('registration.html',message ='Password should be more than 8 characters!')
        
        else:
            cursor.execute(sql,data)
            connection.commit()
            return render_template('registration.html',success = 'Registration Complete')
    else:
        return render_template("registration.html", message = 'Register Here')


@app.route('/mpesa', methods = ['POST', 'GET'])
def payment():
    phone = request.form['phone']
    amount = request.form['amount']

    from mpesa import stk_push
    stk_push(phone, amount)

    return "Please Check your phone to complete Payment"

@app.route('/home')
def home():
    return render_template ('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/tenders')
def tenders():
    return render_template('tenders.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/supplier')
def supplier():
    return render_template('supplier.html')

@app.route('/interegration')
def interegration():
    return render_template('interegration.html')

@app.route('/nitif')
def nitif():
    return render_template('nitif.html')

@app.route('/order')
def order():
    return render_template('order.html')

# @app.route('/supplier_dashboard')
# def supplierDash():
#     if session['key'] == 'supplier':
#         return render_template('supplier.html')
#     else:
#         return render_template('403.html')

app.run(debug=True)