from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Referral
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user
import string
import random

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "":
            flash("Enter email", category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash("Incorrect password", category='error')
            else:
                flash("Email not registered", category='error')

    return render_template('login.html', user=current_user)


def generate_referral_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(7))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        referralCode = request.form.get('referralcode')
        ownReferralCode = generate_referral_code()

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email is already registered, try logging in", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 8:
            flash("Password must be greater than 7 characters", category="error")
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'), referralCode=ownReferralCode)

            if referralCode:
                referrer = User.query.filter_by(referralCode=referralCode).first()
                if referrer:
                    referral = Referral(referrer_email=referrer.email, referred_email=new_user.email)
                    db.session.add(referral)

            db.session.add(new_user)
            db.session.commit()
            flash("Sign up success!", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))