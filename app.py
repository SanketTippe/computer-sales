import os
import random
import string
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'bwoc0wbiohcd7lulo3iv-mysql.services.clever-cloud.com')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'urkj6e4vd5nlvhpp')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'YOUR_PASSWORD_HERE')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'bwoc0wbiohcd7lulo3iv')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'sanket-computers-secret-key-2024'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql = MySQL(app)

# ============================================
# HELPER FUNCTIONS
# ============================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def generate_invoice_number():
    return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

def generate_order_number():
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'noreply@sanketscomputers.com'
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Configure with your SMTP settings
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login('your-email@gmail.com', 'your-password')
        # server.send_message(msg)
        # server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_sms(phone_number, message):
    try:
        # Configure with your SMS API
        # Use Fast2SMS, Msg91, etc.
        return True
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uid' not in session and 'admin_id' not in session and 'delivery_id' not in session:
            return redirect(url_for('userlog'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('adminlog'))
        return f(*args, **kwargs)
    return decorated_function

def delivery_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'delivery_id' not in session:
            return redirect(url_for('delivery_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_settings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT setting_key, setting_value FROM tbl_settings")
    settings = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    return settings

def get_cart_count():
    count = 0
    if 'uid' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(quantity) FROM tbl_cart WHERE user_id=%s", ([session['uid']]))
        result = cur.fetchone()[0]
        count = result if result else 0
        cur.close()
    elif 'cart_session' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(quantity) FROM tbl_cart WHERE session_id=%s", ([session['cart_session']]))
        result = cur.fetchone()[0]
        count = result if result else 0
        cur.close()
    return count

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_database():
    cur = mysql.connection.cursor()

    # Create tables if not exist (already in SQL file, but adding columns for existing DB)
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN payment_method VARCHAR(50) DEFAULT NULL")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN payment_date DATETIME DEFAULT NULL")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN invoice_number VARCHAR(50) DEFAULT NULL")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN booking_date DATETIME DEFAULT CURRENT_TIMESTAMP")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN is_canceled TINYINT(1) DEFAULT 0")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN cancellation_date DATETIME DEFAULT NULL")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN booking_status VARCHAR(50) DEFAULT 'Pending'")
    except:
        pass
    try:
        cur.execute("ALTER TABLE tbl_booking ADD COLUMN order_number VARCHAR(50) DEFAULT NULL")
    except:
        pass

    # Create wishlist table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_wishlist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except:
        pass

    # Create cart table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(100),
                user_id INT DEFAULT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
    except:
        pass

    # Create product reviews table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_product_reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                user_id INT NOT NULL,
                rating INT NOT NULL,
                title VARCHAR(200),
                review_text TEXT,
                is_verified_purchase TINYINT(1) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except:
        pass

    # Create coupons table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_coupons (
                id INT AUTO_INCREMENT PRIMARY KEY,
                coupon_code VARCHAR(50) UNIQUE NOT NULL,
                coupon_type VARCHAR(20) NOT NULL,
                discount_value DECIMAL(10, 2) NOT NULL,
                min_order_amount DECIMAL(10, 2) DEFAULT 0,
                max_discount_amount DECIMAL(10, 2) DEFAULT NULL,
                valid_from DATETIME NOT NULL,
                valid_until DATETIME NOT NULL,
                is_active TINYINT(1) DEFAULT 1
            )
        """)
    except:
        pass

    # Create notifications table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT DEFAULT NULL,
                title VARCHAR(200) NOT NULL,
                message TEXT NOT NULL,
                notification_type VARCHAR(50) DEFAULT 'system',
                is_read TINYINT(1) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except:
        pass

    # Create delivery boy table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_delivery_boy (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                password VARCHAR(255) NOT NULL,
                vehicle_number VARCHAR(20),
                is_available TINYINT(1) DEFAULT 1,
                is_active TINYINT(1) DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except:
        pass

    mysql.connection.commit()
    cur.close()

# Initialize on startup
with app.app_context():
    init_database()

    # Create default admin if not exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_adminsign WHERE email=%s", ("sankettippe9766@gmail.com",))
    if not cur.fetchone():
        hashed = bcrypt.hashpw("sanket9766".encode('utf-8'), bcrypt.gensalt())
        cur.execute("INSERT INTO tbl_adminsign(full_name, email, phone_number, password, confirm_password) VALUES (%s,%s,%s,%s,%s)",
                    ("Sanket Tippe", "sankettippe9766@gmail.com", "9766575428", hashed.decode('utf-8'), hashed.decode('utf-8')))
        mysql.connection.commit()
    cur.close()

# ============================================
# PUBLIC ROUTES
# ============================================

@app.route("/")
def home():
    cur = mysql.connection.cursor()

    # Get featured products
    cur.execute("SELECT * FROM tbl_addproduct WHERE is_active=1 AND is_featured=1 ORDER BY id DESC LIMIT 8")
    featured_products = cur.fetchall()

    # Get new arrivals
    cur.execute("SELECT * FROM tbl_addproduct WHERE is_active=1 AND is_new_arrival=1 ORDER BY id DESC LIMIT 8")
    new_arrivals = cur.fetchall()

    # Get flash sale products
    cur.execute("SELECT * FROM tbl_addproduct WHERE is_active=1 AND is_flash_sale=1 AND flash_sale_end > NOW() ORDER BY id DESC LIMIT 4")
    flash_sale_products = cur.fetchall()

    # Get categories
    cur.execute("SELECT * FROM tbl_addcategory WHERE is_active=1 ORDER BY sort_order ASC")
    categories = cur.fetchall()

    # Get settings
    settings = get_settings()

    cur.close()

    return render_template('home.html',
                         featured_products=featured_products,
                         new_arrivals=new_arrivals,
                         flash_sale_products=flash_sale_products,
                         categories=categories,
                         settings=settings)

@app.route("/about")
def about():
    settings = get_settings()
    return render_template('about.html', settings=settings)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    settings = get_settings()
    if request.method == 'POST':
        details = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_complaint(first_name, last_name, email, number, complaint_type, complaint_descrip) VALUES (%s,%s,%s,%s,%s,%s)",
                    (details.get('name'), '', details.get('email'), details.get('phone'), details.get('subject'), details.get('message')))
        mysql.connection.commit()
        cur.close()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', settings=settings)

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route("/usersign", methods=['POST', 'GET'])
def usersign():
    if request.method == "POST":
        details = request.form
        u_fname = details['u_fname']
        u_email = details['u_email']
        u_num = details['u_num']
        u_pass = details['u_pass']

        hashed_password = bcrypt.hashpw(u_pass.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM tbl_usersign WHERE email=%s", (u_email,))
        if cur.fetchone():
            cur.close()
            flash('Email already registered!', 'danger')
            return redirect(url_for('usersign'))

        cur.execute("insert into tbl_usersign(full_name, email, phone_number, password, confirm_password, loyalty_points) values (%s,%s,%s,%s,%s,%s)",
                    (u_fname, u_email, u_num, hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), 100))  # 100 bonus points
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! You earned 100 loyalty points!', 'success')
        return redirect(url_for('userlog'))
    return render_template("usersign.html")

@app.route("/userlog", methods=['POST', 'GET'])
def userlog():
    if request.method == "POST":
        details = request.form
        user_email = details['user_email']
        user_pass = details['user_pass']

        cur = mysql.connection.cursor()
        cur.execute("select * from tbl_usersign where email=%s", (user_email,))
        data = cur.fetchone()

        if data:
            stored_password = data[4]
            try:
                if stored_password.startswith('$2') and len(stored_password) >= 60:
                    if bcrypt.checkpw(user_pass.encode('utf-8'), stored_password.encode('utf-8')):
                        session['uid'] = data[0]
                        session['unm'] = data[1]
                        session['uadd'] = data[5]
                        session['unum'] = data[3]
                        session['loyalty_points'] = data[14] if len(data) > 14 else 0

                        if 'cart_session' in session:
                            cur.execute("UPDATE tbl_cart SET user_id=%s WHERE session_id=%s", (session['uid'], session['cart_session']))
                            mysql.connection.commit()

                        cur.close()
                        return redirect('view_category')
                else:
                    if stored_password == user_pass:
                        hashed_password = bcrypt.hashpw(user_pass.encode('utf-8'), bcrypt.gensalt())
                        cur.execute("UPDATE tbl_usersign SET password=%s, confirm_password=%s WHERE email=%s",
                                    (hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), user_email))
                        mysql.connection.commit()

                        session['uid'] = data[0]
                        session['unm'] = data[1]
                        session['uadd'] = data[5]
                        session['unum'] = data[3]
                        cur.close()
                        return redirect('view_category')
            except Exception:
                if stored_password == user_pass:
                    session['uid'] = data[0]
                    session['unm'] = data[1]
                    session['uadd'] = data[5]
                    session['unum'] = data[3]
                    cur.close()
                    return redirect('view_category')

        cur.close()
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('userlog'))
    return render_template('userlog.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/forgot", methods=['POST', 'GET'])
def forgot():
    if request.method == "POST":
        details = request.form
        uemail = details['uemail']
        unewpass = details['unewpass']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM tbl_usersign WHERE email=%s", (uemail,))
        if cur.fetchone():
            hashed_password = bcrypt.hashpw(unewpass.encode('utf-8'), bcrypt.gensalt())
            cur.execute("UPDATE tbl_usersign SET password=%s, confirm_password=%s WHERE email=%s",
                        (hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), uemail))
            mysql.connection.commit()
            cur.close()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('userlog'))
        cur.close()
        flash('Email not found!', 'danger')
    return render_template('forgot.html')

# ============================================
# ADMIN ROUTES
# ============================================

@app.route("/adminlog", methods=['POST', 'GET'])
def adminlog():
    if request.method == "POST":
        details = request.form
        ad_email = details['ad_email']
        ad_pass = details['ad_pass']

        cur = mysql.connection.cursor()
        cur.execute("select * from tbl_adminsign where email=%s", (ad_email,))
        data = cur.fetchone()

        if data:
            stored_password = data[4]
            try:
                if stored_password.startswith('$2') and len(stored_password) >= 60:
                    if bcrypt.checkpw(ad_pass.encode('utf-8'), stored_password.encode('utf-8')):
                        session['admin_id'] = data[0]
                        session['admin_name'] = data[1]
                        cur.close()
                        return redirect('dash')
                else:
                    if stored_password == ad_pass:
                        hashed_password = bcrypt.hashpw(ad_pass.encode('utf-8'), bcrypt.gensalt())
                        cur.execute("UPDATE tbl_adminsign SET password=%s, confirm_password=%s WHERE email=%s",
                                    (hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), ad_email))
                        mysql.connection.commit()
                        session['admin_id'] = data[0]
                        session['admin_name'] = data[1]
                        cur.close()
                        return redirect('dash')
            except Exception:
                if stored_password == ad_pass:
                    session['admin_id'] = data[0]
                    session['admin_name'] = data[1]
                    cur.close()
                    return redirect('dash')

        cur.close()
        flash('Invalid email or password!', 'danger')
    return render_template("/adminlog.html")

@app.route("/adminsign", methods=['POST', 'GET'])
def adminsign():
    if request.method == "POST":
        details = request.form
        ad_fnm = details['ad_fnm']
        ad_email = details['ad_email']
        ad_num = details['ad_num']
        ad_pss = details['ad_pss']

        hashed_password = bcrypt.hashpw(ad_pss.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("insert into tbl_adminsign(full_name, email, phone_number, password, confirm_password) values (%s,%s,%s,%s,%s)",
                    (ad_fnm, ad_email, ad_num, hashed_password.decode('utf-8'), hashed_password.decode('utf-8')))
        mysql.connection.commit()
        cur.close()
        flash('Admin registered successfully!', 'success')
        return redirect(url_for('adminlog'))
    return render_template('adminsign.html')

@app.route("/admin_logout")
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    return redirect(url_for('home'))

@app.route("/dash")
def dash():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()

    # Get statistics
    cur.execute("SELECT COUNT(*) FROM tbl_usersign")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tbl_addproduct WHERE is_active=1")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tbl_booking")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(final_amount) FROM tbl_booking WHERE payment_status='paid'")
    total_revenue = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM tbl_booking WHERE booking_status='Pending'")
    pending_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tbl_complaint WHERE status='pending'")
    pending_complaints = cur.fetchone()[0]

    # Get recent orders
    cur.execute("SELECT * FROM tbl_booking ORDER BY id DESC LIMIT 10")
    recent_orders = cur.fetchall()

    cur.close()

    return render_template('dash.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         pending_orders=pending_orders,
                         pending_complaints=pending_complaints,
                         recent_orders=recent_orders)

# ============================================
# CATEGORY ROUTES
# ============================================

@app.route("/addcategory", methods=['POST', 'GET'])
def addcategory():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    if request.method == "POST":
        details = request.form
        cname = details['cname']
        cimage = request.files['cimage']

        filename = secure_filename(cimage.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cimage.save(file_path)

        cdesc = details['cdesc']
        cur = mysql.connection.cursor()
        cur.execute("insert into tbl_addcategory(category_name, category_image, description) values (%s,%s,%s)", (cname, file_path, cdesc))
        mysql.connection.commit()
        cur.close()
        flash('Category added successfully!', 'success')
        return redirect(url_for('category_list'))
    return render_template('addcategory.html')

@app.route('/category_list')
def category_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("select * from tbl_addcategory ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('category_list.html', value=data)

@app.route('/delete_category/<int:c_id>')
def delete_category(c_id):
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_addcategory WHERE id=%s", ([c_id]))
    mysql.connection.commit()
    cur.close()
    flash('Category deleted!', 'success')
    return redirect(url_for('category_list'))

# ============================================
# PRODUCT ROUTES
# ============================================

@app.route("/addproduct", methods=['POST', 'GET'])
def addproduct():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_addcategory WHERE is_active=1")
    categories = cur.fetchall()
    cur.close()

    if request.method == "POST":
        details = request.form
        product_nm = details['product_nm']
        product_br = details['product_br']
        product_price = float(details['product_price'])
        product_quan = int(details['product_quan'])
        product_desc = details['product_desc']
        product_cat = details['product_cat']
        product_img = request.files['product_img']

        filename = secure_filename(product_img.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        product_img.save(file_path)

        original_price = product_price
        is_featured = 1 if details.get('is_featured') else 0
        is_new = 1 if details.get('is_new_arrival') else 0
        is_flash = 1 if details.get('is_flash_sale') else 0

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO tbl_addproduct
            (product_name, brand, price, original_price, quantity, description, category, product_image,
             is_featured, is_new_arrival, is_flash_sale, flash_sale_price, flash_sale_end)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (product_nm, product_br, product_price, original_price, product_quan, product_desc,
                     product_cat, file_path, is_featured, is_new, is_flash,
                     details.get('flash_sale_price'), details.get('flash_sale_end')))
        mysql.connection.commit()
        cur.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_list'))
    return render_template('addproduct.html', categories=categories)

@app.route('/product_list')
def product_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.*, c.category_name
        FROM tbl_addproduct p
        LEFT JOIN tbl_addcategory c ON p.category = c.id
        ORDER BY p.id DESC
    """)
    data = cur.fetchall()
    cur.close()
    return render_template('product_list.html', value=data)

@app.route('/update_product', methods=['POST', 'GET'])
def update_product():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    if request.method == "POST":
        details = request.form
        p_id = details['p_id']
        product_nm = details['product_nm']
        product_br = details['product_br']
        product_price = details['product_price']
        product_quan = details['product_quan']
        product_desc = details['product_desc']
        product_cat = details['product_cat']

        cur = mysql.connection.cursor()

        if 'product_img' in request.files and request.files['product_img'].filename:
            product_img = request.files['product_img']
            filename = secure_filename(product_img.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            product_img.save(file_path)
            cur.execute("""UPDATE tbl_addproduct SET product_name=%s, brand=%s, price=%s, quantity=%s,
                description=%s, category=%s, product_image=%s WHERE id=%s""",
                        (product_nm, product_br, product_price, product_quan, product_desc, product_cat, file_path, p_id))
        else:
            cur.execute("""UPDATE tbl_addproduct SET product_name=%s, brand=%s, price=%s, quantity=%s,
                description=%s, category=%s WHERE id=%s""",
                        (product_nm, product_br, product_price, product_quan, product_desc, product_cat, p_id))

        mysql.connection.commit()
        cur.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_list'))

    p_id = request.args.get('p_id')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_addproduct WHERE id=%s", ([p_id]))
    product = cur.fetchone()
    cur.execute("SELECT * FROM tbl_addcategory")
    categories = cur.fetchall()
    cur.close()
    return render_template('update_product.html', product=product, categories=categories)

@app.route('/delete_product/<int:p_id>')
def delete_product(p_id):
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tbl_addproduct SET is_active=0 WHERE id=%s", ([p_id]))
    mysql.connection.commit()
    cur.close()
    flash('Product deleted!', 'success')
    return redirect(url_for('product_list'))

# ============================================
# CUSTOMER PRODUCT VIEWING
# ============================================

@app.route("/view_category")
def view_category():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_addcategory WHERE is_active=1 ORDER BY sort_order ASC")
    data = cur.fetchall()
    cur.close()
    return render_template("view_category.html", value=data)

@app.route("/view_product", methods=['GET', 'POST'])
def view_product():
    cur = mysql.connection.cursor()

    # Get products by category
    category_id = session.get('mnm')
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    sort_by = request.args.get('sort', 'newest')

    query = "SELECT * FROM tbl_addproduct WHERE is_active=1"
    params = []

    if category_id:
        query += " AND category = %s"
        params.append(category_id)

    if search_query:
        query += " AND (product_name LIKE %s OR brand LIKE %s OR description LIKE %s)"
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param, search_param])

    if brand_filter:
        query += " AND brand = %s"
        params.append(brand_filter)

    if min_price:
        query += " AND price >= %s"
        params.append(float(min_price))

    if max_price:
        query += " AND price <= %s"
        params.append(float(max_price))

    if sort_by == 'price_low':
        query += " ORDER BY price ASC"
    elif sort_by == 'price_high':
        query += " ORDER BY price DESC"
    elif sort_by == 'rating':
        query += " ORDER BY rating DESC"
    else:
        query += " ORDER BY id DESC"

    cur.execute(query, params)
    data = cur.fetchall()

    # Get all brands for filter
    cur.execute("SELECT DISTINCT brand FROM tbl_addproduct WHERE is_active=1")
    brands = cur.fetchall()

    # Get category name
    category_name = ''
    if category_id:
        cur.execute("SELECT category_name FROM tbl_addcategory WHERE id=%s", ([category_id]))
        cat = cur.fetchone()
        category_name = cat[0] if cat else ''

    cur.close()
    return render_template("view_product.html", value=data, brands=brands,
                           category_name=category_name, search_query=search_query)

@app.route('/view', methods=['POST'])
def view():
    if request.method == "POST":
        details = request.form
        session['mnm'] = details['mnm']
    return redirect('view_product')

@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    cur = mysql.connection.cursor()

    # Increment views
    cur.execute("UPDATE tbl_addproduct SET views = views + 1 WHERE id=%s", ([product_id]))

    # Get product details
    cur.execute("""
        SELECT p.*, c.category_name
        FROM tbl_addproduct p
        LEFT JOIN tbl_addcategory c ON p.category = c.id
        WHERE p.id = %s
    """, ([product_id]))
    product = cur.fetchone()

    if not product:
        cur.close()
        flash('Product not found!', 'danger')
        return redirect(url_for('view_category'))

    # Get product reviews
    cur.execute("""
        SELECT r.*, u.full_name
        FROM tbl_product_reviews r
        LEFT JOIN tbl_usersign u ON r.user_id = u.id
        WHERE r.product_id = %s AND r.is_approved = 1
        ORDER BY r.id DESC
        LIMIT 10
    """, ([product_id]))
    reviews = cur.fetchall()

    # Get related products
    cur.execute("""
        SELECT * FROM tbl_addproduct
        WHERE category = %s AND id != %s AND is_active = 1
        LIMIT 4
    """, (product[9], product_id))
    related_products = cur.fetchall()

    # Check if in wishlist
    in_wishlist = False
    if 'uid' in session:
        cur.execute("SELECT id FROM tbl_wishlist WHERE user_id=%s AND product_id=%s", (session['uid'], product_id))
        in_wishlist = True if cur.fetchone() else False

    cur.close()

    return render_template('product_details.html', product=product, reviews=reviews,
                           related_products=related_products, in_wishlist=in_wishlist)

# ============================================
# CART ROUTES
# ============================================

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))

    if 'uid' not in session:
        if 'cart_session' not in session:
            session['cart_session'] = str(random.randint(100000, 999999))

    cur = mysql.connection.cursor()

    # Check if product exists
    cur.execute("SELECT id, price, quantity FROM tbl_addproduct WHERE id=%s AND is_active=1", ([product_id]))
    product = cur.fetchone()

    if not product:
        cur.close()
        flash('Product not found!', 'danger')
        return redirect(url_for('view_product'))

    if product[2] < quantity:
        cur.close()
        flash('Insufficient stock!', 'danger')
        return redirect(url_for('product_details', product_id=product_id))

    # Check if already in cart
    if 'uid' in session:
        cur.execute("SELECT id, quantity FROM tbl_cart WHERE user_id=%s AND product_id=%s",
                   (session['uid'], product_id))
    elif 'cart_session' in session:
        cur.execute("SELECT id, quantity FROM tbl_cart WHERE session_id=%s AND product_id=%s",
                   (session['cart_session'], product_id))
    else:
        cur.close()
        flash('Please login to add to cart!', 'danger')
        return redirect(url_for('userlog'))

    cart_item = cur.fetchone()

    if cart_item:
        new_quantity = cart_item[1] + quantity
        if product[2] >= new_quantity:
            cur.execute("UPDATE tbl_cart SET quantity=%s WHERE id=%s", (new_quantity, cart_item[0]))
        else:
            cur.close()
            flash('Insufficient stock!', 'danger')
            return redirect(url_for('product_details', product_id=product_id))
    else:
        if 'uid' in session:
            cur.execute("INSERT INTO tbl_cart(user_id, product_id, quantity) VALUES (%s,%s,%s)",
                       (session['uid'], product_id, quantity))
        else:
            cur.execute("INSERT INTO tbl_cart(session_id, product_id, quantity) VALUES (%s,%s,%s)",
                       (session['cart_session'], product_id, quantity))

    mysql.connection.commit()
    cur.close()

    flash('Added to cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cur = mysql.connection.cursor()

    cart_items = []
    subtotal = 0

    if 'uid' in session:
        cur.execute("""
            SELECT c.id, c.quantity, p.id, p.product_name, p.price, p.product_image, p.quantity as stock
            FROM tbl_cart c
            JOIN tbl_addproduct p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, ([session['uid']]))
    elif 'cart_session' in session:
        cur.execute("""
            SELECT c.id, c.quantity, p.id, p.product_name, p.price, p.product_image, p.quantity as stock
            FROM tbl_cart c
            JOIN tbl_addproduct p ON c.product_id = p.id
            WHERE c.session_id = %s
        """, ([session['cart_session']]))
    else:
        cur.close()
        return render_template('cart.html', cart_items=[], subtotal=0)

    cart_items = cur.fetchall()

    for item in cart_items:
        subtotal += float(item[4]) * item[1]

    # Get available coupons
    cur.execute("SELECT * FROM tbl_coupons WHERE is_active = 1 AND valid_until > NOW() AND min_order_amount <= %s", (subtotal,))
    coupons = cur.fetchall()

    cur.close()

    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, coupons=coupons)

@app.route('/update_cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    quantity = int(request.form.get('quantity', 1))

    cur = mysql.connection.cursor()

    if quantity > 0:
        cur.execute("UPDATE tbl_cart SET quantity=%s WHERE id=%s", (quantity, cart_id))
    else:
        cur.execute("DELETE FROM tbl_cart WHERE id=%s", ([cart_id]))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_cart WHERE id=%s", ([cart_id]))
    mysql.connection.commit()
    cur.close()
    flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))

# ============================================
# CHECKOUT & ORDER ROUTES
# ============================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cur = mysql.connection.cursor()

    # Get cart items
    if 'uid' in session:
        cur.execute("""
            SELECT c.id, c.quantity, p.id, p.product_name, p.price, p.product_image, p.quantity as stock
            FROM tbl_cart c
            JOIN tbl_addproduct p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, ([session['uid']]))
    elif 'cart_session' in session:
        cur.execute("""
            SELECT c.id, c.quantity, p.id, p.product_name, p.price, p.product_image, p.quantity as stock
            FROM tbl_cart c
            JOIN tbl_addproduct p ON c.product_id = p.id
            WHERE c.session_id = %s
        """, ([session['cart_session']]))
    else:
        cur.close()
        return redirect(url_for('cart'))

    cart_items = cur.fetchall()

    if not cart_items:
        cur.close()
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))

    # Calculate totals
    subtotal = sum(float(item[4]) * item[1] for item in cart_items)
    shipping = 0 if subtotal >= 1000 else 100
    tax = (subtotal * 18) / 100
    total = subtotal + shipping + tax

    # Apply coupon if selected
    coupon_discount = 0
    coupon_code = request.args.get('coupon', '')
    if coupon_code:
        cur.execute("""
            SELECT * FROM tbl_coupons
            WHERE coupon_code = %s AND is_active = 1 AND valid_until > NOW() AND min_order_amount <= %s
        """, (coupon_code, subtotal))
        coupon = cur.fetchone()

        if coupon:
            if coupon[2] == 'percentage':
                coupon_discount = (subtotal * float(coupon[3])) / 100
                if coupon[5] and coupon_discount > float(coupon[5]):
                    coupon_discount = float(coupon[5])
            else:
                coupon_discount = float(coupon[3])

            total = total - coupon_discount
            session['applied_coupon'] = coupon_code

    # Get user details
    user = None
    if 'uid' in session:
        cur.execute("SELECT * FROM tbl_usersign WHERE id=%s", ([session['uid']]))
        user = cur.fetchone()

    cur.close()

    if request.method == 'POST':
        details = request.form

        # Create order
        invoice_number = generate_invoice_number()
        order_number = generate_order_number()

        full_name = details.get('full_name')
        email = details.get('email')
        phone = details.get('phone')
        address = details.get('address')
        city = details.get('city')
        state = details.get('state')
        pincode = details.get('pincode')

        # Create booking for each cart item
        for item in cart_items:
            cur = mysql.connection.cursor()
            cur.execute("""INSERT INTO tbl_booking
                (user_id, invoice_number, order_number, full_name, email_address, contact_number,
                 shipping_address, shipping_city, shipping_state, shipping_pincode,
                 enter_product, product_id, price, quantity, total_amount, coupon_discount,
                 shipping_charge, gst_amount, final_amount, booking_status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')""",
                       (session.get('uid'), invoice_number, order_number, full_name, email, phone,
                        address, city, state, pincode,
                        item[3], item[2], item[4], item[1], float(item[4]) * item[1],
                        coupon_discount, shipping, tax, total))

            # Get last inserted ID
            cur.execute("SELECT LAST_INSERT_ID()")
            booking_id = cur.fetchone()[0]
            session['booking_id'] = booking_id

            # Update product stock
            cur.execute("UPDATE tbl_addproduct SET quantity = quantity - %s WHERE id=%s",
                       (item[1], item[2]))

            mysql.connection.commit()
            cur.close()

        # Clear cart
        if 'uid' in session:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM tbl_cart WHERE user_id=%s", ([session['uid']]))
            mysql.connection.commit()
            cur.close()

        # Clear applied coupon
        session.pop('applied_coupon', None)

        return redirect(url_for('payment_method'))

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal,
                         shipping=shipping, tax=tax, total=total, user=user,
                         coupon_discount=coupon_discount)

@app.route('/payment_method')
def payment_method():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_booking WHERE id=%s", ([session['booking_id']]))
    order = cur.fetchone()
    cur.close()

    if not order:
        return redirect(url_for('cart'))

    return render_template('method.html', order=order)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    coupon_code = request.form.get('coupon_code')
    return redirect(url_for('checkout', coupon=coupon_code))

# ============================================
# PAYMENT ROUTES
# ============================================

@app.route('/upi', methods=['POST', 'GET'])
def upi():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    if request.method == "POST":
        details = request.form
        upi_name = details['upi_name']
        upi_email = details['upi_email']
        upi_number = details['upi_number']
        upi_id = details['upi_id']
        upi_amount = details['upi_amount']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_upi(full_name, email_address, phone_number, upi_id, amount) VALUES (%s,%s,%s,%s,%s)",
                   (upi_name, upi_email, upi_number, upi_id, upi_amount))

        cur.execute("""UPDATE tbl_booking SET payment_method='UPI', payment_date=NOW(),
            payment_status='paid', booking_status='Confirmed' WHERE id=%s""",
                   ([session['booking_id']]))

        mysql.connection.commit()
        cur.close()

        # Add loyalty points
        if 'uid' in session:
            cur = mysql.connection.cursor()
            points = int(float(upi_amount) / 10)
            cur.execute("UPDATE tbl_usersign SET loyalty_points = loyalty_points + %s WHERE id=%s",
                       (points, session['uid']))
            cur.execute("INSERT INTO tbl_loyalty_points(user_id, points, transaction_type, description, order_id) VALUES (%s,%s,%s,%s,%s)",
                       (session['uid'], points, 'earn', 'Purchase reward', session['booking_id']))
            mysql.connection.commit()
            cur.close()

        session.pop('booking_id', None)
        flash('Payment successful! You earned loyalty points!', 'success')
        return redirect(url_for('myord'))
    return render_template("/upi.html")

@app.route("/cd", methods=['POST', 'GET'])
def cd():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    if request.method == "POST":
        details = request.form
        cd_nm = details['cd_nm']
        cd_num = details['cd_num']
        cd_ex = details['cd_ex']
        cd_cvv = details['cd_cvv']
        cd_amount = details['cd_amount']

        cur = mysql.connection.cursor()
        cur.execute("insert into tbl_cd(name, card_number, expiry_date, cvv, total_amount) values (%s,%s,%s,%s,%s)",
                   (cd_nm, cd_num, cd_ex, cd_cvv, cd_amount))

        cur.execute("""UPDATE tbl_booking SET payment_method='Card', payment_date=NOW(),
            payment_status='paid', booking_status='Confirmed' WHERE id=%s""",
                   ([session['booking_id']]))

        mysql.connection.commit()
        cur.close()

        session.pop('booking_id', None)
        flash('Payment successful!', 'success')
        return redirect(url_for('myord'))
    return render_template("/cd.html")

@app.route('/cod_form', methods=['GET', 'POST'])
def cod_form():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    cur = mysql.connection.cursor()
    cur.execute("""UPDATE tbl_booking SET payment_method='Cash on Delivery', payment_date=NOW(),
        booking_status='Confirmed' WHERE id=%s""",
               ([session['booking_id']]))
    mysql.connection.commit()
    cur.close()

    session.pop('booking_id', None)
    flash('Order placed successfully! You will pay on delivery.', 'success')
    return redirect(url_for('myord'))

@app.route('/qr_payment')
def qr_payment():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT total_amount FROM tbl_booking WHERE id=%s", ([session['booking_id']]))
    result = cur.fetchone()
    cur.close()

    if not result:
        return redirect(url_for('cart'))

    amount = result[0]
    upi_id = "sankettippe9766@oksbi"

    # Generate QR code
    qr_data = f"upi://pay?pa={upi_id}&pn=Computer%20Sales&am={amount}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    # Set payment timer
    import time
    session['payment_start_time'] = int(time.time())

    return render_template('qr_payment.html', qr_image=qr_image, amount=amount, upi_id=upi_id)

@app.route('/qr_payment_complete')
def qr_payment_complete():
    if 'booking_id' not in session:
        return redirect(url_for('cart'))

    cur = mysql.connection.cursor()
    cur.execute("""UPDATE tbl_booking SET payment_method='UPI QR', payment_date=NOW(),
        payment_status='paid', booking_status='Confirmed' WHERE id=%s""",
               ([session['booking_id']]))

    # Get amount for loyalty points
    cur.execute("SELECT total_amount, user_id FROM tbl_booking WHERE id=%s", ([session['booking_id']]))
    order = cur.fetchone()

    if order and order[1]:
        points = int(float(order[0]) / 10)
        cur.execute("UPDATE tbl_usersign SET loyalty_points = loyalty_points + %s WHERE id=%s",
                   (points, order[1]))
        cur.execute("INSERT INTO tbl_loyalty_points(user_id, points, transaction_type, description, order_id) VALUES (%s,%s,%s,%s,%s)",
                   (order[1], points, 'earn', 'Purchase reward', session['booking_id']))

    mysql.connection.commit()
    cur.close()

    session.pop('booking_id', None)
    flash('Payment successful!', 'success')
    return redirect(url_for('myord'))

# ============================================
# ORDER MANAGEMENT ROUTES
# ============================================

@app.route('/myord')
def myord():
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, invoice_number, order_number, enter_product, price, quantity,
        total_amount, booking_status, payment_method, payment_status, booking_date
        FROM tbl_booking WHERE user_id=%s ORDER BY id DESC""",
               ([session['uid']]))
    data = cur.fetchall()
    cur.close()
    return render_template('myord.html', value=data)

@app.route('/booking_list')
def booking_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_booking ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('booking_list.html', value=data)

@app.route('/update_booking', methods=['POST'])
def update_booking():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    if request.method == "POST":
        details = request.form
        book_id = details['b_id']
        status = details['status']
        delivery_otp = details.get('delivery_otp', '')

        cur = mysql.connection.cursor()

        if delivery_otp:
            cur.execute("UPDATE tbl_booking SET booking_status=%s, delivery_otp=%s WHERE id=%s",
                       (status, delivery_otp, book_id))
        else:
            cur.execute("UPDATE tbl_booking SET booking_status=%s WHERE id=%s", (status, book_id))

        # Add status history
        cur.execute("INSERT INTO tbl_order_status_history(order_id, status, notes) VALUES (%s,%s,%s)",
                   (book_id, status, f'Order status updated to {status}'))

        mysql.connection.commit()
        cur.close()
        flash('Order updated!', 'success')
    return redirect(url_for('booking_list'))

@app.route('/invoice/<int:booking_id>')
def invoice(booking_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_booking WHERE id=%s", (booking_id,))
    data = cur.fetchone()
    cur.close()

    if data:
        return render_template('invoice.html', order=data)
    flash('Order not found!', 'danger')
    return redirect(url_for('myord'))

@app.route('/cancel_order/<int:booking_id>')
def cancel_order(booking_id):
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, booking_status, is_canceled, product_id, quantity FROM tbl_booking WHERE id=%s AND user_id=%s",
               (booking_id, session['uid']))
    order = cur.fetchone()

    if order and order[2] == 0 and order[1] in ['Pending', 'Confirmed']:
        cur.execute("UPDATE tbl_booking SET is_canceled=1, cancellation_date=NOW(), booking_status='Canceled', payment_status='refunded' WHERE id=%s",
                   (booking_id,))

        # Restore product stock
        cur.execute("UPDATE tbl_addproduct SET quantity = quantity + %s WHERE id=%s",
                   (order[4], order[3]))

        mysql.connection.commit()
        cur.close()
        flash('Order cancelled!', 'success')
        return redirect(url_for('myord'))

    cur.close()
    flash('Order cannot be cancelled!', 'danger')
    return redirect(url_for('myord'))

# ============================================
# WISHLIST ROUTES
# ============================================

@app.route('/add_wishlist/<int:product_id>')
def add_wishlist(product_id):
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_wishlist WHERE user_id=%s AND product_id=%s", (session['uid'], product_id))
    if not cur.fetchone():
        cur.execute("INSERT INTO tbl_wishlist(user_id, product_id) VALUES (%s,%s)", (session['uid'], product_id))
        mysql.connection.commit()
        flash('Added to wishlist!', 'success')
    else:
        flash('Already in wishlist!', 'info')
    cur.close()
    return redirect(url_for('product_details', product_id=product_id))

@app.route('/wishlist')
def wishlist():
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.product_name, p.brand, p.price, p.product_image
        FROM tbl_addproduct p
        JOIN tbl_wishlist w ON p.id = w.product_id
        WHERE w.user_id = %s
    """, ([session['uid']]))
    data = cur.fetchall()
    cur.close()
    return render_template('wishlist.html', value=data)

@app.route('/remove_wishlist/<int:product_id>')
def remove_wishlist(product_id):
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_wishlist WHERE user_id=%s AND product_id=%s", (session['uid'], product_id))
    mysql.connection.commit()
    cur.close()
    flash('Removed from wishlist!', 'success')
    return redirect(url_for('wishlist'))

# ============================================
# REVIEW ROUTES
# ============================================

@app.route('/add_review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    if 'uid' not in session:
        return redirect(url_for('userlog'))

    details = request.form
    rating = int(details['rating'])
    title = details['title']
    review_text = details['review_text']

    cur = mysql.connection.cursor()

    # Check if user purchased this product
    cur.execute("SELECT id FROM tbl_booking WHERE user_id=%s AND product_id=%s AND booking_status='Delivered'", (session['uid'], product_id))
    verified = cur.fetchone()

    cur.execute("INSERT INTO tbl_product_reviews(product_id, user_id, rating, title, review_text, is_verified_purchase) VALUES (%s,%s,%s,%s,%s,%s)",
               (product_id, session['uid'], rating, title, review_text, 1 if verified else 0))

    # Update product rating
    cur.execute("SELECT AVG(rating), COUNT(*) FROM tbl_product_reviews WHERE product_id=%s AND is_approved=1", ([product_id]))
    avg_rating = cur.fetchone()

    if avg_rating[0]:
        cur.execute("UPDATE tbl_addproduct SET rating=%s, total_reviews=%s WHERE id=%s",
                   (round(float(avg_rating[0]), 1), avg_rating[1], product_id))

    mysql.connection.commit()
    cur.close()
    flash('Review submitted!', 'success')
    return redirect(url_for('product_details', product_id=product_id))

# ============================================
# FEEDBACK & COMPLAINT ROUTES
# ============================================

@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    if request.method == "POST":
        details = request.form
        feed_name = details['feed_name']
        feed_email = details['feed_email']
        feed_rating = details['feed_rating']
        feed_yourfeed = details['feed_yourfeed']

        cur = mysql.connection.cursor()
        cur.execute("insert into tbl_feedback(full_name, email_address, rating, your_feedback) values (%s,%s,%s,%s)",
                    (feed_name, feed_email, feed_rating, feed_yourfeed))
        mysql.connection.commit()
        cur.close()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('home'))
    return render_template("feedback.html")

@app.route('/feedback_list')
def feedback_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_feedback ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('feedback_list.html', value=data)

@app.route("/complaint", methods=['POST', 'GET'])
def complaint():
    if request.method == "POST":
        details = request.form
        cfirst_fnm = details['cfirst_fnm']
        clast_lnm = details['clast_lnm']
        c_email = details['c_email']
        c_num = details['c_num']
        c_type = details['c_type']
        c_descp = details['c_descp']

        cur = mysql.connection.cursor()
        cur.execute("insert into tbl_complaint(first_name, last_name, email, number, complaint_type, complaint_descrip) values (%s,%s,%s,%s,%s,%s)",
                    (cfirst_fnm, clast_lnm, c_email, c_num, c_type, c_descp))
        mysql.connection.commit()
        cur.close()
        flash('Complaint submitted!', 'success')
        return redirect(url_for('home'))
    return render_template("complaint.html")

@app.route('/complaint_list')
def complaint_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_complaint ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('complaint_list.html', value=data)

# ============================================
# COUPON ROUTES (ADMIN)
# ============================================

@app.route('/add_coupon', methods=['POST'])
def add_coupon():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    details = request.form
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO tbl_coupons(coupon_code, coupon_type, discount_value, min_order_amount,
        max_discount_amount, valid_from, valid_until) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
               (details['coupon_code'], details['coupon_type'], details['discount_value'],
                details.get('min_order_amount', 0), details.get('max_discount_amount'),
                details['valid_from'], details['valid_until']))
    mysql.connection.commit()
    cur.close()
    flash('Coupon created!', 'success')
    return redirect(url_for('coupon_list'))

@app.route('/coupon_list')
def coupon_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_coupons ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('coupon_list.html', value=data)

# ============================================
# AI CHATBOT ROUTES
# ============================================

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '').lower()

    # Simple AI responses
    responses = {
        'hello': 'Hello! Welcome to Sanket\'s Computers & Sales. How can I help you today?',
        'hi': 'Hi there! What can I help you with?',
        'laptop': 'We have a great selection of laptops! Check our products page to explore.',
        'laptops': 'We have a great selection of laptops! Check our products page to explore.',
        'computer': 'We offer various computers - desktops, laptops, and gaming PCs. What are you looking for?',
        'price': 'Our prices are competitive. You can browse products to see current prices.',
        'delivery': 'We deliver all over India! Standard delivery is free above Rs 1000.',
        'warranty': 'All our products come with manufacturer warranty. Extended warranty available on checkout.',
        'return': 'We offer 7-day return policy for most products. Check product details for specifics.',
        'refund': 'Refunds are processed within 5-7 business days after return approval.',
        'payment': 'We accept UPI, Card Payment, and Cash on Delivery.',
        'contact': 'You can reach us at sankettippe9766@gmail.com or call +91 9766575428.',
        'thank': 'You\'re welcome! Happy shopping!',
        'thanks': 'You\'re welcome! Happy shopping!'
    }

    # Find matching response
    response = 'I\'m here to help! Ask me about our products, delivery, payment options, or any other questions.'
    for key, value in responses.items():
        if key in message:
            response = value
            break

    # Add product recommendations for specific queries
    if 'recommend' in message or 'suggestion' in message:
        cur = mysql.connection.cursor()
        cur.execute("SELECT product_name, brand, price FROM tbl_addproduct WHERE is_active=1 ORDER BY rating DESC LIMIT 3")
        products = cur.fetchall()
        if products:
            response += '<br><br><strong>Top Rated Products:</strong><br>'
            for p in products:
                response += f'- {p[0]} by {p[1]} - Rs {p[2]}<br>'
        cur.close()

    return jsonify({'response': response, 'type': 'bot'})

# ============================================
# SEARCH ROUTES
# ============================================

@app.route('/search')
def search():
    query = request.args.get('q', '')
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM tbl_addproduct
        WHERE is_active=1 AND (product_name LIKE %s OR brand LIKE %s OR description LIKE %s)
        LIMIT 20
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    results = cur.fetchall()

    cur.close()
    return render_template('search_results.html', results=results, query=query)

# ============================================
# USER MANAGEMENT (ADMIN)
# ============================================

@app.route('/user_list')
def user_list():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_usersign ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template('user_list.html', value=data)

# ============================================
# ANALYTICS (ADMIN)
# ============================================

@app.route('/analytics')
def analytics():
    if 'admin_id' not in session:
        return redirect(url_for('adminlog'))

    cur = mysql.connection.cursor()

    # Get sales data
    cur.execute("""
        SELECT DATE(booking_date) as date, COUNT(*) as orders, SUM(final_amount) as revenue
        FROM tbl_booking
        WHERE booking_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY DATE(booking_date)
        ORDER BY date
    """)
    sales_data = cur.fetchall()

    # Get top products
    cur.execute("""
        SELECT enter_product, COUNT(*) as count
        FROM tbl_booking
        GROUP BY enter_product
        ORDER BY count DESC
        LIMIT 10
    """)
    top_products = cur.fetchall()

    # Get category-wise sales
    cur.execute("""
        SELECT c.category_name, COUNT(b.id) as orders
        FROM tbl_booking b
        JOIN tbl_addproduct p ON b.product_id = p.id
        JOIN tbl_addcategory c ON p.category = c.id
        GROUP BY c.category_name
        ORDER BY orders DESC
    """)
    category_sales = cur.fetchall()

    cur.close()
    return render_template('analytics.html', sales_data=sales_data, top_products=top_products, category_sales=category_sales)

# ============================================
# DELIVERY BOY ROUTES
# ============================================

@app.route('/delivery_login', methods=['GET', 'POST'])
def delivery_login():
    if request.method == 'POST':
        details = request.form
        email = details['email']
        password = details['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_delivery_boy WHERE email=%s AND is_active=1", (email,))
        data = cur.fetchone()

        if data and check_password_hash(data[4], password):
            session['delivery_id'] = data[0]
            session['delivery_name'] = data[1]
            cur.close()
            return redirect(url_for('delivery_dashboard'))
        cur.close()
        flash('Invalid credentials!', 'danger')

    return render_template('delivery_login.html')

@app.route('/delivery_logout')
def delivery_logout():
    session.pop('delivery_id', None)
    session.pop('delivery_name', None)
    return redirect(url_for('home'))

@app.route('/delivery_dashboard')
def delivery_dashboard():
    if 'delivery_id' not in session:
        return redirect(url_for('delivery_login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.*, a.category_name
        FROM tbl_booking b
        LEFT JOIN tbl_addproduct p ON b.product_id = p.id
        LEFT JOIN tbl_addcategory a ON p.category = a.id
        WHERE b.delivery_boy_id = %s
        ORDER BY b.id DESC
    """, ([session['delivery_id']]))
    orders = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM tbl_booking WHERE delivery_boy_id=%s AND booking_status='Out for Delivery'",
               ([session['delivery_id']]))
    active_deliveries = cur.fetchone()[0]

    cur.close()
    return render_template('delivery_dashboard.html', orders=orders, active_deliveries=active_deliveries)

# ============================================
# MAIN ROUTES
# ============================================

@app.route("/main")
def main():
    return render_template("/main.html")

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__=="__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)