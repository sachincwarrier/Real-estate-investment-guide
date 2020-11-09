# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.analysis import Analysis  # noqa: E501
from swagger_server.models.details import Details  # noqa: E501
from swagger_server.models.model_property import ModelProperty  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPropertiesController(BaseTestCase):
    """PropertiesController integration test stubs"""

    def test_find_properties_by_zip_code(self):
        """Test case for find_properties_by_zip_code

        Find Properties by Zip Code
        """
        query_string = [('finance', true),
                        ('cashDown', 789),
                        ('maxPrice', 789),
                        ('minPrice', 789),
                        ('propertyType', 'propertyType_example'),
                        ('bedrooms', 789),
                        ('bathrooms', 789)]
        response = self.client.open(
            '/v1/properties/findByZipCode/{zipcode}'.format(zipcode=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_properties(self):
        """Test case for get_all_properties

        Get all properties
        """
        query_string = [('finance', true),
                        ('cashDown', 789),
                        ('maxPrice', 789),
                        ('minPrice', 789),
                        ('propertyType', 'propertyType_example'),
                        ('bedrooms', 789),
                        ('bathrooms', 789)]
        response = self.client.open(
            '/v1/properties',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_analysis_by_id(self):
        """Test case for get_analysis_by_id

        Return analysis of property by ID
        """
        query_string = [('finance', true),
                        ('cashDown', 789),
                        ('interestRate', 3.4),
                        ('term', 789)]
        response = self.client.open(
            '/v1/properties/analysis/{propertyID}'.format(propertyID=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_details_by_id(self):
        """Test case for get_details_by_id

        Return details of property by ID
        """
        response = self.client.open(
            '/v1/properties/details/{propertyID}'.format(propertyID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
