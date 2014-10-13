# -*- coding: utf-8 -*-

from zope.interface import Invalid

from seantis.plonetools import tests
from seantis.plonetools import schemafields


class TestSchemafields(tests.IntegrationTestCase):

    def test_validate_email(self):
        schemafields.validate_email(u'')
        schemafields.validate_email(u'test@example.org')
        schemafields.validate_email(u' test@example.org ')
        self.assertRaises(Invalid, schemafields.validate_email, u'asdf')

    def test_validate_color(self):
        schemafields.validate_hex_color('')
        schemafields.validate_hex_color('red')
        schemafields.validate_hex_color('#000')
        self.assertRaises(Invalid, schemafields.validate_hex_color, u'#0')

    def test_validate_iban(self):
        schemafields.validate_iban(u'')
        schemafields.validate_iban(u'BE31435411161155')
        self.assertRaises(Invalid, schemafields.validate_iban, u'asdf')
