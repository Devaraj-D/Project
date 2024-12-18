from flask import Flask, render_template, request, send_file,redirect, url_for, flash,session,jsonify
import jwt
from datetime import datetime,timedelta
from datetime import datetime
from config import Config
from models import db, User, Company, Application, Subscription
from flask import send_from_directory, abort
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import json
import stripe
import calendar
import secrets



app = Flask(__name__)
app.config.from_object(Config)
# Generate a random 32-byte secret key
app.secret_key = "3b4cdfeea29bc51ea4279edaec4343d64eb2eb91183474fafd53cddfb2eaf792"
print(app.secret_key)
stripe.api_key = "sk_test_51QVG2DEDpEKIoaMrgZHvdXwgKMnB15MP9Zv17uJcoeDINFjL0yxiZMqIXNiR9e3D80k5ycgpl396NpRdJ9VFyRa8005oV7R2JZ"  # Secret Key
STRIPE_PUBLISHABLE_KEY = "pk_test_51QVG2DEDpEKIoaMrw39uJTGEWkHI4dFETMXApIsfAgE7Ad1MpBS9ctl3HsdS3oRb6EIpLWmuNJqnKraIzSru5I9d00kMiWGm0h"    # Replace with a strong secret key

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

# Secret Key for JWT
JWT_SECRET = 'your_jwt_secret_key'  # Replace with a strong secret key
JWT_ALGORITHM = 'HS256'            # Algorithm for encoding tokens

# Create tables if they don't exist
with app.app_context():
    db.create_all()


# Function to generate JWT tokens
def generate_tokens(user_id):
    current_time = datetime.utcnow()
    
    access_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": current_time + timedelta(minutes=15),  # Access token valid for 15 minutes
            "iat": current_time
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    refresh_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": current_time + timedelta(days=7),  # Refresh token valid for 7 days
            "iat": current_time
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    id_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": current_time + timedelta(hours=1),  # ID token valid for 1 hour
            "iat": current_time
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    return access_token, refresh_token, id_token


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password=request.form.get('confirm_password')

        if password !=confirm_password:
            flash('password and confirm password do not match','danger')
            return redirect(url_for('signup'))

        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different one.', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Add new user to the database
        new_user = User(role=role,username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()
        print(user)
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

        username = user.username
        # Generate tokens
        access_token, refresh_token, id_token = generate_tokens(user.id)

        # Save tokens in session (optional for server-side usage)
        session['access_token'] = access_token
        session['user_id'] = user.id
        session['refresh_token'] = refresh_token
        session['user_email'] = user.email
        session['id_token'] = id_token
        session['username'] = username

        # Check the user's role and redirect accordingly
        if user.role == 'student':
            flash('Login successful! Redirecting to student dashboard.', 'success')
            return redirect(f'http://127.0.0.1:8000/index1?username={username}&role=student')
        elif user.role == 'company':
            
            flash('Login successful! Redirecting to company dashboard.', 'success')
            return redirect(f'http://127.0.0.1:8000/index2?username={username}&role=employer')
        else:
            flash('Invalid role! Please contact support.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    # Check if the user has an access token in the session
    if 'access_token' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    try:
        # Decode access token to validate it
        decoded_token = jwt.decode(session['access_token'], JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = decoded_token.get('user_id')  # Optionally get user_id from token
    except jwt.ExpiredSignatureError:
        flash('Session expired. Please log in again.', 'danger')
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        flash('Invalid session. Please log in again.', 'danger')
        return redirect(url_for('login'))

    # Fetch all company data from the database
    companies = Company.query.filter_by(status='verified').all()
    user_email = session.get('user_email')

    applied_companies = [app.company_id for app in Application.query.filter_by(email=user_email).all()]
    print(applied_companies)

    # role = User.query.get('role')
    # print(role)
    # Render the dashboard with the company data
    subscription = Subscription.query.filter_by(email=user_email,).first()
    # subscription = db.session.query(Subscription, role).join(User, Subscription.id == User.id).all()
    if subscription:
        # Compare expire_date with current date
        current_date = datetime.now()
        if subscription.expire_date > current_date:
            subscription_status = "subscribed"  # If expire_date is later than current date
        else:
            subscription_status = "expired"  # If expire_date is earlier or same as current date
    else:
        subscription_status = "no_subscription"

    return render_template('dashboard.html', companies=companies, applied_companies=applied_companies,
                           subscription_status=subscription_status)


UPLOAD_FOLDER = 'project2/static/assests'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/company_dashboard', methods=['GET', 'POST'])
def company_dashboard():
    print('++++++++++++++++++++++++++++++')
    if 'access_token' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    print('next')

    # Decode the token to get user info (like email or ID)
    user_email = session.get('user_email')
    print(user_email)
    # Fetch the company associated with the logged-in user (based on user_email)
    company = Company.query.filter_by(email=user_email).first()
    print(company)

    if request.method == 'POST':
        # Adding a new job post
        name = request.form['name']
        location = request.form['location']
        
        internship = request.form['internship']
        # skills_json = request.form.get('skills', '[]')
        # print(skills_json)
        #   # Default to an empty JSON array
        # skills = json.loads(skills_json) 

        # skills_str = json.dumps(skills) if skills else '[]'
        skills_json = request.form.get('skills', '[]')
        print("Raw skills JSON:", skills_json)  # Print raw JSON input from the form

        # Convert the JSON string to a Python list
        skills_list = json.loads(skills_json)
        print("Parsed skills list:", skills_list)  # Print parsed list

        # Convert the list to a comma-separated string
        skills_str = ', '.join(skills_list)
        print("Skills string:", skills_str)  # Print final string for debugging
        # payment = int(request.form['payment'])
        duration = request.form['duration']

        about_internship = request.form['about_internship']
        certification_courses = request.form['certification_courses']
        who_can_apply = request.form['who_can_apply']
        no_of_vacancies = int(request.form['no_of_vacancies'])
        # about_talentconnect = request.form['about_talentconnect']

        # Handle file upload for logo
        file = request.files['logo']
        print(f"Uploaded file: {file}")  # Debug print for file object
        print(f"All files in request: {request.files}")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(logo_path)
        else:
            flash('Invalid file type for logo. Please upload a valid image file.', 'danger')
            return redirect(url_for('company_dashboard'))

        new_company = Company(
            company_name=name,
            location=location,
            internship=internship,
            skills=skills_str,
            # payment=payment,
            duration=duration,
            about_internship=about_internship,
            certification_courses=certification_courses,
            who_can_apply=who_can_apply,
            no_of_vacancies=no_of_vacancies,
            # about_talentconnect=about_talentconnect,
            email=user_email,
            company_logo=logo_path  # Save the logo path in the database
        )
        db.session.add(new_company)
        db.session.commit()

        flash('Job post added successfully!', 'success')
        return redirect(url_for('company_dashboard'))

    # if not company:
    #     # No company data found, render the dashboard without data
    #     flash('No company data found. You can add new job posts.', 'info')
    #     return render_template('company_dashboard.html', companies=[], applied_companies=[])
    
    # Fetch the company's internship posts
    companies = Company.query.filter_by(email=user_email, status='verified').all()


    if companies:# For "View Applicants", get a list of applied users for each job post
       applied_companies = Application.query.filter_by(company_id=company.id).all()
    else:
        applied_companies=None
    print('okay')


    subscription = Subscription.query.filter_by(email=user_email).first()
    # role = User.query.get('role')
    # print(role)
    # subscription = db.session.query(Subscription, role).join(User, Subscription.id == User.id).all()

    if subscription:
        # Compare expire_date with current date
        current_date = datetime.now()
        if subscription.expire_date > current_date:
            subscription_status = "subscribed"  # If expire_date is later than current date
        else:
            subscription_status = "expired"  # If expire_date is earlier or same as current date
    else:
        subscription_status = "no_subscription"

    return render_template('company_dashboard.html', companies=companies, applied_companies=applied_companies,subscription_status=subscription_status)




@app.route('/subscribe')
def subscribe():
    return render_template('subscription .html', stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():

    data = request.get_json()
    plan = data.get("plan")

    try:
        if plan == "monthly":
            price_id = "price_monthly_id" 
            amount=1000
        elif plan == "yearly":
            price_id = "price_yearly_id"
            amount=10000
    
        # Create a new Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": "Premium Plan",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.host_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.host_url + "cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

    

# @app.route("/success")
# def success():
#     from flask import session
#     user_email=session.get('user_email')
#     session_id = request.args.get("session_id")  # Retrieve session ID from URL query parameter
#     if not session_id:
#         return "Error: session_id not provided", 400  # Handle error if session_id is missing
#
#     try:
#         # Retrieve the session details using the session_id
#         session = stripe.checkout.Session.retrieve(session_id)
#         customer_email = session.customer_email or session.customer_details.get('email')
#
#         print(user_email,"=========++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
#         # Get the amount total from the session
#         amount_total = session.amount_total  # This is in the smallest currency unit (in paise)
#
#         # Determine the plan based on the amount_total
#         plan = "monthly" if amount_total == 1000 else "yearly" if amount_total == 10000 else None
#         if not plan:
#             return "Error: Invalid amount_total for plan type", 400
#
#         # Initialize expire_date with None or a default value
#         expire_date = None
#
#         # Calculate expiration date based on plan
#         current_date = datetime.now()
#         if plan == "monthly":
#             expire_date = current_date.replace(day=1) + timedelta(days=31)  # Move to next month
#             expire_date = expire_date.replace(day=calendar.monthrange(expire_date.year, expire_date.month)[1])  # Get last day of the month
#         elif plan == "yearly":
#             expire_date = current_date.replace(year=current_date.year + 1)
#
#         # If expire_date is not set, handle invalid plan type
#         if expire_date is None:
#             return "Error: Invalid plan type", 400  # Handle error if plan is not "monthly" or "yearly"
#
#         # Create a new subscription in your database
#         new_subscription = Subscription(email=user_email, plan=plan, expire_date=expire_date)
#         db.session.add(new_subscription)
#         db.session.commit()
#
#         # Redirect to the company dashboard
#         return redirect(url_for('company_dashboard', email=customer_email))
#
#     except stripe.error.StripeError as e:
#         return f"Error retrieving session: {str(e)}", 400
#
#
#
@app.route("/cancel")
def cancel():
    return "Payment canceled!"


@app.route("/success")
def success():
    from flask import session
    user_email = session.get('user_email')
    session_id = request.args.get("session_id")  # Retrieve session ID from URL query parameter

    if not session_id:
        return "Error: session_id not provided", 400  # Handle error if session_id is missing

    try:
        # Retrieve the session details using the session_id
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.customer_email or session.customer_details.get('email')
        # customer_role = session.customer_role or session.customer_details.get('role')

        # Debug print to verify the email
        print(user_email, "==== User Email ===")

        # Get the amount total from the session
        amount_total = session.amount_total  # This is in the smallest currency unit

        # Determine the plan based on the amount_total
        plan = "monthly" if amount_total == 1000 else "yearly" if amount_total == 10000 else None
        if not plan:
            return "Error: Invalid amount_total for plan type", 400

        # Calculate expiration date
        current_date = datetime.now()
        expire_date = None
        if plan == "monthly":
            expire_date = current_date.replace(day=1) + timedelta(days=31)
            expire_date = expire_date.replace(day=calendar.monthrange(expire_date.year, expire_date.month)[1])
        elif plan == "yearly":
            expire_date = current_date.replace(year=current_date.year + 1)

        if expire_date is None:
            return "Error: Invalid plan type", 400

        user_type = get_user_type_by_email(user_email)

        # Create a new subscription in your database
        new_subscription = Subscription(email=user_email, plan=plan, expire_date=expire_date)
        db.session.add(new_subscription)
        db.session.commit()

        # Fetch user type (student/company) from your database or session
         # Custom function to fetch user type

        # Conditional redirection based on user type
        if user_type == "student":
            return redirect(url_for('dashboard', email=customer_email))
        elif user_type == "company":
            return redirect(url_for('company_dashboard', email=customer_email))
        else:
            return "Error: Invalid user type", 400

    except stripe.error.StripeError as e:
        return f"Error retrieving session: {str(e)}", 400

# Example helper function to get user type from the database
def get_user_type_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user.role if user else None




@app.route('/view_applicants/<int:company_id>')
def view_applicants(company_id):
    if 'access_token' not in session:
        flash('Please log in to view applicants.', 'danger')
        return redirect(url_for('login'))

    # Fetch the company
    company = Company.query.get_or_404(company_id)
    print(company)
    print(company_id)

    # Get all applicants for this company’s internship post
    applicants = Application.query.filter_by(company_id=company_id, status='verified').all()
    print(applicants)

    return render_template('view_applicants.html', company=company, applicants=applicants)


@app.route('/details/<int:company_id>')
def details_page(company_id):
    # Fetch the company details from the database
    company = Company.query.get(company_id)
    if not company:
        flash("Company not found", "error")
        return redirect(url_for('dashboard'))

    # Replace 'user_email' with the logged-in user's email (e.g., from session data)
    user_email = session.get('user_email')
    # Check if the user has applied for this company
    has_applied = Application.query.filter_by(company_id=company_id, email=user_email).first() is not None

    return render_template('details.html', company=company, has_applied=has_applied)

@app.route('/details1/<int:company_id>')
def details_page1(company_id):
    # Fetch the company details from the database
    company = Company.query.get(company_id)
    if not company:
        flash("Company not found", "error")
        return redirect(url_for('admin_dashboard'))

    # Replace 'user_email' with the logged-in user's email (e.g., from session data)
    user_email = session.get('user_email')
    # Check if the user has applied for this company
    # has_applied = Application.query.filter_by(company_id=company_id, email=user_email).first() is not None

    return render_template('details1.html', company=company)





@app.route('/apply/<int:company_id>', methods=['GET', 'POST'])
def apply(company_id):
    if 'access_token' not in session:
        flash('Please log in to apply.', 'danger')
        return redirect(url_for('login'))

    # Get the company based on company_id
    company = Company.query.get_or_404(company_id)

    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        mobile_number= request.form['mobile_number']
        qualification = request.form['qualification']
        year_of_graduation = request.form['year_of_graduation']
        resume = request.files['resume']
        user_ids=session.get("user_id")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",user_ids)

        # Save resume file
        if resume:
            filename = secure_filename(resume.filename)
            resume_path = os.path.join('project2/static/resumes', filename)
            resume.save(resume_path)

        # Create a new application
        new_application = Application(
            name=name,
            email=email,
            user_id=user_ids,
            mobile_number=mobile_number,
            qualification=qualification,
            year_of_graduation=year_of_graduation,
            resume=resume_path,
            company_id=company.id
        )

        # Save to the database
        db.session.add(new_application)
        db.session.commit()

        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    email = session.get('user_email')
    return render_template('apply.html', company=company, email=email)





@app.route('/view_resume/<int:application_id>')
def view_resume(application_id):
    # Fetch the application by ID
    application = Application.query.get(application_id)
    print(f"Application: {application}")

    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('company_dashboard'))

    # Get the resume file path
    resume_path = application.resume
    print(f"Resume path: {resume_path}")

    if not resume_path or not os.path.exists(os.path.abspath(resume_path)):
        flash('Resume file not found.', 'danger')
        return redirect(url_for('company_dashboard'))

    # Serve the file
    try:
        return send_file(os.path.abspath(resume_path), mimetype='application/pdf', as_attachment=False)
    except Exception as e:
        print(f"Error serving file: {e}")
        flash('Error viewing resume.', 'danger')
        return redirect(url_for('company_dashboard'))


@app.route('/post_job', methods=['GET'])
def post_job():
    if 'access_token' not in session:
        flash('Please log in to post a job.', 'danger')
        return redirect(url_for('login'))

    # Simply render the post_job.html page
    return render_template('post_job.html')



@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print('________________________________')

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new User with the default role 'admin'
        new_user = User(role='admin',username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! You are now an admin.', 'success')
            return redirect(url_for('admin_signin'))
        except Exception as e:
            db.session.rollback()
            flash('Error occurred. Please try again.', 'danger')
            print(e)
    
    return render_template('admin_signup.html')

@app.route('/admin_signin', methods=['GET', 'POST'])
def admin_signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_email'] = user.email
            session['user_role'] = user.role  # Store the role in the session
            flash('Signin successful!', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirect to dashboard or admin page
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('admin_signin.html')


def get_all_users():
    return User.query.all()


def get_all_companies():
    return Company.query.all()


def get_pending_requests():
    return Company.query.filter_by(status='pending').all()


def get_approved_requests():
    return Company.query.filter_by(status='verified').all()


def get_rejected_requests():
    return Company.query.filter_by(status='rejected').all()


def approve_company_in_db(company_id):
    company = Company.query.get(company_id)
    if company:
        company.status = 'verified'

        db.session.commit()


def reject_company_in_db(company_id):
    company = Company.query.get(company_id)
    if company:
        company.status = 'rejected'
        db.session.commit()


# @app.route('/admin_dashboard')
# def admin_dashboard():
#     active_section = request.args.get('active_section', 'users')  # Default to 'users'
#     users = get_all_users()  # Fetch users
#     print(users)
#     companies = get_all_companies()  # Fetch companies
#     pending_companies = get_pending_requests()  # Fetch pending requests
#     approved_companies = get_approved_requests()  # Fetch approved companies
#     rejected_companies = get_rejected_requests()
#     print(approved_companies)# Fetch rejected companies
#     return render_template(
#         'admin_dashboard.html',
#         active_section=active_section,
#         users=users,
#         companies=companies,
#         pending_companies=pending_companies,
#         approved_companies=approved_companies,
#         rejected_companies=rejected_companies
#     )

def get_all_applications():
    # Query all application data
    return Application.query.all()


def get_pending_applications():
    # Query applications with status 'pending'
    return Application.query.filter_by(status='pending').all()


def get_approved_applications():
    # Query applications with status 'approved'
    return Application.query.filter_by(status='verified').all()


def get_rejected_applications():
    # Query applications with status 'rejected'
    return Application.query.filter_by(status='rejected').all()


def get_application_by_id(app_id):
    """
    Fetch an application by its ID from the database.

    :param app_id: The ID of the application to fetch.
    :return: The application object if found, otherwise None.
    """
    return Application.query.get(app_id)
@app.route('/approve_application/<int:app_id>', methods=['POST'])
def approve_application(app_id):
    # Logic to approve the application
    application = get_application_by_id(app_id)  # Fetch application
    if application:
        application.status = 'verified'
        db.session.commit()  # Save changes
        return redirect(url_for('admin_dashboard', active_section='nav-pending-apps'))
    return "Application not found", 404

@app.route('/reject_application/<int:app_id>', methods=['POST'])
def reject_application(app_id):
    # Logic to reject the application
    application = get_application_by_id(app_id)  # Fetch application
    if application:
        application.status = 'rejected'
        db.session.commit()  # Save changes
        return redirect(url_for('admin_dashboard', active_section='rejected-apps'))
    return "Application not found", 404


@app.route('/admin_dashboard')
def admin_dashboard():
    active_section = request.args.get('active_section', 'users')  # Default to 'users'

    # Fetch data from the users table
    users = get_all_users()  # Fetch users
    print(users)

    # Fetch data from the companies table
    companies = get_all_companies()  # Fetch companies
    pending_companies = get_pending_requests()  # Fetch pending requests
    approved_companies = get_approved_requests()  # Fetch approved companies
    rejected_companies = get_rejected_requests()  # Fetch rejected companies
    print(approved_companies)

    # Fetch data from the applications table
    applications = get_all_applications()  # Fetch all applications
    pending_applications = get_pending_applications()  # Fetch pending applications
    approved_applications = get_approved_applications()  # Fetch approved applications
    rejected_applications = get_rejected_applications()  # Fetch rejected applications

    print(applications)
    subscribe = Subscription.query.all()
    # Pass all fetched data to the template
    return render_template(
        'admin_dashboard.html',
        active_section=active_section,
        users=users,
        companies=companies,
        pending_companies=pending_companies,
        approved_companies=approved_companies,
        rejected_companies=rejected_companies,
        applications=applications,  # Pass applications data
        pending_applications=pending_applications,  # Pending applications
        approved_applications=approved_applications,  # Approved applications
        rejected_applications=rejected_applications,
        subscription=subscribe# Rejected applications
    )


@app.route('/approve_company/<int:company_id>', methods=['POST'])
def approve_company(company_id):
    # Approve the company logic
    approve_company_in_db(company_id)
    return redirect(url_for('admin_dashboard', active_section='pending_requests'))

@app.route('/reject_company/<int:company_id>', methods=['POST'])
def reject_company(company_id):
    # Reject the company logic
    reject_company_in_db(company_id)
    return redirect(url_for('admin_dashboard', active_section='pending_requests'))

# @app.route('/approve_application/<int:application_id>', methods=['POST'])
# def approve_application(id):
#     # Approve the company logic
#     approve_application_in_db(id)
#     return redirect(url_for('admin_dashboard', active_section='pending_application'))
#
# @app.route('/reject_application/<int:application_id>', methods=['POST'])
# def reject_application(id):
#     # Reject the company logic
#     reject_application_in_db(id)
#     return redirect(url_for('admin_dashboard', active_section='pending_application'))


@app.route('/application_tracking', methods=['GET'])
def application_tracking():
    user_email = session.get('user_email')
    print(user_email) # Fetch the email of the logged-in user
    companies = Company.query.filter_by(email=user_email).all()
    print(companies)  # Fetch companies associated with the email

    return render_template(
        'application_tracking.html',
         companies=companies
    )

@app.route('/view_resumes/<int:application_id>')
def view_resumes(application_id):
    # Fetch the application by ID
    application = Application.query.get(application_id)
    print(f"Application: {application}")

    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Get the resume file path
    resume_path = application.resume
    print(f"Resume path: {resume_path}")

    if not resume_path or not os.path.exists(os.path.abspath(resume_path)):
        flash('Resume file not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Serve the file
    try:
        return send_file(os.path.abspath(resume_path), mimetype='application/pdf', as_attachment=False)
    except Exception as e:
        print(f"Error serving file: {e}")
        flash('Error viewing resume.', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/index')
def index():
    return redirect(f'http://127.0.0.1:8000/index')

@app.route('/intern')
def intern():
    return redirect(f'http://127.0.0.1:8000/intern')

@app.route('/jobs')
def jobs():
    return redirect(f'http://127.0.0.1:8000/intern')

@app.route('/')
def index1():
    return "Welcome! Visit /signup to register."

if __name__ == '__main__':
    app.run(debug=True)
