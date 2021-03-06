# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, flash, url_for, redirect)
from flask_login import login_user, login_required, logout_user

from mytrade.extensions import login_manager
from mytrade.user.models import User
from mytrade.public.forms import LoginForm
from mytrade.user.forms import RegisterForm
from mytrade.utils import flash_errors
#from mytrade.database import db

from mytrade.utils import (
    render, 
    _,
)

blueprint = Blueprint('public', __name__
                      , static_folder="../static"
                      , template_folder="../templates/public")

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash(_("You are logged in."), 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render("home.html", form=form)

@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(_('You are logged out.'), 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash(_("Thank you for registering. You can now log in."), 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render('register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render("about.html", form=form)
