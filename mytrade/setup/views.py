# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
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
from mytrade.utils import (
    render,
    _,
)
from mytrade.extensions import (
    db
)

blueprint = Blueprint("setup", __name__, url_prefix='/setup',
                      static_folder="../static",
                      template_folder="../templates/setup")

@blueprint.route("/")
@login_required
def setup():
    return render("user/members.html")

@blueprint.route('/units', methods=['GET'])
@login_required
def units():
    """Unit Query"""
    return_url = request.args.get('next', url_for(".units"))

    units = Unit.query.all()
    return render('units.html', units=units, return_url=return_url)

@blueprint.route('/unit_add', methods=['POST', 'GET'])
@login_required
def unit_add():
    """Unit Add"""
    return_url = request.args.get('next', url_for(".units"))
    unit = Unit('')
    unitform = UnitForm(next=return_url)
    if unitform.validate_on_submit():
        try:
            unitform.populate_obj(unit)
            db.session.add(unit)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.unit_add', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model. %(error)s',  error=str(ex    )), 'danger')

    return render('unit_add.html', unitform=unitform,
        return_url=return_url)

@blueprint.route('/unit_edit/<unit_id>', methods=['GET', 'POST'])
@login_required
def unit_edit(unit_id):
    """Unit Edit"""
    return_url = request.args.get('next', url_for(".units"))
    #unit = Unit.query.filter_by(id=unit_id).first()
    unit = db.session.query(Unit).get(unit_id)

    if unit is None:
        return redirect(return_url)

    unitform = UnitForm(obj=unit, next=return_url)
    if unitform.validate_on_submit():
        try:
            unitform.populate_obj(unit)
            #unit.commit()
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('unit_edit.html', unitform=unitform,
        return_url=return_url)

@blueprint.route('/unit_delete/<unit_id>', methods=['POST'])
@login_required
def unit_delete(unit_id):
    """Unit Delete"""
    return_url = request.args.get('next', url_for(".units"))
    unit = Unit.query.filter_by(id=unit_id).first()

    if unit:
        unit.delete()
    return redirect(return_url)

