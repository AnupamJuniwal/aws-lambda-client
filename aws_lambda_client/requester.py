import os
import requests

from aws_lambda_client.aws_auth import AWSRequestsAuth


class AWSLambdaRequester:
    """Creates a lambda http requester.
        Can take credentials for custom access.
        Args:
            secret (str)
            access_key (str)
            session_token (str)
            region (str)
    """
    def __init__(self, secret = None, access_key=None, session_token=None, region=None):
        if secret is None:
            secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        if access_key is None:
            access_key = os.getenv('AWS_ACCESS_KEY_ID')
        if session_token is None:
            session_token = os.getenv('AWS_SESSION_TOKEN')
        if region is None:
            region = os.getenv('AWS_DEFAULT_REGION')
        
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret
        self.aws_session_token = session_token
        self.aws_region = region

    def call(self, method, url, host, headers, payload):
        """Call api endpoint

        Args:
            method (str): POST | GET | PUT | PATCH | DELETE
            url (str): complete url of a service
            host (str): host for the request {service}:{region}:{partition}
            headers (dict): custom headers to add in request
            payload (dict): Final payload

        Returns:
            [type]: [description]
        """

        auth = AWSRequestsAuth(aws_access_key=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key,
                            aws_token = self.aws_session_token,
                            aws_host=host,
                            aws_region=self.aws_region,
                            aws_service='lambda')

        r = requests.request(method, url, headers = headers, data = payload, auth=auth)
        return r
