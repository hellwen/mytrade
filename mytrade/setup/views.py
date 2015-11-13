# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
from flask_login import login_required

from .models import (
    Unit,
    #Item_Group,
    #Company,
)
from .forms import (
    UnitForm,
)


setup = Blueprint("setup", __name__, url_prefix='/setup',
                      static_folder="../static")


@setup.route("/")
@login_required
def setup():
    return render_template("user/members.html")

@setup.route('/units', methods=['GET'])
@login_required
def units():
    """Unit Query"""
    units = Unit.query.all()
    return render_template('units.html', units=units)

@setup.route('/unit_add', methods=['POST'])
@login_required
def unit_add():
    """Unit Add"""
    return_url = request.args.get('next', url_for(".units"))
    unitform = UnitForm(Unit)
    if unitform.validate_on_submit():
        if '_add_another' in request.form:
            flash('Created successfully.')
            return redirect(url_for('.unit_add', url=return_url))
        else:
            return redirect(return_url)

    return render_template('unit_add.html', unitform=unitform,
        return_url=return_url)

@setup.route('/unit_edit/<unit_id>', methods=['GET', 'POST'])
@login_required
def unit_edit(unit_id):
    """Unit Edit"""
    return_url = request.args.get('next', url_for(".units"))
    unit = Unit.get_one(unit_id)

    if unit is None:
        return redirect(return_url)

    unitform = UnitForm(unit)
    if unitform.validate_on_submit():
        try:
            unitform.populate_obj(unit)
            unit.commit()
            return True
        except Exception:
            flash('Failed to update model.')
            return False

    return render_template('unit_edit.html', unitform=unitform,
        return_url=return_url)

@setup.route('/unit_delete/<unit_id>', methods=['POST'])
@login_required
def unit_delete(unit_id):
    """Unit Delete"""
    return_url = request.args.get('next', url_for(".units"))
    unit = Unit.get_one(unit_id)

    if unit:
        unit.delete()
    return redirect(return_url)
