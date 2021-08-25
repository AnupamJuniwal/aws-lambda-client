import os
import requests

from requests_auth_aws_sigv4 import AWSSigV4

class AWSLambdaRequester:
    """Creates a lambda http requester.
        Can take credentials for custom access.
        kwargs:
            AWS_SECRET_ACCESS_KEY (str)
            AWS_ACCESS_KEY_ID (str)
            AWS_SESSION_TOKEN (str)
    """
    def __init__(self, secret = None, access_key=None, session_token=None):
        if secret is None:
            secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        if access_key is None:
            access_key = os.getenv('AWS_ACCESS_KEY_ID')
        if session_token is None:
            session_token = os.getenv('AWS_SESSION_TOKEN')
        self.aws_auth = AWSSigV4('lambda',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
            aws_session_token=session_token,
        )

    def call(self, method, headers, url, payload):
        """Call api endpoint

        Args:
            method (str): POST | GET | PUT | PATCH | DELETE
            headers (dict): custom headers to add in request
            url (str): complete url of a service
            payload (dict): Final payload

        Returns:
            [type]: [description]
        """
        r = requests.request(method, url, headers = headers, data = payload, auth=self.aws_auth)
        return r
