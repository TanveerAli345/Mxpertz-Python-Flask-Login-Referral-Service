from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import Referral

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    referred_users = Referral.query.filter_by(referrer_email=current_user.email).all()

    return render_template('home.html', user=current_user, referred_users=referred_users)
