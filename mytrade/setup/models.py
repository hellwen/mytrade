# -*- coding: utf-8 -*-

from mytrade.database import (
    Column,
    db,
    Model,
#    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Unit(SurrogatePK, Model):

    __tablename__ = 'units'
    unit_name = Column(db.String(80), unique=True, nullable=False)
    must_be_whole_number = Column(db.Boolean, default=True)

    def __init__(self, unit_name, **kwargs):
        db.Model.__init__(self, unit_name=unit_name, **kwargs)

    def __str__(self):
        return u'{name}'.format(name=self.unit_name)

    def __repr__(self):
        return u'<Unit({name})>'.format(name=self.unit_name)

class ItemGroup(Model):

    __tablename__ = 'item_groups'

    id = db.Column(db.Integer, primary_key=True)

    item_group_name = Column(db.String(80), unique=True, nullable=False)
    parent_id = Column(db.Integer, db.ForeignKey('item_groups.id'))
    parent = relationship('ItemGroup', remote_side=[id])

    # Only leaf nodes are allowed in transaction
    is_group = Column(db.Boolean, default=False)

    def __init__(self, item_group_name, **kwargs):
        db.Model.__init__(self, item_group_name=item_group_name, **kwargs)

    def __str__(self):
        return u'{name}'.format(name=self.item_group_name)

    def __repr__(self):
        return u'<Item Group({name})>'.format(name=self.item_group_name)

class Company(SurrogatePK, Model):
    
    __tablename__ = 'companies'
    company_name = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, company_name, **kwargs):
        db.Model.__init__(self, company_name=company_name, **kwargs)

    def __str__(self):
        return u'{name}'.format(name=self.company_name)

    def __repr__(self):
        return u'<Company({name})'.format(name=self.company_name)

