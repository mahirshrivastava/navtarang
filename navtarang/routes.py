
import os
from flask import render_template, redirect, url_for, request
from flask_login import confirm_login, current_user, login_required, login_user, logout_user
from navtarang import app, db, mail
from flask import flash, session
from navtarang.models import Product, User, Booking, Package
from navtarang.forms import ChangePassword, RegisterUser, LoginUser, BookingForm, PackageForm, RefreshPage, ServiceForm, UpdatePackageForm
from datetime import timedelta
from flask_mail import Message
from navtarang import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

class Routes:
    @app.route('/')
    @app.route('/home')
    def home_page():
        try:
            admin = False
            packages = Package.query.all()
            if current_user.is_authenticated:
                if current_user.admin_access==True:
                    admin = True
            return render_template('home.html',admin=admin, packages=packages)
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for('home_page'))

    @app.route('/booking/<string:username>', methods=['GET','POST'])
    @login_required
    def booking_page(username):
        try:
            if username != current_user.username:
                    raise Exception(f"username {username} does not exist! in current login!", category="danger")
            admin = False
            if current_user.admin_access==True:
                admin = True
            bookingForm = BookingForm()
            productmodel = Product.query.all()
            if request.method == 'GET':
                return render_template('booking.html', booking=bookingForm, model=productmodel, admin=admin)

            if request.method == 'POST':
                if bookingForm.validate_on_submit:
                    requirements = request.form.get('requirements')
                    event_date = str(bookingForm.event_date.data)
                    anotherContact = "Not Provided"
                    if bookingForm.alternate_contact.data:
                        anotherContact = bookingForm.alternate_contact.data
                    customer_name = f"{current_user.first_name} {current_user.last_name}"
                    booking = Booking(
                                    customer_name = customer_name,
                                    dateOfEvent = event_date,
                                    contact_detail = current_user.contact,
                                    alternate_contact = anotherContact,
                                    requirements = requirements,
                                    address = bookingForm.address.data
                                    )
                    db.session.add(booking)
                    db.session.commit()
                    flash(f"Thank You Dear '{current_user.first_name}' We will contact you soon!", category="success")

                if bookingForm.errors != {}:
                    displayErrors(bookingForm.errors)
            return redirect(url_for('booking_page', username=username))
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for('home_page', **username))

    @app.route('/product/<string:username>', methods=['GET','POST'])
    def product_page(username):
        try:
            if current_user.is_authenticated:
                if username != current_user.username:
                        raise Exception("username {username} does not exist in current login!")
            packages = Package.query.all()
            if request.method == 'GET':
                return render_template('product.html', packages=packages)
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for('home_page', username=username))

    @app.route('/register', methods=['GET','POST'])
    def register_page():
        try:
            if not current_user.is_authenticated or current_user.admin_access==True:
                form = RegisterUser()
                if request.method == 'GET':
                    admin = False
                    if current_user.is_authenticated:
                        if current_user.admin_access==True:
                            admin = True
                    return render_template('register.html', register=form,admin=admin)
                if request.method == 'POST':
                    if form.validate_on_submit():
                        email = (form.email.data).lower()
                        admin = False
                        if request.form.get('admin') == 'True':
                            admin = True
                        user = User(
                                    username = form.username.data,
                                    password = form.password.data,
                                    email_address = email,
                                    first_name = form.first_name.data,
                                    last_name = form.last_name.data,
                                    contact = form.contact.data,
                                    admin_access = admin 
                                    )
                        db.session.add(user)
                        db.session.commit()
                        if not current_user.is_authenticated:
                            login_user(user)
                        flash(f"Account Created Successfully!", category='success')
                        return redirect(url_for("home_page", username=current_user.username))
                    if form.errors != {}:
                        displayErrors(form.errors)
                        return redirect(url_for("register_page"))
        except Exception as error:
            flash(f"{error}", category='danger')
            return redirect(url_for('home_page'))

    @app.route('/login', methods = ['GET', 'POST'])
    def login_page():
        try:
            if current_user.is_authenticated:
                raise Exception("User Already Logged In!")
            form = LoginUser()
            if request.method == 'GET':
                return render_template('login.html', login=form)
            if request.method == 'POST':
                if form.validate_on_submit():
                    user = User.query.filter_by(username=form.username.data).first()
                    if user.check_password(form.password.data):
                        remember = False
                        for value in request.form.getlist('remember'):
                            if value == 'True':
                                remember = True
                        login_user(user, remember=remember)
                        session.permanent = True
                        flash(f" Logged in Successfully!", category='success') 
                        return redirect(url_for('home_page'))    
                    flash(f"Invalid Password!", category='danger')
                    return redirect(url_for("login_page"))
            if form.errors != {}:
                displayErrors(form.errors)
                return redirect(url_for("login_page"))
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for("home_page"))

    @app.route('/logout/<string:username>', methods=['GET','POST'])
    @login_required
    def logout_page(username):
        admin = False
        logout_user()
        flash("Logged Out!", category='info')
        return redirect(url_for('home_page', admin=admin))

    @app.route('/about/<string:username>', methods=['GET','POST'])
    def about_page(username):
        try:
            if request.method == 'GET':
                return render_template('about.html')
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for("home_page", username=username))

    @app.route('/profile/<string:username>', methods=['GET','POST'])
    @login_required
    def profile_page(username):
        try:
            if username != current_user.username:
                raise Exception(f"username {username} does not exist! in current login!")
            user = User.query.all()
            if request.method == 'GET':
                return render_template('profile.html', username=username, user=user)
        except Exception as error:  
            flash(error, category="danger")
            return redirect(url_for('home_page', username=username))
    
    @app.route('/<string:username>/profile/<string:admin>')
    @login_required
    def delete_profile(username, admin):
        try:
            if admin == "True":
                if current_user.is_authenticated:
                    user = User.query.filter_by(username=username).first()
                    db.session.delete(user)
                    db.session.commit()
                    flash(f"{username} deleted successfully!", category='success')
                    return redirect(url_for('profile_page', username=username))
            raise Exception("User is not an admin!")
        except Exception as error:
            flash(error, category='danger')
            return redirect(url_for('profile_page', username=username))

    @app.route('/changePassword/<string:username>', methods=['GET','POST'])
    @login_required
    def changePassword(username):
        try: 
            if username != current_user.username:
                raise Exception(f"username {username} does not exist! in current login!")
            change_password = ChangePassword()
            user = User.query.filter_by(username=username).first()
            if request.method == 'GET':
                return render_template('changePassword.html', username=username, changePassword=change_password)
            if request.method == 'POST':
                if change_password.validate_on_submit():
                    if change_password.newPassword.data == change_password.password.data:
                        flash(f"New Password can't be same as current password", category="danger")
                        return redirect(url_for('changePassword', username=username))
                    user.password = change_password.newPassword.data
                    db.session.commit()
                    flash(f"{username}'s password changed successfully! ", category='success')
                    return redirect(url_for('home_page', username=username))
                    else:
                        flash(f"Invalid Old Password!", category="danger")
                        return redirect(url_for('changePassword', username=username))
            if change_password.errors != {}:
                displayErrors(change_password.errors)
                return redirect(url_for('changePassword', username=username))                  
        except Exception as error:
            flash(f"{error}", category="danger")
            return redirect(url_for('home_page', username=username))

    @app.route('/refresh/<string:username>', methods=['GET','POST'])
    @login_required
    def refresh_page(username):
        if username != current_user.username:
                flash(f"username {username} does not exist! in current login!", category="danger")
                username = current_user.username
                return redirect(url_for('home_page', username=username))
        refresh = RefreshPage()
        if request.method== 'GET':
            return render_template('refresh.html', refresh=refresh)
        elif request.method== 'POST':
            if current_user.check_password(refresh.confirm_password.data):
                confirm_login()
                redirect(url_for('user_profile'))

    def check_filename(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

    @app.route('/admin/<string:username>', methods=['GET','POST'])
    @login_required
    def admin_page(username):
        try:
            if username != current_user.username:
                flash(f"username {username} does not exist! in current login!", category="danger")
                username = current_user.username
                return redirect(url_for('home_page', username=username))
            packageForm = PackageForm()
            serviceForm = ServiceForm()
            serviceList = Product.query.all()
            packageList = Package.query.all()
            if request.method=='GET':
                return render_template('admin.html', packageList=packageList, package=packageForm, service=serviceForm, serviceList=serviceList)
            if request.method=='POST':
                if packageForm.validate_on_submit:
                    # check file option
                    if not packageForm.package_image.data:
                        flash(f"no file part!", category='danger')
                        return redirect(url_for('admin_page', username=username))
                    # check file name
                    file = packageForm.package_image.data
                    if file.filename == "":
                        flash(f"No selected file", category='danger')
                        return redirect(url_for('admin_page', username=username))
                    if file and Routes.check_filename(file.filename):
                        packageFile = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOADS_IMAGE'], packageFile))
                        filePath = f"uploads/{packageFile}"
                    package = Package(
                                    package_code = packageForm.package_code.data,
                                    package_name = packageForm.package_name.data,
                                    price = packageForm.price.data,
                                    filename = filePath,
                                    description = packageForm.description.data
                                    )
                    db.session.add(package)
                    db.session.commit()
                    flash(f"Package {packageForm.package_name.data} has been added to the list!", category="success")
                    return redirect(url_for('admin_page', username=username))
                if not Product.query.filter_by(product_name=serviceForm.service_name.data).first():
                    service = Product(
                        product_name = serviceForm.service_name.data
                    )
                    db.session.add(service)
                    db.session.commit()
                    flash(f"Service {serviceForm.service_name.data} has been added to the list", category='success')
                    return redirect(url_for('admin_page', username=username))
                else:
                    raise Exception("Service already Exists!")
        except Exception as e:
            flash(f"{e}", category='danger')
            return redirect(url_for('admin_page', username=username))

    @app.route('/mail/<string:username>')
    @login_required
    def mail_page():
        if username != current_user.username:
                flash(f"username {username} does not exist! in current login!", category="danger")
                username = current_user.username
                return redirect(url_for('home_page', username=username))
        msg = Message("Hello")
        msg.add_recipient("shrivastavamahir06@gmail.com")
        msg.body="This is email body"
        mail.send(msg)
        flash(f"Mail has been sent to the user.", category="success")
        return redirect(url_for('home_page'))

    @app.route('/admin/<string:username>/updatePackage/<int:package_code>', methods=['GET','POST'])
    @login_required
    def update_package(username, package_code):
        try:
            if current_user.admin_access == True:
                package = Package.query.filter_by(package_code=package_code).first()
                if not package:
                    flash(f"Package not in the list! check the package code!", category="danger")
                    return redirect(url_for("admin_page", username=current_user.username))
                packageForm = UpdatePackageForm()
                if request.method == 'POST':
                    if packageForm.validate_on_submit:
                        counter = 0
                        flashs = []
                        if not request.form.getlist('same_name'):
                            package.package_name = packageForm.package_name.data
                            counter += 1
                            flashs.append("Package Name has been updated in the list!")
                        if not request.form.getlist('same_price'):
                            package.price = packageForm.price.data
                            counter += 1
                            flashs.append("Package Price has been updated in the list!")
                        if not request.form.getlist('same_image'):
                            filePath = f"./navtarang/static/{package.filename}"
                            os.remove(filePath)
                            if packageForm.package_code.data:
                                # check file option
                                if not packageForm.package_image.data:
                                    flash(f"no file part!", category='danger')
                                    return redirect(url_for('admin_page', username=username))
                                # check file name
                                file = packageForm.package_image.data
                                if file.filename == "":
                                    flash(f"No selected file", category='danger')
                                    return redirect(url_for('admin_page', username=username))
                                if file and Routes.check_filename(file.filename):
                                    packageFile = secure_filename(file.filename)
                                    file.save(os.path.join(app.config['UPLOADS_IMAGE'], packageFile))
                                    package.filename = packageFile
                                    counter += 1
                            flashs.append("Package Image has been updated in the list!")
                        if not request.form.getlist('same_description'):
                            package.description = packageForm.description.data
                            counter += 1
                            flashs.append("Package Description has been updated in the list!")
                        
                        if counter > 0:
                            db.session.commit()
                            for msg in flashs:
                                flash(msg, category='success')
                            return redirect(url_for('admin_page', username=username))
                        else:
                            flash('No Changes in package list!', category="danger")
                            return redirect(url_for('admin_page', username=username))

                elif request.method == 'GET':
                    if package:
                        return render_template('packageUpdate.html', package=package, packageForm = packageForm)
            else:
                raise Exception("You are not allowed to visit this page")
        except Exception as error:
            flash(f"{error}", category='danger')
            return redirect(url_for('home_page'))

    @app.route('/admin/<string:username>/deletePackage/<int:package_code>')
    @login_required
    def delete_package(username, package_code):
        try:
            if username == current_user.username:
                if current_user.admin_access == True:
                    package = Package.query.filter_by(package_code=package_code).first()
                    if package:
                        db.session.delete(package)
                        db.session.commit()
                        filePath = f"./navtarang/static/{package.filename}"
                        os.remove(filePath)
                        flash("Package deleted, Package list is updated!", category='success')
                        return redirect(url_for('admin_page', username=current_user.username))
            else:
                raise Exception("This is not the right url to go through this process!")
        except Exception as error:
            flash(f"{error}", category='danger')
            return redirect(url_for('home_page'))

    @app.route('/admin/<string:username>/updateService/<string:service_name>', methods=['GET','POST'])
    @login_required
    def update_service(username, service_name):
        try:
            if username == current_user.username:
                if current_user.admin_access == True:
                    service = Product.query.filter_by(product_name=service_name).first()
                    serviceForm = ServiceForm()
                    if request.method=='GET':
                        if service:
                            return render_template('productUpdation.html', service=service,serviceForm=serviceForm)
                        else:
                            raise Exception("Service name doesn't exist!")
                    elif request.method == 'POST':
                        if Product.query.filter_by(product_name=serviceForm.service_name.data):
                            service.product_name = serviceForm.service_name.data
                            db.session.commit()
                            flash("Service Updated in the list!", category='success')
                            return redirect(url_for('admin_page', username=current_user.username))
                        else:
                            flash("Product already Exist!", category="danger")
                            return redirect(url_for('update_service', username=username, service_name=service.product_name))
                else:
                    raise Exception("Username not allowed!")        
            else:
                raise Exception("Username not allowed!")
        except Exception as error:
            flash(f"{error}", category='danger')
            return redirect(url_for('home_page'))
        
    @app.route('/admin/<string:username>/deleteService/<string:service_name>')
    @login_required
    def delete_service(username, service_name):
        try: 
            if username == current_user.username:
                if current_user.admin_access == True:
                    service = Product.query.filter_by(product_name=service_name).first()
                    if service:
                        db.session.delete(service)
                        db.session.commit()
                        flash(f"Service {service_name} Deleted successfully! List Updated", category='success')
                        return redirect(url_for('admin_page', username=username))
                    else:
                        raise Exception("Service does not exist!")
                else:
                    raise Exception("Username is not allowed to perform this method!")
            else:
                raise Exception("Username is invalid! invalid attempt!")
        except Exception as error:
            flash(f"{error}", category='danger')
            return redirect(url_for('home_page'))

    @app.route('/<string:username>/dj')
    def dj_page(username):
        return redirect(url_for("product_page", username=username))

    @app.route('/<string:username>/orchestra')
    def orchestra_page(username):
        return redirect(url_for("product_page", username=username))

    @app.route('/<string:username>/langa')
    def langa_page(username):
        return redirect(url_for("product_page", username=username))

    @app.route('/<string:username>/retro')
    def retro_page(username):
        return redirect(url_for("product_page", username=username))
    
    @app.errorhandler(404)
    def handle_bad_request(e):
        username = "?"
        if current_user.is_authenticated:
            username = current_user.username
        flash(f"{e}", category='danger')
        return redirect(url_for('home_page', username=username))

    @app.route('/bookingList/<string:username>', methods=['GET'])
    @login_required
    def bookingList(username):
        try:
            if not current_user.admin_access == True:
                raise Exception("User is not an admin!")
            if username != current_user.username:
                raise Exception("Username is not valid!")
            bookingList = Booking.query.all()    
            if request.method == 'GET':
                return render_template('bookinglist.html', username=username, bookingList=bookingList)
            
        except Exception as error:
            flash(f"{error}")
            return redirect(url_for('bookingList', username=username))
    
def displayErrors(errors):
        for error in errors.values():
            flash(f"{error[0]}", category="danger")
