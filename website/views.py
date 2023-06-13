from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

the_user = ""

def open_web(name):
    global the_user
    the_user = name
    return redirect(url_for('views.home', name=name))


@views.route('/home/<string:name>')
@login_required
def home(name):
    return render_template("chat.html", user=current_user, log_user=name)

@views.route('/')
@login_required
def redirecting():
    if (the_user == ""):
        return redirect(url_for('auth.login'))
    return redirect(url_for('views.home', name=the_user))
