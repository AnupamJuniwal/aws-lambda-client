import os

from tests import mock, unittest, HttpMock

from aws_lambda_client import requester, aws_auth

AWSLambdaRequester = requester.AWSLambdaRequester

class AWSRequestsAuthMock:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

TEST_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
TEST_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
TEST_AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN"
TEST_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"

class RequesterTest(unittest.TestCase):
    def setUp(self):
        self.target = AWSLambdaRequester
        os.environ["AWS_SECRET_ACCESS_KEY"] = TEST_AWS_SECRET_ACCESS_KEY
        os.environ["AWS_ACCESS_KEY_ID"] = TEST_AWS_ACCESS_KEY_ID
        os.environ["AWS_SESSION_TOKEN"] = TEST_AWS_SESSION_TOKEN
        os.environ["AWS_DEFAULT_REGION"] = TEST_AWS_DEFAULT_REGION


    def test_should_pick_up_credentials_from_environment(self):
        req = AWSLambdaRequester()

        assert req is not None
        assert req.aws_access_key_id == TEST_AWS_ACCESS_KEY_ID
        assert req.aws_region == TEST_AWS_DEFAULT_REGION
        assert req.aws_secret_access_key == TEST_AWS_SECRET_ACCESS_KEY
        assert req.aws_session_token == TEST_AWS_SESSION_TOKEN


    def test_should_override_region_with_passed_value(self):
        req = AWSLambdaRequester(region='us-west-2')

        assert req is not None
        assert req.aws_access_key_id == TEST_AWS_ACCESS_KEY_ID
        assert req.aws_region == 'us-west-2'
        assert req.aws_secret_access_key == TEST_AWS_SECRET_ACCESS_KEY
        assert req.aws_session_token == TEST_AWS_SESSION_TOKEN
   

    def test_should_override_access_key_with_passed_value(self):
        req = AWSLambdaRequester(access_key='access_key')

        assert req is not None
        assert req.aws_access_key_id == 'access_key'
        assert req.aws_region == TEST_AWS_DEFAULT_REGION
        assert req.aws_secret_access_key == TEST_AWS_SECRET_ACCESS_KEY
        assert req.aws_session_token == TEST_AWS_SESSION_TOKEN


    def test_should_override_secret_with_passed_value(self):
        req = AWSLambdaRequester(secret='secret')

        assert req is not None
        assert req.aws_access_key_id == TEST_AWS_ACCESS_KEY_ID
        assert req.aws_region == TEST_AWS_DEFAULT_REGION
        assert req.aws_secret_access_key == 'secret'
        assert req.aws_session_token == TEST_AWS_SESSION_TOKEN


    def test_should_override_session_token_with_passed_value(self):
        req = AWSLambdaRequester(session_token='token')

        assert req is not None
        assert req.aws_access_key_id == TEST_AWS_ACCESS_KEY_ID
        assert req.aws_region == TEST_AWS_DEFAULT_REGION
        assert req.aws_secret_access_key == TEST_AWS_SECRET_ACCESS_KEY
        assert req.aws_session_token == 'token'


    @mock.patch('aws_lambda_client.aws_auth.AWSRequestsAuth.__init__')
    def test_initiates_aws_auth(self, mocked_auth):
        HttpMock.reset_http()
        mocked_auth.return_value = None
        req = AWSLambdaRequester(session_token='token', secret='secret', access_key='access_key', region='us-west-2')

        self.assertIsNotNone(req)
        req.call('POST', 'http://abc.com/bcd', 'abc.com', {}, "")

        self.assertTrue(mocked_auth.called,
            'mocked_auth called called')

    def test_initiate_aws_auth_with_passed_values(self):
        HttpMock.reset_http()
        req = AWSLambdaRequester(session_token='token', secret='secret', access_key='access_key', region='us-west-2')

        self.assertIsNotNone(req)
        res = req.call('POST', 'http://abc.com/bcd', 'abc.com', {}, "")

        self.assertEquals(res.kwargs['auth'].aws_access_key, 'access_key')
        self.assertEquals(res.kwargs['auth'].aws_secret_access_key, 'secret')
        self.assertEquals(res.kwargs['auth'].aws_token, 'token')
        self.assertEquals(res.kwargs['auth'].aws_host, 'abc.com')
        self.assertEquals(res.kwargs['auth'].aws_region, 'us-west-2')

    
    def test_should_fire_a_request_using_requests_module(self):
        HttpMock.reset_http()
        req = AWSLambdaRequester(session_token='token', secret='secret', access_key='access_key', region='us-west-2')

        self.assertIsNotNone(req)
        res = req.call('POST', 'http://abc.com/bcd', 'abc.com', {}, "")

        self.assertAlmostEqual(HttpMock.get_http_count(), 1)