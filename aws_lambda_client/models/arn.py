import re

ARN_REGEX = "(arn:(aws[a-zA-Z-]*):lambda:)([a-z]{2}(-gov)?-[a-z]+-\d{1}:)(\d{12}:)(function:)([a-zA-Z0-9-_\.]+)$"
matcher = re.compile(ARN_REGEX)

INVALID_ARN_ERROR_MSG_TEMPLATE = 'Provided ARN: {} must be of the format: arn:partition:service:region:account:resource:resource_name'
class ARN:
    def __init__(self, arn):
        if matcher.match(arn) is None:
            raise Exception(INVALID_ARN_ERROR_MSG_TEMPLATE.format(arn))

        arn_prefix, partition, service, region, account, resource, resource_name = arn.split(':', 6)
        self.partition = partition
        self.service = service
        self.region = region
        self.account = account
        self.resource = resource
        self.resource_name = resource_name


    def get_details(self):
        return {
            'partition': self.partition,
            'service': self.service,
            'region': self.region,
            'account': self.account,
            'resource': self.resource,
            'resource_name': self.resource_name
        }


    def get_partition(self):
        return self.partition

    
    def get_service(self):
        return self.service
    
    def get_region(self):
        return self.region


    def get_account(self):
        return self.account


    def get_resource(self):
        return self.resource

    
    def get_resource_name(self):
        return self.resource_name
    
    def __repr__(self):
        return 'arn:{}:{}:{}:{}:{}:{}'.format(self.partition,
                                            self.service,
                                            self.region,
                                            self.account,
                                            self.resource,
                                            self.resource_name
                                            )

