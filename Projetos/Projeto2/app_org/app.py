from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader
from flask_cors import CORS
import hashlib
from forms import *
from datetime import date
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)
CORS(app)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'deti_shop'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

env = Environment(loader=FileSystemLoader('templates'))
env.globals.update(url_for=app.jinja_env.globals['url_for'])


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
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        username = form.username.data
        password_cand = form.password.data

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM UserP WHERE username=%s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['passwd']
            uid = data['usrID']

            if hashlib.sha256(password_cand.encode()).hexdigest() == password:

                session['logged_in'] = True
                session['uid'] = uid
                session['username'] = username

                if data['perms'] == 'A':
                    session['is_admin_logged_in'] = True
                    return redirect(url_for('admin'))
                else:
                    session['is_admin_logged_in'] = False
                    return redirect(url_for('index'))
            
            else:
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
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data

        # Safe
        password = form.password.data
        if len(password) < 8:
            flash('Your password should have at least 8 characters', "danger")
            return render_template("register.html", form=form)
        elif not any(char.isdigit() for char in password) :
            flash('Password should have at least one numeral' , "danger")
            return render_template("register.html", form=form)
        elif not any(char.isupper() for char in password):
            flash('Password should have at least one uppercase letter', "danger")
            return render_template("register.html", form=form)
        elif not any(char.islower() for char in password):
            flash('Password should have at least one lowercase letter', "danger")
            return render_template("register.html", form=form)
        else: 
            password = hashlib.sha256(password.encode()).hexdigest()

        
        description = form.description.data
        mobile = form.mobile.data
        permission = 'U'
        creationDate = date.today()

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO UserP(first_name, last_name, username, email, passwd, descript, phoneNum, perms, createDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, username, email, password, description, mobile, permission, creationDate))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)

@app.route('/search', methods=['GET'])
def search():
    if 'q' in request.args:
        search_name = request.args.get('q')

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM Product WHERE nome LIKE %s ORDER BY nome ASC", ('%' + search_name + '%',))

        products = cur.fetchall()
        cur.close()

        return render_template('search.html', products=products, search_name=search_name)
    return ''

@app.route('/category', methods=['GET', 'POST'])
def category():
    form = AddOrder(request.form)
    CommForm = CommentForm(request.form)

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
            prid = request.args['view']
            rate = CommForm.rating.data
            comm = CommForm.comment.data
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

        return render_template('view_product.html', prods=prods, prod_category=cat, cats=cats, reviews= reviews)
    

    if 'order' in request.args:

        if 'uid' not in session:
            flash('You need to be logged in to order products', 'danger')
            return redirect(url_for('login'))
        
        product_id = request.args['order']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Product WHERE prodID=%s", (product_id,))
        product = cur.fetchall()

        return render_template('order_product.html', prods=product, form=form, prod_category=prod_category, cats=cats)
    
    return render_template('category.html', prods=products, form=form, prod_category=prod_category, cats=cats)


@app.route('/shoppingcart', methods=['POST', 'GET', 'DELETE'])
def shoppingcart():
    form = ShoppingCart(request.form)
    if 'uid' not in session or 'user' not in request.args or session['uid'] != int(request.args['user']):
            flash('Please login to view your shopping cart', 'danger')
            return redirect(url_for('login'))

    usrID = request.args['user']

    print("RECEIVED REQUEST")
    
    c = mysql.connection.cursor()
    c.execute("SELECT Cart.*, Product.* FROM Cart INNER JOIN Product ON Product.prodID = Cart.prodID WHERE Cart.usrID = %s", (usrID,))
    orders = c.fetchall()
    print("GOT THE ORDERS FROM THE USER")

    total = 0
    for order in orders:
        total += order.get("quant") * order.get("price")

    c.execute("SELECT * FROM UserP WHERE usrID = %s", (usrID,))
    user = c.fetchone()

    if request.method == 'POST': # Confirm order containing all shopping items and their respective quantities
        address = form.address.data
        curDate = datetime.datetime.now()
        status = 0
        c.execute("INSERT INTO Request (reqDate, reqUsrID, morada, reqStatus) "
        "VALUES (%s, %s, %s, %s)",(curDate, usrID, address, status))
        
        c.execute("SELECT reqID FROM Request WHERE morada = %s", (address,))
        reqID = c.fetchone()['reqID']
        
        # Move products from Cart to Product_Request
        c.execute("SELECT prodID, quant FROM Cart WHERE usrID = %s", (usrID,))
        cart_items = c.fetchall()

        for cart_item in cart_items:
            prodID = cart_item['prodID']
            quant = cart_item['quant']
            c.execute("INSERT INTO Product_Request (prodID, reqID, quant) VALUES (%s, %s, %s)", (prodID, reqID, quant))

        c.execute("DELETE FROM Cart WHERE usrID = %s", (usrID,))

        mysql.connection.commit()

        # Retrieve updated cart items
        c.execute("SELECT Cart.*, Product.* FROM Cart INNER JOIN Product ON Product.prodID = Cart.prodID WHERE Cart.usrID = %s", (usrID,))
        orders = c.fetchall()

        c.close()

        flash('Order added successfuly', 'success')
        return render_template('shoppingcart.html', orders=orders, form=form, user=user)
    elif request.method == 'DELETE':
        # Expects just a single item to be deleted

        del_form = DeleteCartForm(request.form)

        print(del_form.prodID.data)
        print(del_form.usrID.data)

        c.execute("DELETE FROM Cart WHERE prodID=%s AND usrID=%s", (del_form.prodID.data, del_form.usrID.data))
        
        mysql.connection.commit()

        c.close()
    
    return render_template('shoppingcart.html', form=form, orders=orders, user=user, total=total)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = int(request.args['user'])
        if 'uid' in session and q == session['uid']:
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM UserP WHERE usrID=%s", (q,))
            result = curso.fetchone()
            print(result)
            if result:
                
                if request.method == 'POST':
                    first_name = form.first_name.data
                    last_name = form.last_name.data
                    username = form.username.data
                    email = form.email.data

                    description = form.description.data
                    mobile = form.mobile.data

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
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))
    
@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    form = UpdatePasswordForm(request.form)
    if 'user' in request.args:
        q = int(request.args['user'])
        if q == session['uid']:
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM UserP WHERE usrID=%s", (q,))
            result = curso.fetchone()
            if result:
                if request.method == 'POST':
                    password = hashlib.sha256(form.password.data.encode()).hexdigest()
                    new_password = form.new_password.data
                    confirm_password = form.confirm_password.data

                    if password == result['passwd']:
                        if new_password == confirm_password:
                            if len(new_password) < 8:
                                flash('Your password should have at least 8 characters', "danger")
                                return render_template("update_password.html", form=form)
                            elif not any(char.isdigit() for char in new_password) :
                                flash('Password should have at least one numeral' , "danger")
                                return render_template("update_password.html", form=form)
                            elif not any(char.isupper() for char in new_password):
                                flash('Password should have at least one uppercase letter', "danger")
                                return render_template("update_password.html", form=form)
                            elif not any(char.islower() for char in new_password):
                                flash('Password should have at least one lowercase letter', "danger")
                                return render_template("update_password.html", form=form)
                            else:
                                new_password = hashlib.sha256(new_password.encode()).hexdigest()
                            cur = mysql.connection.cursor()
                            exe = cur.execute("UPDATE UserP SET passwd=%s WHERE usrID=%s", (new_password, q))
                            if exe:
                                mysql.connection.commit()
                                flash('Password updated', 'success')
                                return redirect(url_for('login'))
                            else:
                                flash('Password not updated', 'danger')
                        else:
                            flash('New Password and Confirm password do not match', 'danger')
                    else:
                        flash('Incorrect old password', 'danger')
                return render_template('update_password.html', result=result, form=form)
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')

        curso.close()
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM UserP WHERE usrID=%s", (q,))
        result = curso.fetchone()

        if result:
            if result.get('usrID') == session.get('uid'):
                curso.execute('''
                    SELECT Request.*, Product_Request.*, Product.*
                    FROM Request
                    INNER JOIN Product_Request ON Request.reqID = Product_Request.reqID
                    INNER JOIN Product ON Product_Request.prodID = Product.prodID
                    WHERE Request.reqUsrID = %s
                    ORDER BY Request.reqID ASC
                ''', (session['uid'],))
                res = curso.fetchall()

                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')

        curso.close()
        return redirect(url_for('login'))

@app.route('/404')
def f404():
    return render_template('404.html')

@app.route('/admin')
def admin():
    if "is_admin_logged_in" in session:
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
def orders():
    if "is_admin_logged_in" in session:
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
def admin_add_product():
    if "is_admin_logged_in" in session:
        if session['is_admin_logged_in'] == True:
            if request.method == 'POST':
                prod_name = request.form['prod_name']
                price = request.form['price']
                description = request.form['description']
                category = request.form['category']
                stock = request.form['stock']
                file = request.files['image']

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
    

@app.route('/admin_edit_product', methods=['POST', 'GET', 'DELETE'])
def admin_edit_product():
    if "is_admin_logged_in" in session:
        if session.get('is_admin_logged_in'):
            if 'id' in request.args:
                pid = request.args['id']
                c = mysql.connection.cursor()
                c.execute("SELECT * FROM Product WHERE prodID = %s", (pid,))
                product = c.fetchall()
                c.close()
                if request.method == 'POST':
                    prod_name = request.form['prod_name']
                    price = request.form['price']
                    description = request.form['description']
                    category = request.form['category']
                    stock = request.form['stock']
                    file = request.files['image']

                    # Create Cursor
                    
                    curs = mysql.connection.cursor()
                    curs.execute("SELECT catID FROM Category WHERE nome = %s", (category,))
                    catID = curs.fetchone()['catID']
                    curs.execute("UPDATE Product SET nome = %s, price = %s, catID = %s, stock = %s, descript = %s WHERE prodID = %s", (prod_name, price, catID, stock, description, pid))
                    mysql.connection.commit()

                    fname = file.filename
                    new_filename = f"{pid}.png"

                    file_path = os.path.join('static/products', new_filename)
                    file.save(file_path)
                    # Close Connection
                    curs.close()

                    flash('Product updated with success', 'success')
                    return redirect(url_for('admin'))
                elif request.method == 'DELETE':

                    print("YEAH!!")

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


if (__name__) == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)