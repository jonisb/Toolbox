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
