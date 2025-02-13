# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import json
from jsbc.compat.OrderedDict import OrderedDict
from jsbc.compat.pathlib import pathlib

__version__ = '0.0.0'


class SettingsClass(OrderedDict):
    def __init__(self, Default=[], Data={}):
        self.filename = pathlib.Path('jsbc.settings.json')
        super(SettingsClass, self).__init__()
        self.Default = OrderedDict()
        self.addDefault(Default)
        self.addData(Data)

    def __getitem__(self, key):
        try:
            value = super(SettingsClass, self).__getitem__(key)
            if isinstance(value, dict) or self.Default.get(key, None) != value:
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
            for item in self.Default:
                if isinstance(key, item):
                    super(SettingsClass, self).__setitem__(key, value)
                    return
            else:
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
                except KeyError:
                    self[key] = SettingsClass(value)
                except ValueError:
                    pass
                else:
                    continue
            self[key] = value

    def export(self, defaults=False):
        Dict = {}
        for key in self.Default:
            if isinstance(key, type):
                for item in self:
                    if isinstance(self[item], SettingsClass):
                        Dict[item] = self[item].export(defaults)
                    else:
                        Dict[item] = self[item]
                continue

            if isinstance(self.Default[key], SettingsClass):
                Dict[key] = self.Default[key].export(defaults)
            else:
                try:
                    Dict[key] = super(SettingsClass, self).__getitem__(key)
                except KeyError:
                    if defaults:
                        Dict[key] = self.Default[key]

        return Dict

    def save(self, filename=None):
        self.filename = pathlib.Path(filename or self.filename)
        try:
            unicode
        except NameError:
            with self.filename.open('w') as f:
                json.dump(self.export(True), f, indent=4)
        else:
            with self.filename.open('wb') as f:
                json.dump(self.export(True), f, indent=4)

    def load(self, filename=None):
        self.filename = pathlib.Path(filename or self.filename)
        with self.filename.open('r') as f:
            self.addData(json.load(f))


settings = SettingsClass()


def DefaultSettings(AddDefaults, Data=settings):
    if isinstance(Data, SettingsClass):
        Settings = Data
        Settings.addDefault(AddDefaults)
    else:
        Settings = SettingsClass(AddDefaults)

    Settings.addData(Data)

    return Settings