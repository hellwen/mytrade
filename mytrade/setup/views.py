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
    ItemGroup,
    Company,
)
from .forms import (
    UnitForm,
    ItemGroupForm,
    CompanyForm
)
from mytrade.extensions import (
    db
)
from mytrade.utils import (
    render,
    _,
)

blueprint = Blueprint("setup", __name__, url_prefix='/setup',
                      static_folder="../static",
                      template_folder="../templates/setup")


@blueprint.route('/units', methods=['GET'])
@login_required
def units():
    """Unit Query"""
    return_url = request.args.get('next', url_for(".units"))

    models = Unit.query.all()
    return render('units.html', models=models, return_url=return_url)

@blueprint.route('/unit/create', methods=['POST', 'GET'])
@login_required
def unit_create():
    """Unit Create"""
    return_url = request.args.get('next', url_for(".units"))
    model = Unit('')
    form = UnitForm(next=return_url)
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.unit_create', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model.') + '%(error)s' % {'error':str(ex)}, 'danger')

    return render('unit_create.html', form=form,
        return_url=return_url)

@blueprint.route('/unit/edit/id=<int:id>', methods=['GET', 'POST'])
@login_required
def unit_edit(id):
    """Unit Edit"""
    return_url = request.args.get('next', url_for(".units"))
    model = Unit.query.get(id)

    if model is None:
        return redirect(return_url)

    form = UnitForm(obj=model, next=return_url)
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('unit_edit.html', form=form,
        return_url=return_url)

@blueprint.route('/unit/delete/id=<int:id>', methods=['POST'])
@login_required
def unit_delete(id):
    """Unit Delete"""
    return_url = request.args.get('next', url_for(".units"))
    model = Unit.query.filter_by(id=id).first()

    if model:
        model.delete()
    return redirect(return_url)

@blueprint.route('/item_groups', methods=['GET'])
@login_required
def item_groups():
    """Item Group Query"""
    return_url = request.args.get('next', url_for(".item_groups"))

    models = ItemGroup.query.all()
    return render('item_groups.html', models=models, return_url=return_url)

@blueprint.route('/item_group/create', methods=['POST', 'GET'])
@login_required
def item_group_create():
    """Item Group Create"""
    return_url = request.args.get('next', url_for(".item_groups"))
    model = ItemGroup('')

    form = ItemGroupForm(next=return_url)
    form.parent_id.choices = [(r.id, r.item_group_name) for r in ItemGroup.query.filter_by().order_by('item_group_name')]

    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.item_group_create', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model.') + '%(error)s' % {'error':str(ex)}, 'danger')

    return render('item_group_create.html', form=form,
        return_url=return_url)

@blueprint.route('/item_group/edit/id=<int:id>', methods=['GET', 'POST'])
@login_required
def item_group_edit(id):
    """Item Group Edit"""
    return_url = request.args.get('next', url_for(".item_groups"))
    model = ItemGroup.query.get(id)

    if model is None:
        return redirect(return_url)

    form = ItemGroupForm(obj=model, next=return_url)
    form.parent_id.choices = [(r.id, r.item_group_name) for r in ItemGroup.query.filter_by().order_by('item_group_name')]

    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('item_group_edit.html', form=form,
        return_url=return_url)

@blueprint.route('/item_group/delete/id=<int:id>', methods=['POST'])
@login_required
def item_group_delete(id):
    """Item Group Delete"""
    return_url = request.args.get('next', url_for(".item_groups"))
    model = ItemGroup.query.get(id)

    if model:
        model.delete()
    return redirect(return_url)

@blueprint.route('/companies', methods=['GET'])
@login_required
def companies():
    """Companies Query"""
    return_url = request.args.get('next', url_for(".companies"))

    models = Company.query.all()
    return render('companies.html', models=models, return_url=return_url)

@blueprint.route('/company/create', methods=['POST', 'GET'])
@login_required
def company_create():
    """Company Create"""
    return_url = request.args.get('next', url_for(".companies"))
    model = Company('')
    form = CompanyForm(next=return_url)
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.company_create', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model.') + '%(error)s' % {'error':str(ex)}, 'danger')

    return render('company_create.html', form=form,
        return_url=return_url)

@blueprint.route('/company/edit/id=<int:id>', methods=['GET', 'POST'])
@login_required
def company_edit(id):
    """Company Edit"""
    return_url = request.args.get('next', url_for(".companies"))
    model = Company.query.get(id)

    if model is None:
        return redirect(return_url)

    form = CompanyForm(obj=model, next=return_url)
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('company_edit.html', form=form,
        return_url=return_url)

@blueprint.route('/company/delete/id=<int:id>', methods=['POST'])
@login_required
def company_delete(id):
    """Company Delete"""
    return_url = request.args.get('next', url_for(".companies"))
    model = Company.query.get(id)

    if model:
        model.delete()
    return redirect(return_url)

