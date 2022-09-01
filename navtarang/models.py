from datetime import datetime
from navtarang import db
from flask_login import UserMixin
from navtarang import bcrypt, login_manager

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(length=10), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30),  nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    contact = db.Column(db.String(length=10), unique=True, nullable=False)
    budget = db.Column(db.Integer, default=0)
    admin_access = db.Column(db.Boolean, default=False)
    booking = db.relationship('Booking', backref='owned_user', lazy=True)

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def check_email(self, attempted_email):
        return self.email_address.lower() == attempted_email.lower()

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password_text):
        self.password_hash = bcrypt.generate_password_hash(password_text).decode('utf-8')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(length=50), nullable=False)
    event_date = db.Column(db.Date, nullable = False)
    contact_detail = db.Column(db.String, nullable = False)
    alternate_contact = db.Column(db.String)
    requirements = db.Column(db.String, nullable = False)
    address = db.Column(db.String,nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    
    @property
    def dateOfEvent(self):
        return self.dateOfEvent
    
    @dateOfEvent.setter
    def dateOfEvent(self, date):
        dates = datetime.strptime(date, "%Y-%m-%d")
        self.event_date = dates.date()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(length=50), nullable=False, unique=True)
    package = db.relationship('Package', backref='package_owned', lazy=True)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_code = db.Column(db.Integer(), nullable=False, unique=True)
    package_name = db.Column(db.String(length=50), nullable = False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Integer, nullable = False)
    product = db.Column(db.ForeignKey(Product.id))    