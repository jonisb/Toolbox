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

    def test_create_object_with_type(self):
        from jsbc.Toolbox import SettingsClass, DefaultSettings
        settingsDefaults = [
            ('servers', [
                (int, [
                ]),
            ]),
        ]
        settings = DefaultSettings(settingsDefaults, SettingsClass())

        assert settings.export(True) == {'servers': {}}, settings.export()
        settings['servers'][15] = {}
        assert settings.export(True) == {'servers': {15: {}}}, settings.export()
        settings['servers'][20] = {'32bit': "60cead10-0d05-624e-22e5-e8984c19a4f5",
                                    '64bit': "d21c3a54-52b3-18d3-5d6c-aae941c6757d"}
        assert settings.export(True) == {'servers': {15: {}, 20: {'32bit': "60cead10-0d05-624e-22e5-e8984c19a4f5",
                                    '64bit': "d21c3a54-52b3-18d3-5d6c-aae941c6757d"}}}, settings.export()
        try:
            settings['servers']['16'] = {'32bit': "0c91ea09-d44a-bc0c-f4da-75e87388e178"}
        except KeyError:
            self.assertTrue(True)


class test_settingsObject(unittest.TestCase):
    def test_test(self):
        from jsbc.Toolbox import SettingsClass, settings
        assert type(settings) == SettingsClass