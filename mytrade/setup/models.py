# -*- coding: utf-8 -*-

from mytrade.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Unit(SurrogatePK, Model):

    __tablename__ = 'units'
    unit_name = Column(db.String(80), unique=True, nullable=False)
    must_be_whole_number = Column(db.Boolean, default=False)

    def __init__(self, unit_name, **kwargs):
        db.Model.__init__(self, unit_name=unit_name, **kwargs)

    def __repr__(self):
        return '<Unit({name})>'.format(name=self.unit_name)

class Item_Group(SurrogatePK, Model):

    __tablename__ = 'item_groups'
    item_group_name = Column(db.String(80), unique=True, nullable=False)
    #parent_item_group_id = ReferenceCol('item_groups')
    #parent_item_group = relationship('Item_Group', backref='item_groups')

    # Only leaf nodes are allowed in transaction
    is_group = Column(db.Boolean, default=False)

    def __init__(self, item_group_name, **kwargs):
        db.Model.__init__(self, item_group_name=item_group_name, **kwargs)

    def __repr__(self):
        return '<Item Group({name})>'.format(name=self.item_group_name)

class Company(SurrogatePK, Model):
    
    __tablename__ = 'companys'
    company_name = Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Company({name})'.format(name=self.company_name)

