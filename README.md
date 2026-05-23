# Computer Sales Management System

A web-based application built using **Flask (Python)** and **MySQL** to manage computer sales, admin login, customer bookings, invoices, and payments.

---

## New Features Added

- **Invoice View** - Customers can view their order invoices
- **Order Cancellation** - Customers can cancel pending/in-process orders
- **Payment Receipt** - Download/print payment receipts
- **QR Code Payment** - Scan QR to pay via UPI apps (Google Pay, PhonePe, Paytm)
- **Wishlist** - Add products to wishlist and view later
- **Password Hashing** - Secure password storage using bcrypt
- **Payment Timer** - 5-minute timer for QR payment completion

---

## UPI Payment Configuration

- **UPI ID:** sankettippe9766@oksbi (for QR payments)
- Update in `app.py` line 34

---

## Tech Stack

- **Backend:** Python (Flask)
- **Database:** MySQL (XAMPP)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Tools:** XAMPP, VS Code, Python 3.x

---

## Prerequisites

1. **Python 3.x** - Download from https://www.python.org/
2. **XAMPP** - Download from https://www.apachefriends.org/

---

## Step 1: Install Python Packages

Open Command Prompt and run:

```bash
pip install Flask flask-mysqldb Werkzeug mysqlclient qrcode Pillow
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

---

## Step 2: Start XAMPP

1. Open **XAMPP Control Panel**
2. Click **Start** next to **MySQL**
3. Click **Start** next to **Apache**
4. Both should show green "Running" status

---

## Step 3: Setup Database

1. Open browser and go to: `http://localhost/phpmyadmin`
2. Click **New** on the left sidebar
3. Database name: `computersales_db`
4. Click **Create**

5. Click on `computersales_db` (left sidebar)
6. Click **Import** tab
7. Click **Choose File**
8. Select: `computersales_db (6).sql` from project folder
9. Click **Go** at the bottom

---

## Step 4: Run the Project

Open Command Prompt in project folder:

```bash
cd "D:\Desktop\Speed Up\sachin\Computer Sales"

# Activate virtual environment
venv\Scripts\activate

# Run the app
python app.py
```

---

## Step 5: Open in Browser

```
http://localhost:5000
```

---

## Login Credentials

### Admin Login (Your Credentials)
| Name | Email | Password |
|------|-------|----------|
| Sanket Tippe | sankettippe9766@gmail.com | sanket9766 |

**Admin URL:** `http://localhost:5000/adminlog`

---

### Customer Login
Register a new account at: `http://localhost:5000/usersign`



**Customer URL:** `http://localhost:5000/userlog`

---

## Project Structure

```
Computer Sales/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── computersales_db (6).sql    # Database file
├── templates/                  # HTML files
│   ├── myord.html            # Customer orders page
│   ├── invoice.html          # Invoice view
│   ├── qr_payment.html       # QR payment page
│   ├── method.html           # Payment methods
│   └── ...
├── static/                     # CSS, JS, Images
└── venv/                       # Virtual environment
```

---

## Important Notes

1. **MySQL must be running** in XAMPP before starting the app
2. **Database name:** `computersales_db` (must match in app.py)
3. **Default MySQL credentials:** Username: `root`, Password: (empty)
4. **New columns** - The app automatically adds new database columns (payment_method, invoice_number, etc.) on first run
5. **UPI ID** - To change UPI ID for QR payments, edit line 32 in `app.py`:
   ```python
   UPI_ID = "computersales@upi"  # Change to your UPI ID
   ```

---

## Quick Reference

| Action | URL |
|--------|-----|
| Home | http://localhost:5000/ |
| User Login | http://localhost:5000/userlog |
| User Signup | http://localhost:5000/usersign |
| Admin Login | http://localhost:5000/adminlog |
| My Orders | http://localhost:5000/myord |
| View Products | http://localhost:5000/view_category |

---

## Troubleshooting

- **Module not found:** Run `pip install -r requirements.txt`
- **MySQL connection error:** Make sure MySQL is running in XAMPP
- **Database error:** Create `computersales_db` and import the SQL file
- **Port error:** If port 5000 is busy, change port in app.py: `app.run(port=5001)`

---

## Deploy to Web (Render - Free)

### Option 1: Deploy to Render

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/computer-sales.git
   git push -u origin main
   ```

2. **Create MySQL Database:**
   - Go to [Render.com](https://render.com)
   - Create a new PostgreSQL or MySQL database
   - Note the connection details

3. **Deploy:**
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Set environment variables:
     - `MYSQL_HOST` = your database host
     - `MYSQL_USER` = your database user
     - `MYSQL_PASSWORD` = your database password
     - `MYSQL_DB` = computersales_db
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

### Option 2: Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Create MySQL database in their dashboard
3. Configure WSGI file
4. Set environment variables

---

## Author

**Sanket Tippe**

---

## Project Status

✅ Completed with new features (Invoice, Cancel Order, Receipt Download, QR Payment)
✅ Ready for deployment
