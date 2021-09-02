import json

from aws_lambda_client.constants import LAMBDA_CLIENT_ENDPOINT_DATA_PATH, IS_PY_3

if IS_PY_3:
    import urllib.parse as urlparse
else:
    import urllib as urlparse

def parse_endpoints(raw):
    parsed = {}
    for partition in raw['partitions']:
        partition_name = partition.get('partition')
        partition_info = {}
        partition_info['defaults'] = partition.get('defaults')
        partition_info['dnsSuffix'] = partition.get('dnsSuffix')
        partition_info['regionRegex'] = partition.get('regionRegex')
        endpoints = {}
        raw_endpoints = partition.get('services').get('lambda').get('endpoints')
        for epn in raw_endpoints.keys():
            ep = raw_endpoints.get(epn)
            if ep.get('hostname') is None:
                continue
            cred_region = ep.get('credentialScope')
            endpoints[epn] = ep.get('hostname')
        partition_info['endpoints'] = endpoints
        parsed[partition_name] = partition_info
    return parsed

def format_api_params(**api_params):
    for key in api_params.keys():
        api_params[key] = urlparse.quote_plus(api_params[key])
    return api_params

class ApiCreator:
    def __init__(self):
        api_file = open(LAMBDA_CLIENT_ENDPOINT_DATA_PATH)
        self.endpoints_raw = json.load(api_file)
        self.endpoints = parse_endpoints(self.endpoints_raw)
    
    def get_host(self, partition, region):
        """Generates host from partition and region information

        Args:
            partition (str): partition info
            region (str): region info

        Returns:
            str: host
        """
        part = self.endpoints.get(partition)
        if part is None: return None

        hostname = part.get('endpoints').get(region)
        if hostname is None:
            dnsSuffix = part.get('dnsSuffix')
            host_template = part.get('defaults').get('hostname')
            hostname = host_template.format(service = 'lambda', region = region, dnsSuffix = dnsSuffix)
        return hostname


    def create_api(self, partition, region, api, query, protocol, api_params):
        """Creates complete api from given information

        Args:
            partition (str): partition info
            region (str): region info
            api (str): api endpoint template of the service function
            query (str): any query param, Empty dictionary if none
            protocol (str): protocol of request - http | https
            api_params (Dict): used to flatten the api endpoint provided, Empty dictionary if none
        Raises:
            Exception: api_params do not match with api template

        Returns:
            str: final url
        """
        host = self.get_host(partition, region)
        encoded_query = urlparse.urlencode(query)
        flat_api = None
        try:
            api_params = format_api_params(**api_params)
            flat_api = api.format(**api_params)
        except:
            raise Exception("Invalid API params")
        return "{}://{}{}?{}".format(protocol, host, flat_api, encoded_query)
    