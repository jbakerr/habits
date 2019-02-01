from app.main import bp
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import User





@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Welcome')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template('user.html', user=user)

