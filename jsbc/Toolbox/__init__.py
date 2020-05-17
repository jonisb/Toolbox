# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from jsbc.compat.OrderedDict import OrderedDict

__version__ = '0.0.0'


class SettingsClass(OrderedDict):
    def __init__(self, Default=[], Data={}):
        super(SettingsClass, self).__init__()
        self.Default = OrderedDict()
        self.addDefault(Default)
        self.addData(Data)

    def __getitem__(self, key):
        try:
            value = super(SettingsClass, self).__getitem__(key)
            if isinstance(value, dict) or self.Default[key] != value:
                return value
            else:
                del self[key]
        except KeyError:
            if isinstance(self.Default[key], SettingsClass):
                self[key] = self.Default[key]
        return self.Default[key]  # TODO Return copy?

    def __setitem__(self, key, value):
        try:
            if self.Default[key] != value:
                super(SettingsClass, self).__setitem__(key, value)
            else:
                try:
                    del self[key]
                except KeyError:  # TODO
                    pass
        except KeyError:  # TODO
            raise KeyError('Default key not defined', key)

    def addDefault(self, Default):
        for key, value in Default if isinstance(Default, list) else Default.items():
            if isinstance(value, (list, dict)):
                try:
                    self.Default[key].addDefault(value)
                except KeyError:
                    try:
                        self.Default[key] = SettingsClass(value)
                    except ValueError:
                        pass
                    else:
                        continue
                else:
                    continue
            self.Default[key] = value

    def addData(self, Data):
        for key, value in Data.items():
            if isinstance(value, dict):
                try:
                    self[key].addData(value)
                except ValueError:
                    pass
                else:
                    continue
            if self.Default[key] != value:
                self[key] = value
            else:
                del self[key]

    def export(self, defaults=False):
        Dict = {}
        for key in self.Default:
            if isinstance(self.Default[key], SettingsClass):
                Dict[key] = self.Default[key].export(defaults)
            else:
                try:
                    Dict[key] = super(SettingsClass, self).__getitem__(key)
                except KeyError:
                    if defaults:
                        Dict[key] = self.Default[key]

        return Dict