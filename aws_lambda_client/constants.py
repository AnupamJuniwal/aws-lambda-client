import os
import sys

LIB_ROOT_PATH = os.path.dirname(__file__)
LAMBDA_CLIENT_DATA_PATH = os.path.join(LIB_ROOT_PATH, 'data')
LAMBDA_CLIENT_ENDPOINT_DATA_PATH = os.path.join(LAMBDA_CLIENT_DATA_PATH, 'endpoints.json')
IS_PY_3 = sys.version_info > (3, 0)