from tests import mock, unittest

from tests.models import arn

ARN = arn.ARN
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
        
        assert error is not None
        assert error_msg is not None

    
    def test_should_return_a_valid_object_if_correct_arn_passed(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.__class__.__module__ == 'aws_lambda_client.models.arn'
    
    
    def test_should_parse_and_return_partition(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_partition() == 'aws'

    
    def test_should_parse_and_return_account(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_account() == '000000000000'

    
    def test_should_parse_and_return_region(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_region() == 'us-west-2'


    def test_should_parse_and_return_function_name(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_resource_name() == 'test-function-name'
    
    def test_should_parse_and_return_resource(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_resource() == 'function'


    def test_should_parse_and_return_service(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        assert obj is not None
        assert obj.get_service() == 'lambda'


    def test_should_parse_and_return_all_details(self):
        obj = ARN('arn:aws:lambda:us-west-2:000000000000:function:test-function-name')
        details = obj.get_details()
        assert obj is not None
        assert details is not None
        assert details.get('service') == 'lambda'
        assert details.get('resource_name') == 'test-function-name'
        assert details.get('resource') == 'function'
        assert details.get('region') == 'us-west-2'
        assert details.get('account') == '000000000000'
        assert details.get('partition') == 'aws'
    
    def test_should_return_original_arn_as_str_representation(self):
        test_arn = 'arn:aws:lambda:us-west-2:000000000000:function:test-function-name'
        obj = ARN(test_arn)
        assert obj is not None
        assert str(obj) == test_arn
    