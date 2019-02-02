from app.main import bp
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import User, Habbit
from app.main.forms import NewHabbitForm



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    habbits = Habbit.query.filter_by(user_id = current_user.id)
    return render_template('index.html', title='Home', user=user, habbits=habbits)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@bp.route('/new_habbit', methods=['GET', 'POST'])
@login_required
def new_habbit():
    user = current_user
    form = NewHabbitForm()
    if form.validate_on_submit():
        habbit = Habbit(habbit=form.habbit.data, creator=current_user)
        db.session.add(habbit)
        db.session.commit()
        flash("Your habbit is saved.")
        return redirect(url_for('main.index'))

    return render_template('new_habbit.html', title='NewHabbit', user=user,
        form=form)
