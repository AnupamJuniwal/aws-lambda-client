from tests import mock, unittest

from aws_lambda_client import api_creator

ApiCreator = api_creator.ApiCreator
class ApiCreatorTest(unittest.TestCase):
    def setUp(self):
        self.target = ApiCreator
    
    def test_endpoints_are_loaded(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.endpoints_raw is not None
    

    def test_endpoints_are_parsed(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.endpoints is not None
    

    def test_endpoints_are_parsed_with_partition_as_key(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.endpoints is not None
        assert ac.endpoints.keys().__contains__("aws")
        assert ac.endpoints.keys().__contains__("aws-cn")
        assert ac.endpoints.keys().__contains__("aws-us-gov")
        assert ac.endpoints.keys().__contains__("aws-iso")
        assert ac.endpoints.keys().__contains__("aws-iso-b")


    def test_get_host_should_return_none_if_invalid_partition_passed(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.get_host("", "") is None
        assert ac.get_host(None, "") is None


    def test_get_host_should_return_correct_host_if_valid_listed_region_passed(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.get_host('aws', "fips-us-west-2") == 'lambda-fips.us-west-2.amazonaws.com'
    
    def test_get_host_should_return_host_from_template_if_unlisted_region_passed(self):
        ac = ApiCreator()

        assert ac is not None
        assert ac.get_host('aws', "us-west-2") == 'lambda.us-west-2.amazonaws.com'
        assert ac.get_host('aws-cn', "us-west-2") == 'lambda.us-west-2.amazonaws.com.cn'
        assert ac.get_host('aws-us-gov', "us-west-2") == 'lambda.us-west-2.amazonaws.com'
        assert ac.get_host('aws-iso', "us-west-2") == 'lambda.us-west-2.c2s.ic.gov'
        assert ac.get_host('aws-iso-b', "us-west-2") == 'lambda.us-west-2.sc2s.sgov.gov'

    def test_create_api_should_be_able_to_return_a_flat_url_if_correct_info_passed(self):
        ac = ApiCreator()

        assert ac is not None
        url = ac.create_api('aws', 'us-west-2', '/', {}, 'http', {})
        assert url is not None
        assert url == 'http://lambda.us-west-2.amazonaws.com/?'

    
    def test_create_api_should_use_passed_protocol(self):
        ac = ApiCreator()

        assert ac is not None
        url = ac.create_api('aws', 'us-west-2', '/', {}, 'http', {})
        assert url is not None
        assert url == 'http://lambda.us-west-2.amazonaws.com/?'

        url2 = ac.create_api('aws', 'us-west-2', '/', {}, 'https', {})
        assert url2 is not None
        assert url2 == 'https://lambda.us-west-2.amazonaws.com/?'


    def test_create_api_should_add_query_params_if_passed(self):
        ac = ApiCreator()

        assert ac is not None
        url = ac.create_api('aws', 'us-west-2', '/abc', {"key": "value"}, 'http', {})
        assert url is not None
        assert url == 'http://lambda.us-west-2.amazonaws.com/abc?key=value'

    
    def test_create_api_should_add_query_params_if_passed_with_special_symbols_encoded(self):
        ac = ApiCreator()

        assert ac is not None
        url = ac.create_api('aws', 'us-west-2', '/abc', {"key": "//value"}, 'http', {})
        assert url is not None
        assert url == 'http://lambda.us-west-2.amazonaws.com/abc?key=%2F%2Fvalue'


    def test_create_api_should_format_url_with_passed_api_params(self):
        ac = ApiCreator()

        assert ac is not None
        url = ac.create_api('aws', 'us-west-2', '/abc/{someValue}', {}, 'http', {'someValue' : '1414141'})
        assert url is not None
        assert url == 'http://lambda.us-west-2.amazonaws.com/abc/1414141?'

    
    def test_create_api_should_throw_error_on_missing_api_params(self):
        ac = ApiCreator()
        error = None
        error_msg = None
        assert ac is not None
        try:
            url = ac.create_api('aws', 'us-west-2', '/abc/{someValue}', {}, 'http', {'someOtherValue' : '1414141'})
        except Exception as e:
            error = e
            error_msg = str(e)
        assert error is not None
        assert error_msg is not None
        assert error_msg == 'Invalid API params'