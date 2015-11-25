# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_login import login_required

from mytrade.utils import (
    render,
    #_,
)

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")

@blueprint.route("/")
@login_required
def members():
    return render("users/members.html")
