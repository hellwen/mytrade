# -*- coding: utf-8 -*-

from mytrade.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Warehouse(SurrogatePK, Model):

    __tablename__ = 'warehouses'
    warehouse_name = Column(db.String(80), unique=True, nullable=False)
    company_id = ReferenceCol('companies', nullable=True)
    company = relationship('Company', backref='warehouses')

    disabled = Column(db.Boolean(), default=False)

    #country = Column(db.String(80), unique=True, nullable=False)
    #province = Column(db.String(80), unique=True, nullable=False)
    #city = Column(db.String(80), unique=True, nullable=False)

    address1 = Column(db.String(200), unique=True, nullable=False)
    address2 = Column(db.String(200), unique=True, nullable=False)

    def __init__(self, warehouse_name, **kwargs):
        db.Model.__init__(self, warehouse_name=warehouse_name, **kwargs)

    def __str__(self):
        return u'{name}'.format(name=self.warehouse_name)

    def __repr__(self):
        return u'<Warehouse({name})>'.format(name=self.warehouse_name)


class Item(SurrogatePK, Model):

    __tablename__ = 'items'
    item_code = Column(db.String(80), unique=True, nullable=False)
    item_name = Column(db.String(80), unique=False, nullable=False)

    # Item Group
    item_group_id = ReferenceCol('item_groups', nullable=True)
    item_group = relationship('ItemGroup', backref='items')

    # Default Unit
    default_unit_id = ReferenceCol('units', nullable=True)
    default_unit = relationship('Unit', backref='items')

    # Default Warehouse
    default_warehouse_id = ReferenceCol('warehouses', nullable=True)
    default_warehouse = relationship('Warehouse', backref='items')

    description = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, item_code, item_name, **kwargs):
        db.Model.__init__(self, item_code=item_code, item_name=item_name, **kwargs)

    def __str__(self):
        return u'{code},{name}'.format(code=self.item_code, name=self.item_name)

    def __repr__(self):
        return u'<Item({code},{name})>'.format(code=self.item_code, name=self.item_name)
