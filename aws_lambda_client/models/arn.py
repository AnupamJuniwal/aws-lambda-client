class ARN:
    def __init__(self, arn):
        try:
            arn_prefix, partition, service, region, account, resource = arn.split(':', 5)
            self.partition = partition
            self.service = service
            self.region = region
            self.account = account
            self.resource = resource
        except:
            raise Exception(
                'Provided ARN: {} must be of the format: \
                    arn:partition:service:region:account:resource'.format(arn))


    def get_details(self):
        return {
            'partition': self.partition,
            'service': self.service,
            'region': self.region,
            'account': self.account,
            'resource': self.resource
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

    
    def __repr__(self):
        return 'arn:{}:{}:{}:{}:{}'.format(self.partition,
                                            self.service,
                                            self.region,
                                            self.account,
                                            self.resource
                                            )

