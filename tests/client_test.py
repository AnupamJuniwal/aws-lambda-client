import os
import re

from tests import mock, unittest, HttpMock

from aws_lambda_client import api_creator, requester, LambdaClient
from aws_lambda_client.models.arn import INVALID_ARN_ERROR_MSG_TEMPLATE

TEST_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
TEST_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
TEST_AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN"
TEST_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"
TEST_ARN = 'arn:aws:lambda:us-west-2:000000000000:function:test-function-name'

class LambdaClientTest(unittest.TestCase):
    def setUp(self):
        self.target = LambdaClient
        # os.environ["AWS_SECRET_ACCESS_KEY"] = TEST_AWS_SECRET_ACCESS_KEY
        # os.environ["AWS_ACCESS_KEY_ID"] = TEST_AWS_ACCESS_KEY_ID
        # os.environ["AWS_SESSION_TOKEN"] = TEST_AWS_SESSION_TOKEN
        # os.environ["AWS_DEFAULT_REGION"] = TEST_AWS_DEFAULT_REGION
    
    @mock.patch('aws_lambda_client.api_creator.ApiCreator.__init__')
    def test_initiates_api_creator(self, mocked_api_creator):
        HttpMock.reset_http()
        mocked_api_creator.return_value = None
        LambdaClient()

        self.assertTrue(mocked_api_creator.called,
            'mocked_api_creator called')

    @mock.patch('aws_lambda_client.requester.AWSLambdaRequester.__init__')
    def test_initiates_requester(self, mocked_requester):
        HttpMock.reset_http()
        mocked_requester.return_value = None
        LambdaClient()

        self.assertTrue(mocked_requester.called,
            'mocked_requester called')
    
    
    @mock.patch('aws_lambda_client.requester.AWSLambdaRequester.__init__')
    def test_initiates_requester_with_passed_values(self, mocked_requester):
        HttpMock.reset_http()
        mocked_requester.return_value = None
        LambdaClient(
            AWS_SECRET_ACCESS_KEY = TEST_AWS_SECRET_ACCESS_KEY,
            AWS_ACCESS_KEY_ID = TEST_AWS_ACCESS_KEY_ID,
            AWS_SESSION_TOKEN = TEST_AWS_SESSION_TOKEN,
            AWS_DEFAULT_REGION = TEST_AWS_DEFAULT_REGION
        )

        # get call args
        name, args, kwargs = mocked_requester.mock_calls[0]
        secret, access_key, session_token, region = args

        self.assertTrue(mocked_requester.called,
            'mocked_requester called')
        self.assertEquals(secret, TEST_AWS_SECRET_ACCESS_KEY)
        self.assertEquals(access_key, TEST_AWS_ACCESS_KEY_ID)
        self.assertEquals(session_token, TEST_AWS_SESSION_TOKEN)
        self.assertEquals(region, TEST_AWS_DEFAULT_REGION)


    # Invoke tests
    def test_invoke_throws_error_if_arn_empty(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.invoke(payload="", version="1")
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, 'Empty ARN')

    def test_invoke_throws_error_if_invalid_arn_passed(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.invoke(arn="test", payload="", version="1")
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, INVALID_ARN_ERROR_MSG_TEMPLATE.format('test'))

    
    def test_invoke_throws_error_if_payload_empty(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.invoke(arn="test", version="1")
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, "Empty Payload")

    
    def test_invoke_throws_error_if_version_empty(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.invoke(arn="test", payload="1")
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, "Empty Version")


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.get_host')
    def test_invoke_calls_api_creator_get_host(self, mocked_get_host):
        mocked_get_host.return_value = "lambda.us-west-2.aws.com"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.invoke(arn=TEST_ARN, payload="", version="1")

        self.assertIsNotNone(lc)
        self.assertTrue(mocked_get_host.called)


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.get_host')
    def test_invoke_calls_api_creator_get_host_with_correct_args(self, mocked_get_host):
        mocked_get_host.return_value = "lambda.us-west-2.aws.com"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.invoke(arn=TEST_ARN, payload="", version="1")

        name, args, kwargs = mocked_get_host.mock_calls[0]
        partition, region = args
        self.assertIsNotNone(lc)
        self.assertTrue(mocked_get_host.called)
        self.assertEqual(partition, 'aws')
        self.assertEqual(region, 'us-west-2')


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.create_api')
    def test_invoke_calls_api_creator_create_api(self, mocked_create_api):
        mocked_create_api.return_value = "http://abc.com/?"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.invoke(arn=TEST_ARN, payload="", version="1")

        self.assertIsNotNone(lc)
        self.assertTrue(mocked_create_api.called)


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.create_api')
    def test_invoke_calls_api_creator_create_api_with_correct_args(self, mocked_create_api):
        mocked_create_api.return_value = "http://abc.com/?"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.invoke(arn=TEST_ARN, payload="", version="1")

        name, args, kwargs = mocked_create_api.mock_calls[0]
        partition, region, api, query, protocol, api_params = args
        self.assertIsNotNone(lc)
        self.assertTrue(mocked_create_api.called)
        self.assertEqual(partition, 'aws')
        self.assertEqual(region, 'us-west-2')
        self.assertEqual(api, "/2015-03-31/functions/{FunctionName}/invocations")
        self.assertDictEqual(query, {"Qualifier": "1"})
        self.assertEqual(protocol, 'https')
        self.assertDictEqual(api_params, {"FunctionName": TEST_ARN})


    # list alias tests
    def test_list_alias_throws_error_if_arn_empty(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.list_alias()
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, 'Empty ARN')

    def test_list_alias_throws_error_if_invalid_arn_passed(self):
        HttpMock.reset_http()
        lc = LambdaClient()
        error = None
        error_msg = None
        try:
            lc.list_alias(arn="test")
        except Exception as e:
            error = e
            error_msg = str(e)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error_msg)
        self.assertEquals(error_msg, INVALID_ARN_ERROR_MSG_TEMPLATE.format('test'))


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.get_host')
    def test_list_alias_calls_api_creator_get_host(self, mocked_get_host):
        mocked_get_host.return_value = "lambda.us-west-2.aws.com"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.list_alias(arn=TEST_ARN)

        self.assertIsNotNone(lc)
        self.assertTrue(mocked_get_host.called)


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.get_host')
    def test_list_alias_calls_api_creator_get_host_with_correct_args(self, mocked_get_host):
        mocked_get_host.return_value = "lambda.us-west-2.aws.com"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.list_alias(arn=TEST_ARN)

        name, args, kwargs = mocked_get_host.mock_calls[0]
        partition, region = args
        self.assertIsNotNone(lc)
        self.assertTrue(mocked_get_host.called)
        self.assertEqual(partition, 'aws')
        self.assertEqual(region, 'us-west-2')


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.create_api')
    def test_list_alias_calls_api_creator_create_api(self, mocked_create_api):
        mocked_create_api.return_value = "http://abc.com/?"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.list_alias(arn=TEST_ARN)

        self.assertIsNotNone(lc)
        self.assertTrue(mocked_create_api.called)


    @mock.patch('aws_lambda_client.api_creator.ApiCreator.create_api')
    def test_list_alias_calls_api_creator_create_api_with_correct_args(self, mocked_create_api):
        mocked_create_api.return_value = "http://abc.com/?"
        HttpMock.reset_http()
        lc = LambdaClient()
        lc.list_alias(arn=TEST_ARN)

        name, args, kwargs = mocked_create_api.mock_calls[0]
        partition, region, api, query, protocol, api_params = args
        self.assertIsNotNone(lc)
        self.assertTrue(mocked_create_api.called)
        self.assertEqual(partition, 'aws')
        self.assertEqual(region, 'us-west-2')
        self.assertEqual(api, "/2015-03-31/functions/{FunctionName}/aliases")
        self.assertDictEqual(query, {})
        self.assertEqual(protocol, 'https')
        self.assertDictEqual(api_params, {"FunctionName": TEST_ARN})