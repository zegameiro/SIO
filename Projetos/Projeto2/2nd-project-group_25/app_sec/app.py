from flask import Flask, session, redirect, url_for, request, render_template, flash, make_response, jsonify
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from argon2 import PasswordHasher
import secretstorage
from forms import *
from datetime import date
from utils import get_b64encoded_qr_image
from cryptography.fernet import Fernet
from pathlib import Path

import hashlib
import pyotp
import datetime
import os
import requests
import re
import atexit
import getpass
import signal
import sys
import traceback



app = Flask(__name__)
app.secret_key = os.urandom(64)

CORS(app)
csrf = CSRFProtect(app)

# Initialize the Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["250 per day", "50 per hour"]
)

limiter.init_app(app)

@app.after_request
def set_request_header(response):
    csp_policy = (
        "default-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js;" # tive de pôr os liknks que estão no layout.html na pasta dos templates
        "frame-ancestors 'none';"
        "frame-src 'none';"
        "script-src 'self' https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js;"
        "style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css;"
        "img-src 'self' static.products data:;"
        "connect-src 'self' https://127.0.0.1:5000;"
    )
    response.headers['Content-Security-Policy'] = csp_policy
    # response.headers['Content-Type'] = "text/html"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers.pop('Server', None)

    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'

    if 'Pragma' not in response.headers:
        response.headers['Pragma'] = 'no-cache'

    if 'Expires' not in response.headers:
        response.headers['Expires'] = '-1'

    return response

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'deti_shop'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_KEY_PREFIX'] = '__Host-'

mysql.init_app(app)

env = Environment(loader=FileSystemLoader('templates'))
env.globals.update(url_for=app.jinja_env.globals['url_for'])

#
# OTP 2-FA Authentication Constants
#
# sha256 didn't align with the Authenticator app's codes
HMAC_DIGEST = hashlib.sha1
ISSUER_NAME = "DETI Shop"

#
# TOTP Secret Token Encryption and Storage Constants
#

SECRETS_DIR = "secrets"
FERNET_KEY_FNAME = "key.pem"


# 
# E-Mail notification Setup
# 

import smtplib, ssl

SMTP_SSL_PORT = 465  # For SMTP SSL
NOTIF_EMAIL_ADDR = "detishop.notif@gmail.com"
NOTIF_EMAIL_PASS = getpass.getpass(f"[SMTP Setup] Please input password for \"{NOTIF_EMAIL_ADDR}\": ")

# Create a secure SSL context
SMTP_CONTEXT = ssl.create_default_context()

smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", SMTP_SSL_PORT, context=SMTP_CONTEXT)
smtp_server.login(NOTIF_EMAIL_ADDR, NOTIF_EMAIL_PASS)

#
# Secret Storage Setup
#

ss_conn = secretstorage.dbus_init()
key_collection = secretstorage.get_default_collection(ss_conn)

if key_collection.is_locked():
    while not key_collection.unlock():
        print("[WARNING] Please insert OS user login password")

def exit_cleanup():
    smtp_server.close()
    ss_conn.close()

def sig_cleanup(arg1, arg2):
    smtp_server.close()
    ss_conn.close()
    sys.exit(0)

atexit.register(exit_cleanup)
signal.signal(signal.SIGTERM, sig_cleanup)
signal.signal(signal.SIGINT, sig_cleanup)


ph = PasswordHasher() # iniciar a instância do argon2

def sanitize_string(input_string):
    return re.sub(r'[^\w\s]', '', input_string)

DEBUG_LOGIN = False
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Redirect any page that doesn't exist to the 404 page
@app.errorhandler(404)
def page_not_found(e):
    response = redirect(url_for('f404'), code=302)
    return response

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(error="rate limit exceeded"), 429
    )


@app.route('/')
def index():
    form = ShoppingCart(request.form)
    
    # Create a cursor
    cur = mysql.connection.cursor()

    values = '1'
    cur.execute('SELECT * FROM Product WHERE catID= %s ORDER BY RAND() LIMIT 4', (values,))
    Clothing = cur.fetchall()
    
    values = '2'
    cur.execute('SELECT * FROM Product WHERE catID = %s ORDER BY RAND() LIMIT 4', (values,))
    FootWear = cur.fetchall()

    values = '3'
    cur.execute('SELECT * FROM Product WHERE catID = %s ORDER BY RAND() LIMIT 4', (values,))
    Eletronics = cur.fetchall()

    values = '4'
    cur.execute('SELECT * FROM Product WHERE catID = %s ORDER BY RAND() LIMIT 4', (values,))
    Utilities = cur.fetchall()

    values = '5'
    cur.execute('SELECT * FROM Product WHERE catID = %s ORDER BY RAND() LIMIT 4', (values,))
    Furniture = cur.fetchall()

    cur.close()    

    return render_template('home.html', Clothing=Clothing, FootWear=FootWear, Eletronics=Eletronics, Utilities=Utilities, Furniture=Furniture)
    
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm(request.form)
    session['setup_2fa'] = False

    if request.method == 'POST':
        username = form.username.data
        password_cand = form.password.data

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM UserP WHERE username=%s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['passwd']
            uid = data['usrID']
            secret_token = data['secretToken'] # TOTP Secret key associated with user
            try:
                ph.verify(password, password_cand)
                if ph.check_needs_rehash(password):
                    new_hash = ph.hash(password_cand)
                    # update the stored hash with new_hash in your database
                    cur.execute("UPDATE UserP SET passwd = %s WHERE usrID = %s", (new_hash,uid))

                res = cur.execute("SELECT * FROM Cart WHERE usrID = %s and waiting_confirm = 1", (uid,))

                if res > 0:
                    shopcart_items = cur.fetchone()
                    address = shopcart_items['morada']
                    curDate = datetime.datetime.now()
                    status = 0
                    cur.execute("INSERT INTO Request (reqDate, reqUsrID, morada, reqStatus) VALUES (%s, %s, %s, %s)",(curDate, uid, address, status))
                
                    reqID = cur.lastrowid
                
                    # Move products from Cart to Product_Request
                    cur.execute("SELECT prodID, quant FROM Cart WHERE usrID = %s", (uid,))
                    cart_items = cur.fetchall()

                    for cart_item in cart_items:
                        prodID = cart_item['prodID']
                        quant = cart_item['quant']
                        cur.execute("INSERT INTO Product_Request (prodID, reqID, quant) VALUES (%s, %s, %s)", (prodID, reqID, quant))

                    cur.execute("DELETE FROM Cart WHERE usrID = %s", (uid,))

                    mysql.connection.commit()

                    cur.close()

                    flash('Your order has been confirmed with success', 'success')
                    return redirect(url_for('profile'))

                if DEBUG_LOGIN:
                    session['uid'] = uid
                    session['username'] = username
                    perms = data['perms']
                    session['logged_in'] = True

                    if perms == 'A':
                        session['is_admin_logged_in'] = True
                        return redirect(url_for('admin'))

                    session['is_admin_logged_in'] = False
                    flash('Login successful! Welcome to DETI Shop!', 'success')
                    return redirect(url_for('index'))

                session['aux_uid'] = uid
                session['aux_username'] = username
                session['aux_perms'] = data['perms']

                if not secret_token:
                    flash("You haven't enabled two-factor authentication, please enable it here.", 'info')
                    session['setup_2fa'] = True
                    return redirect(url_for('setup_2fa'))
                
                return redirect(url_for('login_2fa'))
            
            except argon2.exceptions.VerifyMismatchError:
            # Invalid password
                flash('Incorrect username or password', 'danger')
                return render_template('login.html', form=form)
        else:
            flash('Incorrect username or password', 'danger')
            cur.close()
            return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)

@app.route('/out')
def logout():
    if 'uid' in session:
        session.clear()

        response = make_response(redirect(url_for('index')))

        # Set headers to instruct browser to not cache the content
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'

        flash('You are logged out', 'success')
        return response
    
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def register():
    user_agent = sanitize_string(request.headers.get('User-Agent'))
    form = RegisterForm(request.form)
    
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        description = form.description.data
        if form.mobile.data is None or form.mobile.data == "":
            mobile = "123456789"  # fixed number to be stored in the database when no value is given. This value cannot be a real phone number
        else:
            mobile = str(form.mobile.data)  # Convert to string only if it's not None or empty
        
        # Check if username already exists in the database
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM UserP WHERE username = %s", [username])

        if result > 0:
            # Username already exists
            flash('This username is already taken. Please choose another one.', 'danger')
            return render_template('register.html', form=form)
        else:
            # Username is unique, proceed with registration
            
            # Safe
            password = form.password.data
            password = ' '.join(password.split()) # damos trim dos espaços seguidos
            if len(password) < 12:
                flash('Your password should have at least 12 characters. Are you using multiple spaces combined?', "danger")
                return render_template("register.html", form=form)
            elif first_name in password or last_name in password or username in password or email in password or mobile in password:
                flash('Your password should not contain any of the informations provided.', "danger")
                return render_template("register.html", form=form)
            elif len(password) > 128:
                flash('Your password should not have more than 128 characters.', "danger")
                return render_template("register.html", form=form)
            else: 
                sha1pass = hashlib.sha1(password.encode()).hexdigest().upper()
                head, tail = sha1pass[:5], sha1pass[5:]
                response = requests.get('https://api.pwnedpasswords.com/range/' + head)

                if tail in response.text:
                    flash('This password has been compromised before, please choose another one', "danger")
                    return render_template("register.html", form=form)
                store_password = ph.hash(password)

            permission = 'U'    
            creationDate = date.today()
    
            cur = mysql.connection.cursor()
    
            print("VALUE TO BE INSERTED", mobile)
            cur.execute("INSERT INTO UserP(first_name, last_name, username, email, passwd, descript, phoneNum, perms, createDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (first_name, last_name, username, email, store_password, description, mobile, permission, creationDate))
    
            mysql.connection.commit()

            if DEBUG_LOGIN:
                session['uid'] = cur.lastrowid
                session['username'] = username
                session['logged_in'] = True

                session['is_admin_logged_in'] = False
                
                flash('Register successful! Welcome to DETI Shop!', 'success')
                return redirect(url_for('index'))

            session['aux_uid'] = cur.lastrowid
            session['aux_username'] = username
            session['aux_perms'] = permission
    
            cur.close()
            session['setup_2fa'] = True
            return redirect(url_for('setup_2fa'))
        
    return render_template("register.html", form=form)

@app.route('/setup-2fa', methods=['GET', 'POST'])
def setup_2fa():
    form = Setup2FAForm(request.form)

    if not session.get('aux_uid') or not session.get('aux_username') or not session.get('setup_2fa'):
        flash('Invalid action.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Assumes user was already registered

        secret_token = pyotp.random_base32()

        # Encrypt secret token and store Fernet key
        
        key = Fernet.generate_key()

        # Secret Service storage, assumes collection is unlocked

        key_collection.create_item(f"DETI_SHOP_UID_{session['aux_uid']}", { 'app':'DETI_SHOP', 'uid':str(session['aux_uid']) }, key)

        f = Fernet(key)
        encrypt_token = f.encrypt(secret_token.encode("utf-8"))

        totp = pyotp.TOTP(secret_token, name = session['aux_username'], digest = HMAC_DIGEST, issuer = ISSUER_NAME)
        
        qr_code = get_b64encoded_qr_image(totp.provisioning_uri())

        cur = mysql.connection.cursor()

        cur.execute("UPDATE UserP SET secretToken = %s WHERE usrID = %s", (encrypt_token, session['aux_uid'],))

        mysql.connection.commit()

        cur.close()

        return render_template("setup_2fa.html", secret=secret_token, form=form, qr_code=qr_code)
    elif request.method == 'POST':
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT secretToken, lastOTP, email FROM UserP WHERE usrID = %s", (session['aux_uid'],))
        data = cur.fetchone()

        encrypt_token = data['secretToken'] 
        last_code = data['lastOTP'] # For TOTP validation
        email = data['email']

        # Read key from Secret Service key storage
        # Assumes collection is unlocked

        try:
            items = key_collection.search_items({'app':'DETI_SHOP', 'uid':str(session['aux_uid'])})
            item : secretstorage.Item = next(items)
            key = item.get_secret()
        except secretstorage.ItemNotFoundException:
            flash('An error occurred while processing your code. Please contact site support.', 'danger')
            return redirect(url_for('login'))

        f = Fernet(key)
        secret_token = f.decrypt(encrypt_token).decode("utf-8")
    
        totp_code = int(form.totp.data)

        totp = pyotp.TOTP(secret_token, name = session['aux_username'], digest = HMAC_DIGEST, issuer = ISSUER_NAME)

        if not totp.verify(totp_code):
            qr_code = get_b64encoded_qr_image(totp.provisioning_uri())
            flash("Wrong code given! Insert your code in time and check for typos.", "danger")
            return render_template('setup_2fa.html', secret=secret_token, form=form, qr_code=qr_code)
        
        # TOTP code can't be used more than once
        if totp_code == last_code:
            cur.close()

            # Inform user of TOTP reuse attempt via e-mail

            email_message = \
            """
            Subject: [DETI-SHOP] Attempted reuse of 2FA code

            This is a warning from DETI Shop to notify you about the reuse of one your two-factor authentication code
            within its expiration period.

            If you used this code more than once, please ignore this message. 
            Otherwise, consider contacting support and changing your 2FA configuration by renewing your secret token.
            """
            try:
                smtp_server.sendmail(NOTIF_EMAIL_ADDR, email, email_message)
            except Exception: # Something failed when sending mail, should opt for a persistent log
                print(traceback.format_exc())

            flash('Invalid action, code was already used before.', 'danger')
            return redirect(url_for('login'))
        
        # Success :)

        session['uid'] = session['aux_uid']
        session['username'] = session['aux_username']
        perms = session['aux_perms']

        # Register last used OTP code
        cur.execute("UPDATE UserP SET lastOTP = %s WHERE usrID = %s", (totp_code, session['aux_uid'],))

        mysql.connection.commit()

        session['aux_uid'] = None
        session['aux_username'] = None
        session['aux_perms'] = None
        session['setup_2fa'] = False

        cur.close()

        if perms == 'A':
            session['is_admin_logged_in'] = True
            return redirect(url_for('admin'))

        session['is_admin_logged_in'] = False
        session['logged_in'] = True
        flash('Login successful! Welcome to DETI Shop!', 'success')
        return redirect(url_for('index'))

    return render_template("404.html")

@app.route('/login-2fa', methods=['GET', 'POST'])
def login_2fa():
    form = Setup2FAForm(request.form)

    if not session.get('aux_uid') or not session.get('aux_username'):
        flash('Invalid action.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template("login_2fa.html", form=form)
    elif request.method == 'POST':
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT secretToken, lastOTP, email FROM UserP WHERE usrID = %s", (session['aux_uid'],))

        data = cur.fetchone()

        encrypt_token = data['secretToken'] 
        last_code = data['lastOTP'] # For TOTP validation
        email = data['email']

        # Read key from Secret Service key storage
        # Assumes collection is unlocked

        try:
            items = key_collection.search_items({'app':'DETI_SHOP', 'uid':str(session['aux_uid'])})
            item : secretstorage.Item = next(items)
            key = item.get_secret()
        except secretstorage.ItemNotFoundException:
            flash('An error occurred while processing your code. Please contact site support.', 'danger')
            return redirect(url_for('login'))

        f = Fernet(key)
        secret_token = f.decrypt(encrypt_token).decode("utf-8")
    
        totp_code = int(form.totp.data)
        totp = pyotp.TOTP(secret_token, name = session['aux_username'], digest = HMAC_DIGEST, issuer = ISSUER_NAME)
        
        if not totp.verify(totp_code):
            flash("Wrong code given! Insert your code in time and check for typos.", "danger")
            return render_template('login_2fa.html', form=form)
        
        # TOTP code can't be used more than once
        if totp_code == last_code:
            cur.close()

            # Inform user of TOTP reuse attempt via e-mail

            email_message = \
            """
            Subject: [DETI-SHOP] Attempted reuse of 2FA code

            This is a warning from DETI Shop to notify you about the reuse of one of your two-factor authentication code
            within its expiration period.

            If you used this code more than once, please ignore this message. 
            Otherwise, consider contacting support and changing your 2FA configuration by renewing your secret token.
            """
            try:
                smtp_server.sendmail(NOTIF_EMAIL_ADDR, email, email_message)
            except Exception: # Something failed when sending mail, should opt for a persistent log
                print(traceback.format_exc())

            flash('Invalid action, code was already used before.', 'danger')
            return redirect(url_for('login'))
        
        # Success :)

        session['uid'] = session['aux_uid']
        session['username'] = session['aux_username']
        perms = session['aux_perms']

        # Register last used OTP code
        cur.execute("UPDATE UserP SET lastOTP = %s WHERE usrID = %s", (totp_code, session['aux_uid'],))

        mysql.connection.commit()

        session['aux_uid'] = None
        session['aux_username'] = None
        session['aux_perms'] = None

        cur.close()

        if perms == 'A':
            session['is_admin_logged_in'] = True
            return redirect(url_for('admin'))
        
        session['logged_in'] = True
        session['is_admin_logged_in'] = False
        
        flash('Login successful! Welcome to DETI Shop!', 'success')
        return redirect(url_for('index'))

    return render_template("404.html")

@app.route('/search', methods=['GET'])
@limiter.limit("30 per minute")
def search():
    if 'q' in request.args:
        search_name = request.args.get('q')

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM Product WHERE nome LIKE %s ORDER BY nome ASC", ('%' + search_name + '%',))

        products = cur.fetchall()
        cur.close()

        return render_template('search.html', products=products, search_name=search_name)
    return render_template('404.html')

@app.route('/category', methods=['GET', 'POST'])
def category():
    form = AddOrder(request.form)
    commForm = CommentForm(request.form)

    cur = mysql.connection.cursor()

    values = request.args.get('catID')

    cur.execute("SELECT * FROM Product WHERE catID = %s ORDER BY prodID ASC", (values,))
    products = cur.fetchall()

    cur.execute("SELECT * FROM Category WHERE catID = %s", (values,))
    prod_category = cur.fetchall()

    cur.execute("SELECT * FROM Category")
    cats = cur.fetchall()

    if request.method == 'POST':
        if 'order' in request.args and 'uid' in session:

            quantity = int(form.quantity.data)
            pid = request.args['order']

            uid = session.get('uid')

            cur.execute("SELECT * FROM Cart WHERE usrID=%s AND prodID=%s", (uid, pid))
            
            cart_prod = cur.fetchone()

            cur.execute("SELECT stock FROM Product WHERE prodID=%s", (pid,))

            prod_stock = cur.fetchone().get("stock")

            if cart_prod is not None: # We don't want any duplicate entries 
                cart_quant = int(cart_prod.get("quant"))
                if cart_quant + quantity <= prod_stock:
                    cur.execute("UPDATE Cart SET quant = %s WHERE usrID = %s AND prodID = %s", (cart_quant + quantity, uid, pid))
                    flash('Added to cart with success', 'success')
                else: 
                    flash("Total requested quantity ("+ cart_quant + quantity +") exceeds stock of " + prod_stock, "danger")
            elif quantity <= prod_stock:
                cur.execute("INSERT INTO Cart(prodID, usrID, quant) VALUES (%s, %s, %s)", (pid, uid, quantity))
                flash('Added to cart with success', 'success')
            else:
                flash("Total requested quantity ("+ quantity +") exceeds stock of " + prod_stock, "danger")
            
            mysql.connection.commit()
            return redirect("/category?catID=%s&view=%s" % (values, pid))

        elif 'view' in request.args:
            print("ENTERED IN POST FROM COMMENT")
            view = request.args.get('view') 
    
            # Validate 'view' parameter
            if view and view.isdigit():
                view = int(view)
                # Further check if 'view' is within the expected range
                if view < 1 or view > 100: # MAX_ID_VALUE (100) should be the length of products
                    return "Invalid 'view' parameter", 400
            else:
                return "Invalid 'view' parameter", 400
    
            prid = request.args['view']
            rate = commForm.rating.data
            comm = commForm.comment.data
            curDate = datetime.datetime.now()
            usrid = session['uid']

            cur.execute("INSERT INTO Review(rating, critique, revDate, usrID, prodID) VALUES (%s, %s, %s, %s,%s)", (rate, comm, curDate, usrid, prid))

            mysql.connection.commit()
            flash('Comment added with success', 'success')
            return redirect("/category?catID=%s&view=%s" % (values, prid))
    
    # GET method cases
    if 'view' in request.args:
        product_id = request.args['view'] 
        cur.execute("SELECT * FROM Product WHERE prodID=%s", (product_id,))
        prods = cur.fetchall()

        catID = prods[0]['catID']
        cur.execute("SELECT * FROM Category WHERE catID=%s", (catID,))
        cat = cur.fetchall()

        cur.execute('''
                    SELECT Review.*, UserP.*
                    FROM Review
                    INNER JOIN UserP ON Review.usrID = UserP.usrID
                    WHERE Review.prodID = %s
                    ''', (product_id,))
        reviews = cur.fetchall()

        return render_template('view_product.html', prods=prods, commForm=commForm, prod_category=cat, cats=cats, reviews= reviews)
    

    if 'order' in request.args:

        if 'uid' not in session:
            flash('You need to be logged in to order products', 'danger')
            return redirect(url_for('login'))
        
        product_id = request.args['order']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Product WHERE prodID=%s", (product_id,))
        product = cur.fetchall()

        return render_template('order_product.html', prods=product, form=form, prod_category=prod_category, cats=cats)
    
    return render_template('category.html', prods=products, commForm=commForm, form=form, prod_category=prod_category, cats=cats)


@app.route('/shoppingcart', methods=['POST', 'GET'])
def shoppingcart():
    form = ShoppingCart(request.form)
    delForm = DeleteProdForm(request.form)

    sess_id = session.get('uid')
    if sess_id:
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM UserP WHERE usrID=%s", (sess_id,))
        result = curso.fetchone()

        if result:
            curso.execute("SELECT Cart.*, Product.* FROM Cart INNER JOIN Product ON Product.prodID = Cart.prodID WHERE Cart.usrID = %s", (sess_id,))
            orders = curso.fetchall()

            total = 0
            for order in orders:
                total += order.get("quant") * order.get("price")

            curso.execute("SELECT * FROM UserP WHERE usrID = %s", (sess_id,))
            user = curso.fetchone()

            if request.method == 'POST': # Update the state of the shopping cart to waiting for confirm where the user needs to log in again
                if 'delete_product' in request.form:
                    prod_id = delForm.prodID.data
                    curso.execute("DELETE FROM Cart WHERE prodID=%s AND usrID=%s", (prod_id, sess_id))
                    mysql.connection.commit()

                    # Update the orders list
                    curso.execute("SELECT Cart.*, Product.* FROM Cart INNER JOIN Product ON Product.prodID = Cart.prodID WHERE Cart.usrID = %s", (sess_id,))
                    orders = curso.fetchall()

                    curso.close()
                    flash('Product removed from shopping cart with success', 'success')
                    return render_template('shoppingcart.html', form=form, delForm=delForm, orders=orders, total=total, user=user)
                
                elif 'order_form' in request.form:
                    address = form.address.data
                    waiting_conf = 1
                    curso.execute("UPDATE Cart SET waiting_confirm = %s, morada = %s WHERE usrID = %s ", (waiting_conf, address, sess_id))
                    mysql.connection.commit()

                    flash('You must log in again to confirm order', 'success')
                    return redirect(url_for('login'))

            return render_template('shoppingcart.html', form=form, delForm=delForm, orders=orders, total=total, user=user)
        else:
            flash('Not logged in', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Not logged in', 'danger')
        return redirect(url_for('login'))

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    form = UpdateRegisterForm(request.form)

    sess_id = session.get('uid')
    if sess_id:
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM UserP WHERE usrID=%s", (sess_id,))
        result = curso.fetchone()

        if result:
            
            if request.method == 'POST':
                first_name = form.first_name.data
                last_name = form.last_name.data
                username = form.username.data
                email = form.email.data

                description = form.description.data
                mobile = form.mobile.data

                if form.mobile.data is None or form.mobile.data == "":
                    mobile = "123456789"  # fixed number to be stored in the database when no value is given. This value cannot be a real phone number
                else:
                    mobile = str(form.mobile.data)  # Convert to string only if it's not None or empty

                # Create Cursor
                cur = mysql.connection.cursor()
                exe = cur.execute("UPDATE UserP SET first_name=%s, last_name=%s, username=%s, email=%s, descript=%s, phoneNum=%s WHERE usrID=%s",
                                    (first_name, last_name, username, email, description, mobile, result['usrID']))
                if exe:
                    mysql.connection.commit()
                    flash('Profile updated', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Profile not updated', 'danger')
            return render_template('user_settings.html', result=result, form=form)

        else:
            # Same message as 'no session', in order not to give away information (if the user exists or not)
            flash('Not logged in', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Not logged in', 'danger')
        return redirect(url_for('login'))
    
@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    form = UpdatePasswordForm(request.form)

    sess_id = session.get('uid')
    if sess_id:
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM UserP WHERE usrID=%s", (sess_id,))
        result = curso.fetchone()

        if result:
            if request.method == 'POST':
                password = form.password.data
                new_password = form.new_password.data
                confirm_password = form.confirm_password.data

                try:
                    if ph.verify(result['passwd'], password):
                        if new_password == confirm_password:
                            new_password = ' '.join(new_password.split()) # damos trim dos espaços seguidos
                            if len(new_password) < 12:
                                flash('Your password should have at least 12 characters. Are you using multiple spaces combined?', "danger")
                                return render_template("update_password.html", result=result, form=form)
                            elif result['first_name'] in new_password or result['last_name'] in new_password or result['username'] in new_password or result['email'] in new_password or str(result['phoneNum']) in new_password:
                                    flash('Your password should not contain any of the informations provided.', "danger")
                                    return render_template("update_password.html", result=result, form=form)
                            elif len(password) > 128:
                                flash('Your password should not have more than 128 characters.', "danger")
                                return render_template("update_password.html", result=result, form=form)
                            else:
                                sha1pass = hashlib.sha1(new_password.encode()).hexdigest().upper()
                                head, tail = sha1pass[:5], sha1pass[5:]
                                response = requests.get('https://api.pwnedpasswords.com/range/' + head)

                                if tail in response.text:
                                    flash('This password has been compromised before, please choose another one', "danger")
                                    return render_template("update_password.html", result=result, form=form)
                                store_password = ph.hash(new_password)


                            exe = curso.execute("UPDATE UserP SET passwd=%s WHERE usrID=%s", (store_password, sess_id))
                            if exe:
                                mysql.connection.commit()
                                flash('Password updated', 'success')
                                return redirect(url_for('login'))
                            else:
                                flash('Password not updated', 'danger')
                        else:
                            flash('New Password and Confirm password do not match', 'danger')
                except argon2.exceptions.VerifyMismatchError:
                    flash('Incorrect old password', 'danger')
            curso.close()
            return render_template('update_password.html', result=result, form=form)
        else:
            # Same message as 'no session', in order not to give away information (if the user exists or not)
            flash('Not logged in', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Not logged in', 'danger')
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    sess_id = session.get('uid')
    if sess_id:
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM UserP WHERE usrID=%s", (sess_id,))
        result = curso.fetchone()

        if result:
            curso.execute('''
                    SELECT Request.*, Product_Request.*, Product.*
                    FROM Request
                    INNER JOIN Product_Request ON Request.reqID = Product_Request.reqID
                    INNER JOIN Product ON Product_Request.prodID = Product.prodID
                    WHERE Request.reqUsrID = %s
                    ORDER BY Request.reqID ASC
                ''', (sess_id,))
            res = curso.fetchall()

            return render_template('profile.html', result=res)
        else:
            # Same message as 'no session', in order not to give away information (if the user exists or not)
            flash('Not logged in', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Not logged in', 'danger')
        return redirect(url_for('login'))

@app.route('/404')
def f404():
    return render_template('404.html')

@app.route('/admin')
def admin():
    if "is_admin_logged_in" in session and "uid" in session:
        if session['is_admin_logged_in']:
            cur = mysql.connection.cursor()

            num_rows = cur.execute("SELECT * FROM Product")
            result = cur.fetchall()

            order_rows = cur.execute('SELECT * FROM Request')
            user_rows = cur.execute('SELECT * FROM UserP')

            return render_template('admin_index.html', result=result, row=num_rows, order_rows=order_rows, user_rows=user_rows)
        
        else:
            flash("You don't have permissions for this page!", "danger")
            return redirect(url_for('index'))
    else:
        flash("You need to log in to access this page!", "danger")
        return redirect(url_for('login'))

@app.route('/users')
def users():
    if "is_admin_logged_in" in session:
        if session['is_admin_logged_in'] == True:
            c = mysql.connection.cursor()
            num_rows = c.execute('SELECT * FROM Product')
            order_rows = c.execute('SELECT * FROM Request')
            users_rows = c.execute('SELECT * FROM UserP')
            result = c.fetchall()

            return render_template('all_users.html', result=result, row=num_rows, order_rows=order_rows, users_rows=users_rows)
        
        else:
            flash("You don't have permissions for this page!", "danger")
            return redirect(url_for('index'))
    else:
        flash("You need to log in to access this page!", "danger")
        return redirect(url_for('login'))

@app.route('/orders')
@limiter.limit("5 per minute")
def orders():
    if "is_admin_logged_in" in session and "uid" in session:
        if session['is_admin_logged_in'] == True:
            cur = mysql.connection.cursor()
            num_rows = cur.execute("SELECT * FROM Product")
            users_rows = cur.execute("SELECT * FROM UserP")
            order_rows = cur.execute("SELECT Request.*, Product_Request.*, Product.*, UserP.* FROM Request INNER JOIN Product_Request ON Request.reqID = Product_Request.reqID INNER JOIN Product ON Product_Request.prodID = Product.prodID INNER JOIN UserP ON UserP.usrID = Request.reqUsrID")
            result = cur.fetchall()

            return render_template("all_orders.html", result=result, row=num_rows, order_rows=order_rows, users_rows=users_rows)
        
        else:
            flash("You don't have permissions for this page!", "danger")
            return redirect(url_for('index'))
    else:
        flash("You need to log in to access this page!", "danger")
        return redirect(url_for('login'))
    
@app.route('/admin_add_product', methods=['POST', 'GET'])
@limiter.limit("3 per minute")
def admin_add_product():
    if "is_admin_logged_in" in session and "uid" in session:
        if session['is_admin_logged_in'] == True:
            if request.method == 'POST':
                prod_name = request.form['prod_name']
                price = request.form['price']
                description = request.form['description']
                category = request.form['category']
                stock = request.form['stock']
                file = request.files['image']

                # Verificação do tamanho do arquivo
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                if file_length > MAX_FILE_SIZE:
                    flash('File size exceeds the maximum limit of 5 MB.', 'danger')
                    return render_template('add_product.html')
                # Reset file pointer
                file.seek(0)

                # Create Cursor
                curs = mysql.connection.cursor()
                curs.execute("SELECT catID FROM Category WHERE nome = %s", (category,))
                catID = curs.fetchone()['catID']
                curs.execute("INSERT INTO Product(nome, price, catID, stock, descript) VALUES( %s, %s, %s, %s, %s)", (prod_name, price, catID, stock, description))
                mysql.connection.commit()
                product_id = curs.lastrowid

                # Safe
                if not file.filename.endswith('.png') and not file.filename.endswith('.jpg'):
                    flash('Invalid file type, please upload a png or jpg image', 'danger')
                    return render_template('add_product.html')
                else:
                    if file.filename.endswith('.png'):
                        new_filename = f"{product_id}.png"
                    elif file.filename.endswith('.jpg'):
                        new_filename = f"{product_id}.jpg"

                    file_path = os.path.join('static/products', new_filename)
                    file.save(file_path) 

                # Close Connection
                curs.close()

                flash('Product added successful', 'success')
                return redirect(url_for('admin'))
            else:
                return render_template('add_product.html')
        else:
            flash("You don't have permissions for this page!", "danger")
            return redirect(url_for('index'))
    else:
        flash("You need to log in to access this page!", "danger")
        return redirect(url_for('login'))
    

@app.route('/admin_edit_product', methods=['POST', 'GET'])
@limiter.limit("5 per minute")
def admin_edit_product():
    if "is_admin_logged_in" in session and "uid" in session:
        if session.get('is_admin_logged_in'):
            if 'id' in request.args:
                pid = request.args['id']
                c = mysql.connection.cursor()
                c.execute("SELECT * FROM Product WHERE prodID = %s", (pid,))
                product = c.fetchall()
                c.close()
                if request.method == 'POST':
                    if 'edit_product' in request.form:
                        prod_name = request.form['prod_name']
                        price = request.form['price']
                        description = request.form['description']
                        category = request.form['category']
                        stock = request.form['stock']
                        file = request.files['image']

                        # Verificação do tamanho do arquivo
                        file.seek(0, os.SEEK_END)
                        file_length = file.tell()
                        if file_length > MAX_FILE_SIZE:
                            flash('File size exceeds the maximum limit of 5 MB.', 'danger')
                            return render_template('edit_product.html')
                        # Reset file pointer
                        file.seek(0)
                        
                        # Create Cursor
                        curs = mysql.connection.cursor()
                        curs.execute("SELECT catID FROM Category WHERE nome = %s", (category,))
                        catID = curs.fetchone()['catID']
                        curs.execute("UPDATE Product SET nome = %s, price = %s, catID = %s, stock = %s, descript = %s WHERE prodID = %s", (prod_name, price, catID, stock, description, pid))
                        mysql.connection.commit()

                        # Safe
                        if not file.filename.endswith('.png') and not file.filename.endswith('.jpg'):
                            flash('Invalid file type, please upload a png or jpg image', 'danger')
                            return render_template('edit_product.html')
                        else:
                            if file.filename.endswith('.png'):
                                new_filename = f"{pid}.png"
                            elif file.filename.endswith('.jpg'):
                                new_filename = f"{pid}.jpg"

                        file_path = os.path.join('static/products', new_filename)
                        file.save(file_path)
                        
                        # Close Connection
                        curs.close()

                        flash('Product updated with success', 'success')
                        return redirect(url_for('admin'))
                    
                    elif 'delete_product' in request.form:
                        curs = mysql.connection.cursor()
                        
                        curs.execute("DELETE FROM Product WHERE prodID = %s", (pid,))

                        mysql.connection.commit()

                        curs.close()
                        flash("Sucessfully removed product!", "success")
                        return redirect(url_for('admin'))
                else:
                    return render_template('edit_product.html', product=product)
            else:
                return redirect(url_for('login'))
        else:
            flash("You don't have permissions for this page!", "danger")
            return redirect(url_for('index'))
    else:
        flash("You need to log in to access this page!", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    context = ("./tls_cert/server.crt", "./tls_cert/server.key")
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=context)