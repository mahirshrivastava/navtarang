
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextAreaField,DateField,SubmitField, FileField,validators, BooleanField, ValidationError
from wtforms.validators import EqualTo, Email, DataRequired, Length
from navtarang.models import Product, User
from flask_login import current_user

class RegisterUser(FlaskForm):
    def validate_username(self, user_to_check):
        if User.query.filter_by(username=user_to_check.data).first():
            raise ValidationError("Username Already Exist!")
    
    def validate_email(self, user_to_check):
        if  User.query.filter_by(email_address=user_to_check.data).first():
           raise ValidationError("Email Address Already Exist!")
    
    def validate_contact(self, user_to_check):
        for char in user_to_check.data:
            if not (char >= '0' and char <= '9'):
                raise ValidationError("Invalid Contact! Please check")
        if User.query.filter_by(contact = user_to_check.data).first():
            raise ValidationError("Contact already exist!")

    username = StringField(label='Username: ', validators=[Length(min=10, max=10), DataRequired(message="Enter Username")])
    password = PasswordField(label='Password: ', validators=[Length(min=8, max=15), DataRequired(message="Enter password")])
    confirm_password = PasswordField(label='Confirm Password: ', validators=[Length(min=8, max=15), EqualTo('password', message="Password Not Matched!"), DataRequired(message="Enter Password to Confirm")])
    email = StringField(label='Email Address: ', validators=[Length(max=50), Email(message="Enter correct Email address!"), DataRequired("Enter Email address!")])
    first_name = StringField(label='First Name: ', validators=[Length(max=30), DataRequired(message="Enter First Name! ")])
    last_name = StringField(label='Last Name: ', validators=[Length(max=30), DataRequired(message="Enter Last Name! ")])
    contact = StringField(label='Contact Number: ', validators=[Length(max=10, min=10, message='Contact Number should be of 10 Digit'), DataRequired(message="Enter the Contact number!")])
    admin = BooleanField(label='Admin Access: ')
    submit = SubmitField(label='Create Account')

class LoginUser(FlaskForm):
    def validate_username(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()
        if not user:
            raise Exception("Invalid Username!")

    username = StringField(label='Username: ', validators=[Length(min=10,max=10), DataRequired()])
    password = PasswordField(label='Password: ', validators=[Length(min=8, max=15), DataRequired()])
    submit = SubmitField(label='Login')

class BookingForm(FlaskForm):
    customer_name = StringField(label='Customer Name: ')
    event_date = DateField(label='Event Date: ', validators=[DataRequired(message="Please fill the Event Date!")])
    contact_detail = StringField(label='Contact Details: ')
    alternate_contact =StringField(label='Alternate Contact (optional): ')
    requirements = StringField(label='Requirements: ', validators=[DataRequired(message="Fill the up requirement!")])
    address = TextAreaField(label="Address: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class PackageForm(FlaskForm):
    package_code = IntegerField(label="Package Code: ", validators=[Length(max=5, message="Package Code should be less than 6000 "), DataRequired()])
    package_name = StringField(label="Package Name: ", validators=[Length(min=3, max=50, message="Package Name should be between 3 to 50 words!"), DataRequired()])
    price = IntegerField(label="Package Price: ", validators=[Length(min=3, message="Price should be between 100 to 100000!")])
    description = TextAreaField(label="Description: ", validators=[Length(min=10, max=1024, message="Description should be between 10 to 1024 words!")])
    package_image = FileField(label="Package Image: ", validators=[DataRequired(message="Package image is required!")])
    submit = SubmitField(label="Submit")

class UpdatePackageForm(FlaskForm):
    package_code = IntegerField(label="Package Code: ", validators=[Length(max=5, message="Package Code should be less than 6000 ")])
    package_name = StringField(label="Package Name: ", validators=[Length(min=3, max=50, message="Package Name should be between 3 to 50 words!")])
    price = IntegerField(label="Package Price: ", validators=[Length(min=3, message="Price should be between 100 to 100000!")])
    description = TextAreaField(label="Description: ", validators=[Length(min=10, max=1024, message="Description should be between 10 to 1024 words!")])
    package_image = FileField(label="Package Image: ")
    submit = SubmitField(label="Submit")

class RefreshPage(FlaskForm):
    def validate_confirm_password(self, password_to_check):
        user = User.query.filter_by(username = current_user.username).first()
        if not user:
            raise Exception("Invalid User!")
        if not user.check_password(password_to_check.data):
            raise Exception("Invalid Password")
    confirm_password = PasswordField(label='Confirm Password: ', validators=[Length(min=8, max=15), DataRequired(message="Enter Password to Confirm")])
    submit = StringField(label='Confirm')

class ServiceForm(FlaskForm):
    def validate_service_name(self, user_to_check):
        if Product.query.filter_by(product_name=user_to_check.data).first():
            raise Exception("Service Name Already Exist!")
    service_name = StringField(label="Service Name: ", validators=[Length(min=3, max=50, message="Product Name should be between 3 to 50 words!"), DataRequired()])
    submit = SubmitField(label="Submit")

class ChangePassword(FlaskForm):
    def validate_password(self, value_to_check):
        oldPassword = User.query.filter_by(username = current_user.username).first()
        if not oldPassword.check_password(value_to_check.data):
            raise ValidationError("Invalid Old Password!")

    password = PasswordField(label='Current Password: ', validators=[Length(min=8, max=15), DataRequired()])
    newPassword = PasswordField(label='New Password: ', validators=[Length(min=8, max=15), DataRequired()])
    confirmPassword = PasswordField(label='Confirm Password: ', validators=[Length(min=8, max=15), EqualTo("newPassword", message="Password not matched with new password!"), DataRequired()])
    submit = SubmitField(label="Submit")

class ConfirmOtp(FlaskForm):
    confirmOtp = IntegerField(label='Enter OTP: ', validators=[Length(min=6, max=6), DataRequired()])
    submit = SubmitField(label="Submit")
