from app.main import bp
from flask import render_template, flash, url_for, redirect, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import User, Habit, HabitHistory
from app.main.forms import NewHabitForm, HabitSettings
from sqlalchemy import desc
from datetime import datetime, date, timedelta


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    user = current_user
    habits = Habit.query.filter_by(user_id=current_user.id)

    return render_template("index.html", title="Home", user=user, habits=habits)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("user.html", user=user)


@bp.route("/new_habit", methods=["GET", "POST"])
@login_required
def new_habit():
    user = current_user
    form = NewHabitForm()
    if form.validate_on_submit():
        habit = Habit(
            habit=form.habit.data,
            creator=current_user,
            weekly_goal=form.weekly_goal.data,
        )
        db.session.add(habit)
        db.session.commit()
        flash("Your habit is saved.")
        return redirect(url_for("main.index"))

    return render_template("new_habit.html", title="New Habit", user=user, form=form)


@bp.route("/<username>/<id>", methods=["GET", "POST"])
@login_required
def habit(username, id):
    habit = Habit.query.filter_by(id=id).first_or_404()
    habit_history = HabitHistory.query.filter_by(habit_id=id)
    form = HabitSettings(habit.habit)
    if form.validate_on_submit():
        habit.habit = form.habit.data
        habit.weekly_goal = form.weekly_goal.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.index"))
    elif request.method == "GET":
        form.habit.data = habit.habit
        form.weekly_goal.data = habit.weekly_goal

    return render_template(
        "habit.html", title="Habit", habit=habit, form=form, habit_history=habit_history
    )


@login_required
@bp.route("/_complete", methods=["GET", "POST"])
def complete():
    id = request.form["id"]
    timestamp = request.form["timestamp"]
    timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
    weekly_count = int(request.form["weekly_count"])
    habit = Habit.query.filter_by(id=id).first_or_404()
    habit_history = HabitHistory.query.filter_by(habit_id=id)

    Habit.complete_habit(habit, current_user, timestamp)
    weekly_count = habit.increase_streak(weekly_count)
    db.session.commit()

    return jsonify(
        current_streak=habit.current_streak,
        longest_streak=habit.longest_streak,
        weekly_count=weekly_count,
    )


@login_required
@bp.route("/_undo", methods=["GET", "POST"])
def undo():
    id = request.form["id"]
    timestamp = request.form["timestamp"]
    timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
    weekly_count = int(request.form["weekly_count"])
    habit = Habit.query.filter_by(id=id).first_or_404()
    habit_history = HabitHistory.query.filter_by(habit_id=id, timestamp=timestamp).first()
    db.session.delete(habit_history)
    weekly_count = habit.decrease_streak(weekly_count)

    habit.active_today = True
    db.session.commit()

    return jsonify(
        current_streak=habit.current_streak,
        longest_streak=habit.longest_streak,
        weekly_count=weekly_count,
    )


@login_required
@bp.route("/_check_status", methods=["GET", "POST"])
def check_status():
    # TODO: Add user setting for start date to be sent in json package
    json = {}
    max_past = datetime.today() - timedelta(days=8)
    if current_user.is_anonymous:
        pass
    habits = Habit.query.filter_by(user_id=current_user.id)
    habit_list = [habit.id for habit in habits]
    json.update({"habit_list": habit_list})
    for habit in habits:
        habit_history = (
            HabitHistory.query.filter_by(habit_id=habit.id)
            .order_by(desc(HabitHistory.timestamp))
            .limit(7)
        )
        history = [status.timestamp.isoformat() for status in habit_history if status.timestamp > max_past]
        if len(history) > 0:
            json.update({str(habit.id): history})
    return jsonify(json)


@login_required
@bp.route("/_reset_current_streak", methods=["GET", "POST"])
def reset_current_streak():
    id = request.form["id"]
    habit = Habit.query.filter_by(id=id).first_or_404()
    habit.reset_current_streak()
    return ""
