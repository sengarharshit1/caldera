import logging
from importlib import import_module

import marshmallow as ma

from app.objects.interfaces.i_object import FirstClassObjectInterface
from app.utility.base_object import BaseObject


class DataEncoderSchema(ma.Schema):
    name = ma.fields.String()
    description = ma.fields.String()
    module = ma.fields.String()


class DataEncoder(FirstClassObjectInterface, BaseObject):
    schema = DataEncoderSchema()
    display_schema = DataEncoderSchema(exclude=['module'])

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    def __init__(self, name, description, module):
        super().__init__()
        self.name = name
        self.description = description
        self.module = module

    def store(self, ram):
        existing = self.retrieve(ram['data_encoders'], self.unique)
        if not existing:
            ram['data_encoders'].append(self)
            return self.retrieve(ram['data_encoders'], self.unique)
        return existing

    def load(self):
        try:
            mod = import_module(self.module)
            return mod.DataEncoding()
        except Exception as e:
            logging.error('Error importing data encoder=%s, %s' % (self.name, e))
