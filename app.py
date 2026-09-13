from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_db_connection
from datetime import datetime, timedelta
from functools import wraps
import secrets
import os
import math

app = Flask(__name__)

from config import SECRET_KEY

app.secret_key = SECRET_KEY





# Login session lifetime = 24 hours
app.permanent_session_lifetime = timedelta(hours=12)

def login_required(view_function):

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(
                url_for(
                    "login",
                    next=request.path
                )
            )

        return view_function(*args, **kwargs)

    return wrapper





# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template("index.html")






# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    try:
        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed.", "error")
            return redirect(url_for("register"))

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""SELECT * FROM branchs""")
        branchs = cursor.fetchall()

    except Exception as e:

        print("Branch Data Fetch error:", e)
        flash("Registration failed.", "error")
        return redirect(url_for("register"))

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        father_name = request.form.get("father_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        image = request.files.get("image")
        branch_id = request.form.get("branch", "").strip()
        account_type = request.form.get("account_type", "")


        # Validation
        if not full_name or not email or not password:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        if not image or image.filename == "":
            flash("Please select a profile image.", "error")
            return redirect(url_for("register"))

        try:

            # Check existing email user table
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:

                # ###Account Duplicate check
                # id = existing_user["id"]
                # cursor.execute("SELECT id FROM accounts WHERE user_id = %s AND account_type = %s", (id, account_type))
                # existing_account = cursor.fetchone()

                # if existing_account:
                #     flash(f"You already have a {account_type} account.", "error")
                #     return redirect(url_for("register"))

                flash("An account with this email already exists.", "error")
                return redirect(url_for("register"))

                # another_account(cursor, existing_user)
                
                

            # Hash password
            password_hash = generate_password_hash(password)

            ##image file
            original_filename = secure_filename(image.filename)

            extension = os.path.splitext(original_filename)[1].lower()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

            image_filename = f"user_{timestamp}{extension}"

            image_path = os.path.join("static/uploads", image_filename)
            image.save(image_path)


            # Insert user
            cursor.execute(
                """
                INSERT INTO users
                (
                    branch_id,
                    full_name, 
                    father_name,
                    email, 
                    phone, 
                    password_hash,
                    image
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    branch_id,
                    full_name,
                    father_name,
                    email,
                    phone,
                    password_hash,
                    image_filename,
                ),
            )

            user_id = cursor.lastrowid

            # Generate cif number
            cif_number = generate_cif_number(cursor)
            # Create cif account
            cursor.execute(
                """
                INSERT INTO user_cif
                (
                    branch_id,
                    user_id,
                    cif
                )
                VALUES (%s, %s, %s)
            """,
                (branch_id, user_id, cif_number),
            )

            cif_id = cursor.lastrowid

            # Generate account number
            account_number = generate_account_number(cursor)

            # Create account
            cursor.execute(
                """
                INSERT INTO accounts
                (
                    user_id, 
                    branch_id,
                    cif_id,
                    account_number,
                    account_type
                )
                VALUES (%s, %s, %s, %s, %s)
            """,
                (user_id, branch_id, cif_id, account_number, account_type),
            )

            connection.commit()

            flash("Registration successful! Please login.", "success")

            return redirect(url_for("login"))

        except Exception as e:

            connection.rollback()

            print("Registration error:", e)

            flash("Registration failed.", "error")

            return redirect(url_for("register"))

        finally:

            cursor.close()
            connection.close()

    return render_template("register.html", branchs=branchs)









def another_account(cursor, user):
    pass







# =========================================================
# ACCOUNT NUMBER GENERATOR
# =========================================================

def generate_account_number(cursor):

    while True:

        number = "10" + secrets.token_hex(5).upper()

        number = number[:12]

        cursor.execute("SELECT id FROM accounts WHERE account_number = %s", (number,))

        existing = cursor.fetchone()

        if not existing:
            return number





# =========================================================
# CIF NUMBER GENERATOR
# =========================================================

def generate_cif_number(cursor):

    while True:

        number = secrets.token_hex(5).upper()

        number = number[:12]

        cursor.execute("SELECT id FROM user_cif WHERE cif = %s", (number,))

        existing = cursor.fetchone()

        if not existing:
            return number





# =========================================================
# REFERANCE NUMBER GENERATOR
# =========================================================

def generate_referance_number(cursor):

    while True:

        number = secrets.token_hex(8).upper()

        cursor.execute("SELECT id FROM transactions WHERE reference = %s", (number,))

        existing = cursor.fetchone()

        if not existing:
            return number





# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed.", "error")
            return redirect(url_for("login"))

        cursor = connection.cursor(dictionary=True)

        try:

            cursor.execute(
                """
                SELECT
                    users.id,
                    users.full_name,
                    users.email,
                    users.password_hash,
                    accounts.account_number,
                    accounts.status
                FROM users

                JOIN accounts
                ON users.id = accounts.user_id

                WHERE users.email = %s
            """,
                (email,),
            )

            user = cursor.fetchone()

            if not user:

                flash("Invalid email or password.", "error")

                return redirect(url_for("login"))

            if not check_password_hash(user["password_hash"], password):

                flash("Invalid email or password.", "error")

                return redirect(url_for("login"))

            if user["status"] == "blocked":

                flash("Your account is blocked.", "error")

                return redirect(url_for("login"))

            # Session
            session.clear()

            session.permanent = True
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        finally:

            cursor.close()
            connection.close()

    return render_template("login.html")





# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("index"))





# =========================================================
# FORGOT PASSWORD
# =========================================================

@app.route("/forgot-password", methods=["GET", "POST"])
@login_required
def forgot_password():

    if request.method == "POST":

        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")
        email = request.form.get("email", "")

        if new_password != confirm_password:
            flash("New Passwords do not match.", "error")
            return redirect(url_for("forgot_password"))

        if len(new_password) < 8:

            flash("New password must contain at least 8 characters.", "error")
            return redirect(url_for("forgot_password"))

        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed.", "error")
            return redirect(url_for("change_password"))

        print("Database successfully connected.")

        cursor = connection.cursor(dictionary=True)

        try:

            cursor.execute(
                """
                SELECT email, password_hash
                FROM users
                WHERE email = %s        
            """,
                (email,),
            )

            user = cursor.fetchone()

            if user is None:
                flash("User is not Found.", "error")
                return redirect(url_for("forgot_password"))

            # if check_password_hash(
            #     user["password_hash"],
            #     new_password
            # ):

            #     flash(
            #         "New password must be diffrent from your old password.",
            #         "error"
            #     )
            #     return redirect(url_for("forgot_password"))

            new_password_hash = generate_password_hash(new_password)

            cursor.execute(
                """
                UPDATE users
                SET password_hash = %s
                WHERE email = %s
            """,
                (new_password_hash, email),
            )

            flash("Password Successfully change.", "success")

            return redirect(url_for("login"))

        except Exception as e:

            connection.rollback()

            print("Forgot password error:", e)

            flash("Unable to change password.", "error")

            return redirect(url_for("forgot_password"))

        finally:

            cursor.close()
            connection.close()

    return render_template("forgot_password.html")





# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        old_password = request.form.get("old_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if new_password != confirm_password:
            flash("New Passwords do not match.", "error")
            return redirect(url_for("change_password"))

        if len(new_password) < 8:
            flash("New password must contain at least 8 characters.", "error")
            return redirect(url_for("change_password"))

        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed.", "error")
            return redirect(url_for("change_password"))

        print("Database successfully connected.")

        cursor = connection.cursor(dictionary=True)

        try:

            cursor.execute(
                """
                SELECT 
                    id, 
                    email, 
                    password_hash
                FROM users
                WHERE users.id = %s
            """,
                (session["user_id"],),
            )

            user = cursor.fetchone()

            # user not found
            if user is None:
                flash("User account not found.", "error")
                return redirect(url_for("/login"))

            ## old password validation
            if not check_password_hash(user["password_hash"], old_password):

                flash("Old password is Incorrect.", "error")

                return redirect(url_for("change_password"))

            ##prevent new password
            if check_password_hash(user["password_hash"], new_password):

                flash("New password must be diffrent from your old password.", "error")
                return redirect(url_for("change_password"))

            new_password_hash = generate_password_hash(new_password)

            ##update password
            cursor.execute(
                """
                UPDATE users 
                SET password_hash = %s
                WHERE id = %s 
                """,
                (new_password_hash, session["user_id"]),
            )

            connection.commit()

            flash("Password change successfully.", "success")

            return redirect(url_for("profile"))

        except Exception as e:

            connection.rollback()

            print("Change password error:", e)

            flash("Unable to change password.", "error")

            return redirect(url_for("change_password"))

        finally:

            cursor.close()
            connection.close()

    return render_template("change_password.html")






# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.full_name,
            users.email,
            users.phone,
            accounts.account_number,
            accounts.balance,
            accounts.status
        FROM users

        JOIN accounts
        ON users.id = accounts.user_id

        WHERE users.id = %s
    """,
        (session["user_id"],),
    )

    account = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("dashboard.html", account=account)





# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
@login_required
def profile():


    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.full_name,
            users.email,
            users.phone,
            users.image,
            users.created_at,
            accounts.account_number,
            accounts.balance,
            accounts.status,
            accounts.account_type,
            user_cif.cif,
            branchs.name,
            branchs.ifsc
        FROM accounts
        JOIN users ON users.id = accounts.user_id
        JOIN branchs ON branchs.id = accounts.branch_id
        JOIN user_cif ON user_cif.id = accounts.cif_id

        WHERE users.id = %s
    """,
        (session["user_id"],),
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("profile.html", user=user)





# =========================================================
# DEPOSIT
# =========================================================

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():

    if request.method == "POST":

        try:
            amount = float(request.form.get("amount", "0"))

        except ValueError:

            flash("Invalid amount.", "error")

            return redirect(url_for("deposit"))

        if amount <= 0:

            flash("Amount must be greater than zero.", "error")

            return redirect(url_for("deposit"))

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        try:

            connection.start_transaction()

            cursor.execute(
                """
                SELECT id
                FROM accounts
                WHERE user_id = %s
                AND status = 'active'
                FOR UPDATE
            """,
                (session["user_id"],),
            )

            account = cursor.fetchone()

            if not account:

                connection.rollback()

                flash("Active account not found.", "error")

                return redirect(url_for("deposit"))

            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE id = %s
            """,
                (amount, account["id"]),
            )

            reference = secrets.token_hex(8).upper()

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_id,
                    transaction_type,
                    amount,
                    reference,
                    description
                )
                VALUES (%s, 'deposit', %s, %s, %s)
            """,
                (account["id"], amount, reference, "Cash deposit"),
            )

            connection.commit()

            flash(f"₹{amount:,.2f} deposited successfully.", "success")

            return redirect(url_for("dashboard"))

        except Exception as e:

            connection.rollback()

            print("Deposit error:", e)

            flash("Deposit failed.", "error")

            return redirect(url_for("deposit"))

        finally:

            cursor.close()
            connection.close()

    return render_template("deposit.html")






# =========================================================
# WITHDRAW
# =========================================================

@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():

    if request.method == "POST":

        try:
            amount = float(request.form.get("amount", "0"))

        except ValueError:

            flash("Invalid amount.", "error")

            return redirect(url_for("withdraw"))

        if amount <= 0:

            flash("Amount must be greater than zero.", "error")

            return redirect(url_for("withdraw"))

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        try:

            connection.start_transaction()

            cursor.execute(
                """
                SELECT id, balance
                FROM accounts
                WHERE user_id = %s
                AND status = 'active'
                FOR UPDATE
            """,
                (session["user_id"],),
            )

            account = cursor.fetchone()

            if not account:

                connection.rollback()

                flash("Active account not found.", "error")

                return redirect(url_for("withdraw"))

            if float(account["balance"]) < amount:

                connection.rollback()

                flash("Insufficient balance.", "error")

                return redirect(url_for("withdraw"))

            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE id = %s
            """,
                (amount, account["id"]),
            )

            reference = secrets.token_hex(8).upper()

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_id,
                    transaction_type,
                    amount,
                    reference,
                    description
                )
                VALUES (%s, 'withdraw', %s, %s, %s)
            """,
                (account["id"], amount, reference, "Cash withdrawal"),
            )

            connection.commit()

            flash(f"₹{amount:,.2f} withdrawn successfully.", "success")

            return redirect(url_for("dashboard"))

        except Exception as e:

            connection.rollback()

            print("Withdraw error:", e)

            flash("Withdrawal failed.", "error")

            return redirect(url_for("withdraw"))

        finally:

            cursor.close()
            connection.close()

    return render_template("withdraw.html")





# =========================================================
# TRANSFER
# =========================================================

@app.route("/transfer", methods=["GET", "POST"])
def transfer():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        receiver_account = request.form.get("receiver_account", "").strip()

        try:

            amount = float(request.form.get("amount", "0"))

        except ValueError:

            flash("Invalid amount.", "error")

            return redirect(url_for("transfer"))

        if amount <= 0:

            flash("Amount must be greater than zero.", "error")

            return redirect(url_for("transfer"))

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        try:

            connection.start_transaction()

            # Sender
            cursor.execute(
                """
                SELECT
                    id,
                    account_number,
                    balance
                FROM accounts
                WHERE user_id = %s
                AND status = 'active'
                FOR UPDATE
            """,
                (session["user_id"],),
            )

            sender = cursor.fetchone()

            if not sender:

                connection.rollback()

                flash("Sender account not found.", "error")

                return redirect(url_for("transfer"))

            if sender["account_number"] == receiver_account:

                connection.rollback()

                flash("You cannot transfer to your own account.", "error")

                return redirect(url_for("transfer"))

            if float(sender["balance"]) < amount:

                connection.rollback()

                flash("Insufficient balance.", "error")

                return redirect(url_for("transfer"))

            # Receiver
            cursor.execute(
                """
                SELECT
                    id,
                    account_number
                FROM accounts
                WHERE account_number = %s
                AND status = 'active'
                FOR UPDATE
            """,
                (receiver_account,),
            )

            receiver = cursor.fetchone()

            if not receiver:

                connection.rollback()

                flash("Receiver account not found.", "error")

                return redirect(url_for("transfer"))

            reference = generate_referance_number(cursor)

            # Deduct sender
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE id = %s
            """,
                (amount, sender["id"]),
            )

            # Add receiver
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE id = %s
            """,
                (amount, receiver["id"]),
            )

            # Sender transaction
            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_id,
                    transaction_type,
                    amount,
                    reference,
                    description
                )
                VALUES (%s, 'transfer', %s, %s, %s)
            """,
                (sender["id"], amount, reference, f"Transfer to {receiver_account}"),
            )

            # Receiver transaction
            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_id,
                    transaction_type,
                    amount,
                    reference,
                    description
                )
                VALUES (%s, 'deposit', %s, %s, %s)
            """,
                (
                    receiver["id"],
                    amount,
                    reference,
                    f"Transfer from {sender['account_number']}",
                ),
            )

            connection.commit()

            flash(f"₹{amount:,.2f} transferred successfully.", "success")

            return redirect(url_for("dashboard"))

        except Exception as e:

            connection.rollback()

            print("Transfer error:", e)

            flash("Transfer failed.", "error")

            return redirect(url_for("transfer"))

        finally:

            cursor.close()
            connection.close()

    return render_template("transfer.html")






# =========================================================
# TRANSACTIONS
# =========================================================

@app.route("/transactions")
@login_required
def transactions():
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                transactions.transaction_type,
                transactions.amount,
                transactions.reference,
                transactions.description,
                transactions.created_at
            FROM transactions

            JOIN accounts
            ON transactions.account_id = accounts.id

            WHERE accounts.user_id = %s

            ORDER BY transactions.created_at DESC
        """,
            (session["user_id"],),
        )

        transaction_list = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    try:
        ITEMS_PER_PAGE = int(request.args.get("per_page", 5))
    except (ValueError, TypeError):
        ITEMS_PER_PAGE = 5

    # Only allow these values
    allowed_per_page = [5, 10, 20, 50]

    if ITEMS_PER_PAGE not in allowed_per_page:
        ITEMS_PER_PAGE = 5

    try:
        current_page = int(request.args.get("page", 1))
    except ValueError as e:
        print("Transaction Paggination Error: ", e)
        current_page = 1

    total_items = len(transaction_list)
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))
    current_page = max(1, min(current_page, total_pages))

    start_index = (current_page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    page_data = transaction_list[start_index:end_index]

    return render_template(
        "transactions.html",
        transactions=page_data,
        current_page=current_page,
        total_pages=total_pages,
        items_per_page=ITEMS_PER_PAGE
    )







@app.route("/transaction-report")
@login_required
def transaction_report():

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                t.id,
                t.transaction_type,
                t.amount,
                t.reference,
                t.created_at,

                YEAR(t.created_at) AS report_year,
                MONTH(t.created_at) AS report_month,
                MONTHNAME(t.created_at) AS month_name

            FROM transactions t
            INNER JOIN accounts a
                ON t.account_id = a.id

            WHERE a.user_id = %s

            ORDER BY
                t.created_at ASC,
                t.id ASC
        """, (user_id,))

        reports = cursor.fetchall()

        # Starting/opening balance
        running_balance = 0

        for report in reports:

            amount = float(report["amount"])

            if report["transaction_type"] == "deposit":
                running_balance += amount

            elif report["transaction_type"] in ("withdraw", "transfer"):
                running_balance -= amount

            report["net_balance"] = running_balance

        # Newest transaction first for display
        reports.reverse()

    except Exception as e:

        conn.rollback()
        print("Transaction Report Error: ", e)
        flash("Unable to fetch transaction report.", "error")

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "transaction_report.html",
        reports=reports
    )






# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "")

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))

        admin = cursor.fetchone()

        cursor.close()
        connection.close()

        if admin and check_password_hash(admin["password_hash"], password):

            session.clear()

            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]

            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin credentials.", "error")

    return render_template("admin/login.html")







# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    users = ""

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT COUNT(*) AS total_branchs FROM branchs")
        total_branchs = cursor.fetchone()["total_branchs"]

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()["total_users"]

        cursor.execute("SELECT COUNT(*) AS total_accounts FROM accounts")
        total_accounts = cursor.fetchone()["total_accounts"]

        cursor.execute(" SELECT COALESCE(SUM(balance), 0) AS total_balance FROM accounts")
        total_balance = cursor.fetchone()["total_balance"]

    except Exception as e:

        connection.rollback()
        print("Error: ", e)
        flash(
            "User data Fetch Problem.",
            "error"
        )

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_accounts=total_accounts,
        total_balance=total_balance,
        total_branch=total_branchs,
    )







# =========================================================
# ADMIN SHOW CUSTOMER LIST
# =========================================================

@app.route("/admin/customer/list")
def admin_customer_list():

    users = ""

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                accounts.id AS account_id,
                users.id AS user_id,
                users.full_name,
                users.email,
                accounts.account_number,
                accounts.balance,
                accounts.status,
                branchs.name AS branch_name,
                branchs.ifsc,
                user_cif.cif
            FROM accounts
            JOIN users ON users.id = accounts.user_id
            JOIN branchs ON branchs.id = accounts.branch_id
            JOIN user_cif ON user_cif.id = accounts.cif_id
            ORDER BY users.id DESC
        """)

        users = cursor.fetchall()

    except Exception as e:

        connection.rollback()
        print("Error: ", e)
        flash(
            "User data Fetch Problem.",
            "error"
        )

        return redirect(url_for('admin_dashboard'))

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "admin/customer-list.html",
        users=users
    )





# =========================================================
# ADMIN BLOCK / UNBLOCK
# =========================================================

@app.route("/admin/account/<int:account_id>/toggle", methods=["POST"])
def toggle_account(account_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT status
            FROM accounts
            WHERE id = %s
        """,
            (account_id,),
        )

        account = cursor.fetchone()

        if account:

            new_status = "blocked" if account["status"] == "active" else "active"

            cursor.execute(
                """
                UPDATE accounts
                SET status = %s
                WHERE id = %s
            """,
                (new_status, account_id),
            )

            connection.commit()
    except Exception as e:

        connection.rollback()

        print("Error: ", e)

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("admin_customer_list"))







# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_id", None)
    session.pop("admin_username", None)

    return redirect(url_for("admin_login"))









# =========================================================
# ADMIN ADD NEW BRANCH
# =========================================================

@app.route("/admin/branch/add", methods=["GET", "POST"])
def admin_add_branch():

    # Admin authentication
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        ifsc = request.form.get("ifsc", "").strip().upper()
        address = request.form.get("address", "").strip()
        email = request.form.get("email", "").strip().lower()

        # Basic validation
        if not name:
            flash("Branch name is required.", "danger")
            return redirect(url_for("admin_add_branch"))

        if not ifsc:
            flash("IFSC code is required.", "danger")
            return redirect(url_for("admin_add_branch"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check duplicate IFSC
            cursor.execute(
                """
                SELECT id
                FROM branchs
                WHERE ifsc = %s
                """,
                (ifsc,)
            )

            existing_branch = cursor.fetchone()

            if existing_branch:
                flash("This IFSC code already exists.", "error")
                return redirect(url_for("admin_add_branch"))

            # Insert branch
            cursor.execute(
                """
                INSERT INTO branchs
                (
                    name,
                    email,
                    ifsc,
                    address,
                    status
                )
                VALUES(%s, %s, %s, %s, 'Active')
                """,(
                    name,
                    email,
                    ifsc,
                    address,
                )
            )

            connection.commit()

            flash("New branch added successfully.", "success")

            return redirect(url_for("admin_branch_list"))

        except Exception as error:

            if connection:
                connection.rollback()

            print("Database error:", error)

            flash("Unable to add branch.", "error")

            return redirect(url_for("admin_add_branch"))

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("admin/add-branch.html")






# =========================================================
# ADMIN SHOW BRANCH LIST
# =========================================================

@app.route("/admin/branchs")
def admin_branch_list():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                name,
                ifsc,
                address,
                email,
                status,
                created_at
            FROM branchs
            ORDER BY id ASC
            """
        )

        branches = cursor.fetchall()

        return render_template(
            "admin/branch-list.html",
            branches=branches
        )

    except Exception as error:

        print("Database error:", error)

        flash("Unable to load branches.", "error")

        return redirect(url_for("admin_dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()






# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5000)
