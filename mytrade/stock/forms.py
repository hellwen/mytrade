# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length

from .models import Warehouse, Item

from mytrade.form.fields import Select2Field
from mytrade.utils import _

class WarehouseForm(Form):
    id = IntegerField()

    warehouse_name = TextField(_('Warehouse Name'),
                 validators=[DataRequired(), Length(max=25)])

    company_id = Select2Field(_('Company'), default=0, coerce=int)

    address1 = TextField(_('Address1'))
    address2 = TextField(_('Address2'))

    disabled = BooleanField(_('Disabled'))

    def __init__(self, *args, **kwargs):
        super(WarehouseForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(WarehouseForm, self).validate()
        if not initial_validation:
            return False

        warehouse = Warehouse.query.filter(Warehouse.warehouse_name==self.warehouse_name.data, Warehouse.id != self.id.data).first()
        if warehouse:
            self.warehouse_name.errors.append(_("Warehouse Name already existed"))
            return False
        return True


class ItemForm(Form):
    id = IntegerField()

    item_code = TextField(_('Item Code'),
                 validators=[DataRequired(), Length(min=3, max=25)])
    item_name = TextField(_('Item Name'),
                 validators=[DataRequired(), Length(max=25)])

    item_group_id = Select2Field(_('Item Group'), default=0, coerce=int)
    default_unit_id = Select2Field(_('Default Unit'), default=0, coerce=int)
    default_warehouse_id = Select2Field(_('Default Warehouse'), default=0, coerce=int)

    description = TextField(_('Description'))

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(ItemForm, self).validate()
        if not initial_validation:
            return False

        item = Item.query.filter(Item.item_code==self.item_code.data, Item.id != self.id.data).first()
        if item:
            self.item_code.errors.append(_("Item Code already existed"))
            return False

        item = Item.query.filter(Item.item_name==self.item_name.data, Item.id != self.id.data).first()
        if item:
            self.item_name.errors.append(_("Item Name already existed"))
            return False

        return True

