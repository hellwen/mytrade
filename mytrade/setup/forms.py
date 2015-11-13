# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired, Length

from .models import Unit#, Item_Group, Company

class UnitForm(Form):
    unit_name = TextField('Unit Name',
                    validators=[DataRequired(), Length(max=80)])
    must_be_whole_number = BooleanField('Must be whole Number',
                    default="checked")

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.unit = None

    def validate(self):
        initial_validation = super(UnitForm, self).validate()
        if not initial_validation:
            return False
        unit = Unit.query.filter_by(unit_name=self.unit_name.data).first()
        if unit:
            self.unit_name.errors.append("Unit Name already registered")
            return False
        return True
