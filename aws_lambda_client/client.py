from aws_lambda_client.models.arn import ARN
from aws_lambda_client.api_creator import ApiCreator
from aws_lambda_client.requester import AWSLambdaRequester

class LambdaClient:
    """Creates a lambda client.
        Can take credentials for custom access.
        kwargs:
            AWS_SECRET_ACCESS_KEY (str)
            AWS_ACCESS_KEY_ID (str)
            AWS_SESSION_TOKEN (str)
            AWS_DEFAULT_REGION (str)
    """
    def __init__(self, **creds):
        secret = creds.get('AWS_SECRET_ACCESS_KEY')
        access_key = creds.get('AWS_ACCESS_KEY_ID')
        session_token = creds.get('AWS_SESSION_TOKEN')
        region = creds.get('AWS_DEFAULT_REGION')

        self.api_creator = ApiCreator()
        self.requester = AWSLambdaRequester(secret, access_key, session_token, region)

    def invoke(self, **info):
        """Invokes a lambda function.
            kwargs:
                arn (str) : fully qualified ARN of function to be invoked (without qualifier)
                payload (Dict) : JSON event
                version (str) :  version or alias to invoke a published version of the function.
                invocation_type (str) : RequestResponse | Event | DryRun
                log_type (str) : Tail | None
        Raises:
            Exception: if any configuration error occurs

        Returns:
            response: response object for corresponding http request
        """
        arn = info.get('arn')
        payload = info.get('payload')
        qualifier = info.get('version')
        invocation_type = info.get('invocation_type')
        log_type = info.get('log_type')
        if arn is None:
            raise Exception("Empty ARN")
        if payload is None:
            raise Exception("Empty Payload")
        if qualifier is None:
            raise Exception("Empty Version")

        arn = ARN(arn)
        partition = arn.get_partition()
        region = arn.get_region()
        host = self.api_creator.get_host(partition, region)
        url = self.api_creator.create_api(partition,
            region,
            "/2015-03-31/functions/{FunctionName}/invocations",
            {"Qualifier": qualifier},
            "https",
            {"FunctionName": str(arn)}
        )
        headers = {
            "Content-Type": "application/json",
            'X-Amz-Invocation-Type': invocation_type,
            'X-Amz-Log-Type': log_type
        }
        return self.requester.call('POST', url, host, headers, payload)


    def list_alias(self, **info):
        """list all aliases of a lambda function.
            kwargs:
                arn (str) : fully qualified ARN of function to be invoked (without qualifier)
        Raises:
            Exception: if any configuration error occurs

        Returns:
            response: response object for corresponding http request
        """
        arn = info.get('arn')
        if arn is None:
            raise Exception("Empty ARN")
        
        arn = ARN(arn)
        partition = arn.get_partition()
        region = arn.get_region()
        host = self.api_creator.get_host(partition, region)
        url = self.api_creator.create_api(partition,
            region,
            "/2015-03-31/functions/{FunctionName}/aliases",
            {},
            "https",
            {"FunctionName": str(arn)}
        )
        headers = {}
        return self.requester.call('GET', url, host, headers, '')
