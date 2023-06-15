import functools
from flask import render_template, render_template, request, session, url_for, g, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    type = db.Column(db.Text)
    project = db.Column(db.Text)