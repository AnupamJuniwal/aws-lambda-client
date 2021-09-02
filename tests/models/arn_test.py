from tests import mock, unittest

from tests.models import arn

ARN = arn.ARN
INVALID_ARN_ERROR_MSG_TEMPLATE = arn.INVALID_ARN_ERROR_MSG_TEMPLATE

TEST_ARN = 'arn:aws:lambda:us-west-2:000000000000:function:test-function-name'
class ArnTest(unittest.TestCase):
    def setUp(self):
        self.target = ARN


    def test_should_return_an_error_if_incorrect_arn_passed(self):
        error = None
        error_msg = None
        try:
            ARN('ABC')
        except Exception as e:
            error = e
            error_msg = str(e)

        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, INVALID_ARN_ERROR_MSG_TEMPLATE.format('ABC'))

    
    def test_should_return_a_valid_object_if_correct_arn_passed(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.__class__.__module__, 'aws_lambda_client.models.arn')
    
    
    def test_should_parse_and_return_partition(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_partition(), 'aws')

    
    def test_should_parse_and_return_account(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_account(), '000000000000')

    
    def test_should_parse_and_return_region(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_region(), 'us-west-2')


    def test_should_parse_and_return_function_name(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_resource_name(), 'test-function-name')
    
    def test_should_parse_and_return_resource(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_resource(), 'function')


    def test_should_parse_and_return_service(self):
        obj = ARN(TEST_ARN)
        self.assertIsNotNone(obj)
        self.assertEquals(obj.get_service(), 'lambda')


    def test_should_parse_and_return_all_details(self):
        obj = ARN(TEST_ARN)
        details = obj.get_details()
        self.assertIsNotNone(obj)
        self.assertIsNotNone(details)
        self.assertEquals(details.get('service'), 'lambda')
        self.assertEquals(details.get('resource_name'), 'test-function-name')
        self.assertEquals(details.get('resource'), 'function')
        self.assertEquals(details.get('region'), 'us-west-2')
        self.assertEquals(details.get('account'), '000000000000')
        self.assertEquals(details.get('partition'), 'aws')
    
    def test_should_return_original_arn_as_str_representation(self):
        test_arn = TEST_ARN
        obj = ARN(test_arn)
        self.assertIsNotNone(obj)
        self.assertEquals(str(obj), test_arn)
    