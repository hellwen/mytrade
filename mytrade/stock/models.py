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

    __tablename__ = 'warehouse'
    warehouse_name = Column(db.String(80), unique=True, nullable=False)
    #company_id = ReferenceCol('companys', nullable=True)
    #company = relationship('Company', backref='warehouses')

    disabled = Column(db.Boolean(), default=False)

    #country = Column(db.String(80), unique=True, nullable=False)
    #province = Column(db.String(80), unique=True, nullable=False)
    #city = Column(db.String(80), unique=True, nullable=False)
    #address1 = Column(db.String(80), unique=True, nullable=False)
    #address2 = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, warehouse_name, **kwargs):
        db.Model.__init__(self, name=warehouse_name, **kwargs)

    def __repr__(self):
        return '<Warehouse({name})>'.format(name=self.warehouse_name)


class Item(SurrogatePK, Model):

    __tablename__ = 'items'
    item_code = Column(db.String(80), unique=True, nullable=False)
    item_name = Column(db.String(80), unique=False, nullable=False)

    # Item Group
    item_group_id = ReferenceCol('item_groups', nullable=True)
    item_group = relationship('Item_Group', backref='items')

    # Default Unit
    default_unit_id = ReferenceCol('units', nullable=True)
    default_unit = relationship('Unit', backref='items')

    # Default Warehouse
    #default_warehouse_id = ReferenceCol('warehouses', nullable=True)
    #default_warehouse = relationship('Warehouse', backref='items')

    description = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, item_code, item_name, **kwargs):
        db.Model.__init__(self, item_code=item_code, item_name=item_name, **kwargs)

    def __repr__(self):
        return '<Item({code,name!r})>'.format(code=self.item_code, name=self.item_name)
