from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Change backref to avoid conflict with 'user' property in Application
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    internship = db.Column(db.String(150), nullable=True)
    skills = db.Column(db.String(300), nullable=True)
    # payment = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    about_internship = db.Column(db.Text)
    certification_courses = db.Column(db.Text)
    who_can_apply = db.Column(db.Text)
    no_of_vacancies = db.Column(db.Integer)
    # about_talentconnect = db.Column(db.Text)

    # Add a new column for the company logo
    company_logo = db.Column(db.String(300), nullable=True)  # Store the logo's file path or URL
    status = db.Column(db.String(50), default='pending')

    # Fix the relationship conflict using back_populates
    applications = db.relationship('Application', back_populates='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.company_name}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    qualification = db.Column(db.String(255), nullable=False)
    year_of_graduation = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.String(255), nullable=False)  # Store resume path or filename
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    # application_id = db.Column(db.Integer, unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')

    # Fix the relationship conflict using back_populates
    company = db.relationship('Company', back_populates='applications', lazy=True)
    
    def __repr__(self):
        return f'<Application {self.name} for {self.company.company_name}>'
    
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)  # User's email address
    plan = db.Column(db.String(50), nullable=False)  # The type of subscription plan (monthly, yearly, etc.)
    expire_date = db.Column(db.DateTime, nullable=False)  # The expiration date of the subscription
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Subscription {self.email} | {self.plan}>"


