import datetime
from uuid import uuid4
import re
import logging


class FileModel(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid')
        self.name = kwargs.get('name')
        self.data_dict = kwargs.get("data_dict", None)
        self.key_list = list(self.data_dict.keys())
        self.value_list = list(self.data_dict.values())

    # @classmethod
    # def


    def to_dict(self, child_object=None, fields=None,):
        if not child_object:
            child_object = self
        result = {}
        for attribute in dir(child_object):
            if fields and attribute not in fields:
                continue

            attr = getattr(child_object, attribute)

            if callable(attr):
                continue

            if isinstance(attr, list):
                result[attribute] = []
                if not len(attr):
                    continue

                if isinstance(attr[0], int) or isinstance(attr[0], str):
                    result[attribute] = attr
                    continue

                for row in attr:
                    if isinstance(row, object):
                        result[attribute].append(self.to_dict(row))
                    else:
                        result[attribute].append(row)
                continue
            result[attribute] = attr
        return result

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
