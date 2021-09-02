from tests import mock, unittest

from aws_lambda_client import api_creator

ApiCreator = api_creator.ApiCreator
class ApiCreatorTest(unittest.TestCase):
    def setUp(self):
        self.target = ApiCreator
    
    def test_endpoints_are_loaded(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertIsNotNone(ac.endpoints_raw)
    

    def test_endpoints_are_parsed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertIsNotNone(ac.endpoints)
    

    def test_endpoints_are_parsed_with_partition_as_key(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertIsNotNone(ac.endpoints)
        self.assertIn("aws", ac.endpoints.keys())
        self.assertIn("aws-cn", ac.endpoints.keys())
        self.assertIn("aws-us-gov", ac.endpoints.keys())
        self.assertIn("aws-iso", ac.endpoints.keys())
        self.assertIn("aws-iso-b", ac.endpoints.keys())


    def test_get_host_should_return_none_if_invalid_partition_passed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertIsNone(ac.get_host("", ""))
        self.assertIsNone(ac.get_host(None, ""))


    def test_get_host_should_return_correct_host_if_valid_listed_region_passed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertEquals(ac.get_host('aws', "fips-us-west-2"), 'lambda-fips.us-west-2.amazonaws.com')
    
    def test_get_host_should_return_host_from_template_if_unlisted_region_passed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        self.assertEquals(ac.get_host('aws', "us-west-2"), 'lambda.us-west-2.amazonaws.com')
        self.assertEquals(ac.get_host('aws-cn', "us-west-2"), 'lambda.us-west-2.amazonaws.com.cn')
        self.assertEquals(ac.get_host('aws-us-gov', "us-west-2"), 'lambda.us-west-2.amazonaws.com')
        self.assertEquals(ac.get_host('aws-iso', "us-west-2"), 'lambda.us-west-2.c2s.ic.gov')
        self.assertEquals(ac.get_host('aws-iso-b', "us-west-2"), 'lambda.us-west-2.sc2s.sgov.gov')

    def test_create_api_should_be_able_to_return_a_flat_url_if_correct_info_passed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        url = ac.create_api('aws', 'us-west-2', '/', {}, 'http', {})
        self.assertIsNotNone(url)
        self.assertEquals(url, 'http://lambda.us-west-2.amazonaws.com/?')

    
    def test_create_api_should_use_passed_protocol(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        url = ac.create_api('aws', 'us-west-2', '/', {}, 'http', {})
        self.assertIsNotNone(url)
        self.assertEquals(url, 'http://lambda.us-west-2.amazonaws.com/?')

        url2 = ac.create_api('aws', 'us-west-2', '/', {}, 'https', {})
        self.assertIsNotNone(url2)
        self.assertEquals(url2, 'https://lambda.us-west-2.amazonaws.com/?')


    def test_create_api_should_add_query_params_if_passed(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        url = ac.create_api('aws', 'us-west-2', '/abc', {"key": "value"}, 'http', {})
        self.assertIsNotNone(url)
        self.assertEquals(url, 'http://lambda.us-west-2.amazonaws.com/abc?key=value')

    
    def test_create_api_should_add_query_params_if_passed_with_special_symbols_encoded(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        url = ac.create_api('aws', 'us-west-2', '/abc', {"key": "//value"}, 'http', {})
        self.assertIsNotNone(url)
        self.assertEquals(url, 'http://lambda.us-west-2.amazonaws.com/abc?key=%2F%2Fvalue')


    def test_create_api_should_format_url_with_passed_api_params(self):
        ac = ApiCreator()

        self.assertIsNotNone(ac)
        url = ac.create_api('aws', 'us-west-2', '/abc/{someValue}', {}, 'http', {'someValue' : '1414141'})
        self.assertIsNotNone(url)
        self.assertEquals(url, 'http://lambda.us-west-2.amazonaws.com/abc/1414141?')

    
    def test_create_api_should_throw_error_on_missing_api_params(self):
        ac = ApiCreator()
        error = None
        error_msg = None
        self.assertIsNotNone(ac)
        try:
            url = ac.create_api('aws', 'us-west-2', '/abc/{someValue}', {}, 'http', {'someOtherValue' : '1414141'})
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, 'Invalid API params')