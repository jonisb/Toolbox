# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import unittest


class test_SettingsClass(unittest.TestCase):
    def test_create_empty_object(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass()
        assert type(settings) == SettingsClass
        assert settings.export() == {}
        assert settings.export(True) == {}

    def test_create_simple_object_with_default_value(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass({'name': 'test'})
        assert settings.export() == {}
        assert settings.export(True) == {'name': 'test'}

    def test_create_simple_object_addDefault_value(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass()
        settings.addDefault({'name': 'test'})
        assert settings.export() == {}
        assert settings.export(True) == {'name': 'test'}

    def test_create_simple_object_with_default_value_new_data(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass({'name': 'test'}, {'name': 'test2'})
        assert settings.export() == {'name': 'test2'}

    def test_create_simple_object_with_default_value_addData(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass({'name': 'test'})
        settings.addData({'name': 'test2'})
        assert settings.export() == {'name': 'test2'}

    def test_create_simple_object_with_deep_default_value(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass({'name': {'name2': 'test2'}})
        assert settings.export() == {'name': {}}, settings.export()
        assert settings.export(True) == {'name': {'name2': 'test2'}}

    def test_create_simple_object_with_deep_default_value_deep_data(self):
        from jsbc.Toolbox import SettingsClass
        settings = SettingsClass({'name': {'name2': 'test2'}}, {'name': {'name2': 'test3'}})
        assert settings.export() == {'name': {'name2': 'test3'}}
        assert settings.export(True) == {'name': {'name2': 'test3'}}
        settings['name']['name2'] = 'test4'
        assert settings.export() == {'name': {'name2': 'test4'}}
        settings['name']['name2'] = 'test2'
        assert settings.export() == {'name': {}}, settings.export()
        assert settings.export(True) == {'name': {'name2': 'test2'}}
