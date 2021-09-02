import random
import sys
import time
import requests

import unittest

# Python 3 includes mocking, while 2 requires an extra module.
if sys.version_info[0] == 2:
    import mock
else:
    from unittest import mock

http_count = 0

def request_proxy(*args, **kwargs):
    http_count += 1

def reset_http():
    http_count = 0

def get_http_count():
    return http_count
    
requests.request = request_proxy


