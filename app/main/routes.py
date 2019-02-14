from app.main import bp
from flask import render_template, flash, url_for, redirect, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import User, Habbit, HabbitHistory
from app.main.forms import NewHabbitForm, HabbitSettings
from sqlalchemy import desc
from datetime import datetime, date, timedelta


@bp.before_request
def before_request():
    yesterday = date.today() - timedelta(1)
    if current_user.is_anonymous == False:
        habbits = Habbit.query.filter_by(creator=current_user)
        for habbit in habbits:
            habbit_history = HabbitHistory.query.filter_by(
                habbit_id=habbit.id).order_by(
                desc(HabbitHistory.timestamp)).first()
            if habbit_history is not None:
                if habbit_history.timestamp.date() < date.today():
                    habbit.active_today = True
                if habbit_history.timestamp.date() < yesterday:
                    habbit.current_streak = 0

    db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    habbits = Habbit.query.filter_by(user_id = current_user.id)
    return render_template(
        'index.html', title='Home', user=user, habbits=habbits)


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
        habbit = Habbit(
            habbit=form.habbit.data,
             creator=current_user,
              weekly_goal=form.weekly_goal.data)
        db.session.add(habbit)
        db.session.commit()
        flash("Your habbit is saved.")
        return redirect(url_for('main.index'))

    return render_template('new_habbit.html', title='New Habbit', user=user,
        form=form)


@bp.route('/<username>/<id>', methods=['GET', 'POST'])
@login_required
def habbit(username, id):
    habbit = Habbit.query.filter_by(id=id).first_or_404()
    habbit_history = HabbitHistory.query.filter_by(habbit_id=id)
    form = HabbitSettings(habbit.habbit)
    if form.validate_on_submit():
        habbit.habbit = form.habbit.data
        habbit.weekly_goal = form.weekly_goal.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.habbit.data = habbit.habbit
        form.weekly_goal.data = habbit.weekly_goal


    return render_template(
        'habbit.html', title='Habbit', habbit=habbit,
         form=form, habbit_history=habbit_history)


@login_required
@bp.route('/_complete', methods=['GET', 'POST'])
def complete():
    id = request.form['id']
    weekly_count = int(request.form['weekly_count'])
    habbit = Habbit.query.filter_by(id=id).first_or_404()
    habbit_history = HabbitHistory.query.filter_by(habbit_id=id)

    Habbit.complete_habbit(habbit,current_user)
    weekly_count = habbit.increase_streak(weekly_count)
    db.session.commit()


    return jsonify(
        current_streak=habbit.current_streak,
         longest_streak=habbit.longest_streak,
         weekly_count=weekly_count)

@login_required
@bp.route('/_undo', methods=['GET', 'POST'])
def undo():
    id = request.form['id']
    weekly_count = int(request.form['weekly_count'])
    habbit = Habbit.query.filter_by(id=id).first_or_404()
    habbit_history = HabbitHistory.query.filter_by(
        habbit_id=id).order_by(desc(HabbitHistory.timestamp)).first()
    db.session.delete(habbit_history)
    weekly_count = habbit.decrease_streak(weekly_count)

    habbit.active_today = True
    db.session.commit()

    return jsonify(
        current_streak=habbit.current_streak,
        longest_streak=habbit.longest_streak,
        weekly_count=weekly_count)

@login_required
@bp.route('/_check_status', methods=['GET', 'POST'])
def check_status():
    if current_user.is_anonymous:
        pass
    habbits = Habbit.query.filter_by(user_id=current_user.id)
    json = {}
    for habbit in habbits:
        habbit_history = HabbitHistory.query.filter_by(
            habbit_id=habbit.id).order_by(desc(
                HabbitHistory.timestamp)).limit(7)
        history = [status.timestamp.isoformat() for status in habbit_history]
        if len(history) > 0:
            json.update({str(habbit.id): history})
    print(json)

    return jsonify(json)
