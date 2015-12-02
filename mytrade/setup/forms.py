# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, required

from .models import Unit, ItemGroup, Company

from mytrade.form.fields import Select2Field
from mytrade.utils import _


class UnitForm(Form):
    id = IntegerField()
    unit_name = TextField(_('Unit Name'),
                    validators=[DataRequired(), Length(max=80)])
    must_be_whole_number = BooleanField(_('Must be whole Number'),
                    default="checked")

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.unit = None

    def validate(self):
        initial_validation = super(UnitForm, self).validate()
        if not initial_validation:
            return False

        unit = Unit.query.filter(Unit.unit_name==self.unit_name.data, Unit.id != self.id.data).first()
        if unit:
            self.unit_name.errors.append(_("Unit Name already existed"))
            return False
        return True

class ItemGroupForm(Form):
    id = IntegerField()
    item_group_name = TextField(_('Item Group'),
                    validators=[DataRequired(), Length(max=80)])

    parent_id = Select2Field(_('Parent'), default=0, coerce=int)

    is_group = BooleanField(_('Is Group?'),
                    default="checked")

    def __init__(self, *args, **kwargs):
        super(ItemGroupForm, self).__init__(*args, **kwargs)
        self.item_group = None

    def validate(self):
        initial_validation = super(ItemGroupForm, self).validate()
        if not initial_validation:
            return False

        item_group = ItemGroup.query.filter(ItemGroup.item_group_name==self.item_group_name.data, ItemGroup.id != self.id.data).first()
        if item_group:
            self.item_group_name.errors.append(_("Item Group Name already existed"))
            return False

        return True

class CompanyForm(Form):
    id = IntegerField()
    company_name = TextField(_('Company Name'),
                    validators=[DataRequired(), Length(max=80)])

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        #self.company = None

    def validate(self):
        initial_validation = super(CompanyForm, self).validate()
        if not initial_validation:
            return False

        company = Company.query.filter(Company.company_name == self.company_name.data, Company.id != self.id.data).first()
        if company:
            self.company_name.errors.append(_("Company Name already existed"))
            return False

        return True
