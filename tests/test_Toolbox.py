# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from jsbc.compat.python3 import *
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

    def test_create_object_with_addData(self):
        from jsbc.Toolbox import SettingsClass, DefaultSettings
        settingsDefaults = [
            ('servers', 'test'),
        ]
        settings = DefaultSettings(settingsDefaults, SettingsClass())
        settings.addData({'servers': 'test'})
        assert settings.export(True) == {'servers': 'test'}

    def test_create_object_with_addData_and_type(self):
        from jsbc.Toolbox import SettingsClass, DefaultSettings
        settingsDefaults = [
            (str, str),
        ]
        settings = DefaultSettings(settingsDefaults, SettingsClass())
        settings.addData({'servers': 'test'})
        assert settings.export(True) == {'servers': 'test'}

    def test_create_object_with_addData_and_type_with_subdata(self):
        from jsbc.Toolbox import SettingsClass, DefaultSettings
        settingsDefaults = [
            (str, [(str, str)]),
        ]
        settings = DefaultSettings(settingsDefaults, SettingsClass())
        settings.addData({'servers': {'32bit': "60cead10-0d05-624e-22e5-e8984c19a4f5",
                                    '64bit': "d21c3a54-52b3-18d3-5d6c-aae941c6757d"}})
        assert settings.export(True) == {'servers': {'32bit': "60cead10-0d05-624e-22e5-e8984c19a4f5",
                                    '64bit': "d21c3a54-52b3-18d3-5d6c-aae941c6757d"}}

    def test_create_object_save_and_load(self):
        from jsbc.compat.pathlib import pathlib
        from jsbc.Toolbox import SettingsClass, DefaultSettings

        settingsDefaults = [
            ('client', [
                ('name', 'KodiLib'),
                ('cache path', pathlib.Path('cache')),
                ('network', [
                    ('User-Agent', "{0}/{1} {2}"),
                ]),
                ('eventclient', [
                    ('enabled', True),
                ]),
                ('icon', [
                    ('url', None),
                    ('type', None),
                ]),
            ]),
            ('server', [
                ('friendlyName', 'Kodi'),
                ('name', 'Kodi'),
                ('version', ''),
                ('network', [
                    ('ip', 'localhost'),
                    ('udp', {
                        'port': 9777,
                    }),
                    ('http', {
                        'port': 8080,
                    }),
                    ('upnp', {
                        'id': '',
                    }),
                ]),
            ]),
            ('commands', [
                ('actions', "(('Code', {0}, {1}), ('HTML', 'http://kodi.wiki/view/Action_IDs', ['Action', 'Description']))"),
            ]),
        ]
        settings = DefaultSettings(settingsDefaults, SettingsClass())
        settings.save()

        settings2 = DefaultSettings(settingsDefaults, SettingsClass())
        settings2.load()
        assert settings.export(True) == settings2.export(True)
        settings.filename.unlink()


class test_settingsObject(unittest.TestCase):
    def test_test(self):
        from jsbc.Toolbox import SettingsClass, settings
        assert type(settings) == SettingsClass