# -*- coding: utf-8 -*-
"""
    test_api

    Test the API

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest
from decimal import Decimal
from configparser import ConfigParser

from avatax import API, AvataxError


class TestAPI(unittest.TestCase):

    def setUp(self):
        parser = ConfigParser()
        parser.read('account.cfg')

        self.api = API(
            parser.get('avalara', 'account_number'),
            parser.get('avalara', 'license_key'),
            parser.get('avalara', 'url'),
        )

    def test_0010_address_validate(self):
        """
        Try sending an incomplete address and get back the address
        """
        response = self.api.address_validate(
            Line1 = '1706 Biscayne Blvd',
            Line2 = '',
            City = 'Miami',
            PostalCode = '33137',
            Region = 'Florida',
            Country = 'USA',
        )
        self.assertEqual(response['County'], 'MIAMI-DADE')

        self.assertRaises(
            AvataxError,
            self.api.address_validate,
            Country='USA'
        )

    def test_0020_tax_get(self):
        """
        Get the tax amount
        """
        response = self.api.tax_get(47.627935, -122.51702, Decimal('10.234'))

        self.assertEqual(response['ResultCode'], 'Success')
        self.assertTrue('Rate' in response)
        self.assertTrue('Tax' in response)
        self.assertTrue('Rate' in response)
        self.assertTrue('TaxDetails' in response)

    def test_0030_tax_get_detailed(self):
        """
        Get the detailed Tax information
        """
        data = {
            'DocDate': '2011-05-11',
            'CustomerCode': 'CUST1',
            'Lines': [
                {
                    'DestinationCode': '1',
                    'Amount': 10, 'Qty': 1,
                    'LineNo': '1',
                    'OriginCode': '1'
                }
            ],
            'Addresses': [
                {
                    'PostalCode': '33137',
                    'AddressCode': '1',
                    'Line1': '1706 Biscayne Boulevard'
                }
            ]
        }
        response = self.api.tax_get_detailed(**data)

        self.assertEqual(response['ResultCode'], 'Success')
        self.assertTrue('TotalTaxable' in response)
        self.assertTrue('TaxLines' in response)
        self.assertTrue('DocCode' in response)
        self.assertTrue('TaxAddresses' in response)
        self.assertTrue('TaxDate' in response)

    def test_0040_test_connection(self):
        """
        Check if the test_connection API works
        """
        self.assertTrue(self.api.test_connection())


if __name__ == '__main__':
    unittest.main()
