import random
import sys
import time
import requests

import unittest

import aws_lambda_client

# Python 3 includes mocking, while 2 requires an extra module.
if sys.version_info[0] == 2:
    import mock
else:
    from unittest import mock

http_count = 0

class HttpMock:
    @staticmethod
    def request_proxy(*args, **kwargs):
        http_count += 1

    @staticmethod
    def reset_http():
        http_count = 0

    @staticmethod
    def get_http_count():
        return http_count

requests.request = HttpMock.request_proxy