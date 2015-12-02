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
    Warehouse,
    Item,
)
from .forms import (
    WarehouseForm,
    ItemForm,
)
from mytrade.setup.models import (
    Unit,
    ItemGroup,
    Company,
)
from mytrade.extensions import db
from mytrade.utils import render, _

blueprint = Blueprint("stock", __name__, url_prefix='/stock',
                      static_folder="../static",
                      template_folder="../templates/stock")


@blueprint.route('/warehouses', methods=['GET'])
@login_required
def warehouses():
    """Warehouse Query"""
    return_url = request.args.get('next', url_for(".warehouses"))

    models = Warehouse.query.all()
    return render('warehouses.html', models=models, return_url=return_url)

@blueprint.route('/warehouse/create', methods=['POST', 'GET'])
@login_required
def warehouse_create():
    """Warehouse Create"""
    return_url = request.args.get('next', url_for(".warehouses"))
    model = Warehouse('')
    form = WarehouseForm(next=return_url, disabled=False)
    form.company_id.choices = [(r.id, r.company_name) for r in Company.query.filter_by().order_by('company_name')]
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.warehouse_create', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model.') + '%(error)s' % {'error':str(ex)}, 'danger')

    return render('warehouse_create.html', form=form,
        return_url=return_url)

@blueprint.route('/warehouse/edit/id=<int:id>', methods=['GET', 'POST'])
@login_required
def warehouse_edit(id):
    """Warehouse Edit"""
    return_url = request.args.get('next', url_for(".warehouses"))
    model = Warehouse.query.get(id)

    if model is None:
        return redirect(return_url)

    form = WarehouseForm(obj=model, next=return_url)
    form.company_id.choices = [(r.id, r.company_name) for r in Company.query.filter_by().order_by('company_name')]
    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('warehouse_edit.html', form=form,
        return_url=return_url)

@blueprint.route('/warehouse/delete/id=<int:id>', methods=['POST'])
@login_required
def warehouse_delete(id):
    """Warehouse Delete"""
    return_url = request.args.get('next', url_for(".warehouses"))
    model = Warehouse.query.filter_by(id=id).first()

    if model:
        model.delete()
    return redirect(return_url)

@blueprint.route('/items', methods=['GET'])
@login_required
def items():
    """Item Query"""
    return_url = request.args.get('next', url_for(".items"))

    models = Item.query.all()
    return render('items.html', models=models, return_url=return_url)

@blueprint.route('/item/create', methods=['POST', 'GET'])
@login_required
def item_create():
    """Item Create"""
    return_url = request.args.get('next', url_for(".items"))
    model = Item('', '')

    form = ItemForm(next=return_url)
    form.item_group_id.choices = [(r.id, r.item_group_name) for r in ItemGroup.query.filter_by().order_by('item_group_name')]
    form.default_unit_id.choices = [(r.id, r.unit_name) for r in Unit.query.filter_by().order_by('unit_name')]
    form.default_warehouse_id.choices = [(r.id, r.warehouse_name) for r in Warehouse.query.filter_by().order_by('warehouse_name')]

    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.item_create', url=return_url))
            else:
                return redirect(return_url)
        except Exception, ex:
            db.session.rollback()
            flash(_('Failed to update model.') + '%(error)s' % {'error':str(ex)}, 'danger')

    return render('item_create.html', form=form,
        return_url=return_url)

@blueprint.route('/item/edit/id=<int:id>', methods=['GET', 'POST'])
@login_required
def item_edit(id):
    """Item Edit"""
    return_url = request.args.get('next', url_for(".items"))
    model = Item.query.get(id)

    if model is None:
        return redirect(return_url)

    form = ItemForm(obj=model, next=return_url)
    form.item_group_id.choices = [(r.id, r.item_group_name) for r in ItemGroup.query.filter_by().order_by('item_group_name')]
    form.default_unit_id.choices = [(r.id, r.unit_name) for r in Unit.query.filter_by().order_by('unit_name')]
    form.default_warehouse_id.choices = [(r.id, r.warehouse_name) for r in Warehouse.query.filter_by().order_by('warehouse_name')]

    if form.validate_on_submit():
        try:
            form.populate_obj(model)
            db.session.commit()
            return redirect(return_url)
        except Exception:
            db.session.rollback()
            flash(_('Failed to update model.'))

    return render('item_edit.html', form=form,
        return_url=return_url)

@blueprint.route('/item/delete/id=<int:id>', methods=['POST'])
@login_required
def item_delete(id):
    """Item Delete"""
    return_url = request.args.get('next', url_for(".items"))
    model = Item.query.get(id)

    if model:
        model.delete()
    return redirect(return_url)

