from flask import render_template, render_template, request, session, url_for,redirect, flash,g
from werkzeug.security import check_password_hash, generate_password_hash
from app.auth import bp
from app.extensions import db
from app.models.auth import login_required, users
import os

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = users.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        elif user.project not in [os.environ.get('type_1'), os.environ.get('type_2')]:
            error = 'Access denied. Invalid project.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html', title="Ingresa")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = users.query.filter_by(id=user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

