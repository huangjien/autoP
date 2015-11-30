from datetime import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import logout_user, login_required
from User import load_user, User
from autoP import app
from forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html'
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Contact me if you have any questions.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Project Brief.'
    )


@app.route('/listUsers')
def listUsers():
    """Renders the listUsers page."""
    return render_template(
        'listUsers.html',
        title='List Users',
        message='These are the users in our system'
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = load_user(form.email.raw_data)[0]
        if user is None:
            flash('We don\'t know you')
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('home'))
            # if user.verify_password(form.password.raw_data):
            #     login_user(user)
            #     flash('Logged in successfully.')
            #     return redirect(url_for('home'))
            # else:
            #     flash('wrong password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        user.save()
        flash('User is registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)