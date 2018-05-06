

class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    def create_key_pair(self, key_name):
        print('Creating a key pair with name ' + key_name)
        return self._client.create_key_pair(KeyName=key_name)

    def create_security_group(self, group_name, description, vpc_id):
        print('Creating a Security Group with name ' + group_name + ' for VPC ' + vpc_id)
        return self._client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )

    def add_inbound_rule_to_sg(self, security_group_id):
        print('Adding inbound public access to Security Group ' + security_group_id)
        self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

    def launch_ec2_instance(self, image_id, key_name, min_count, max_count, security_group_id, subnet_id, user_data):
        print('Launching EC2 Instance(s) within Subnet ' + subnet_id)
        return self._client.run_instances(
            ImageId=image_id,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType='t2.micro',
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            UserData=user_data
        )

    def describe_ec2_instances(self):
        print('Describing EC2 Instances...')
        return self._client.describe_instances()

    def modify_ec2_instance(self, instance_id):
        print('Modifying EC2 Instance ' + instance_id)
        return self._client.modify_instance_attribute(
            InstanceId=instance_id,
            DisableApiTermination={'Value': True}
        )

    def stop_instance(self, instance_id):
        print('Stopping EC2 Instance ' + instance_id)
        return self._client.stop_instances(
            InstanceIds=[instance_id]
        )

    def start_instance(self, instance_id):
        print('Starting EC2 Instance ' + instance_id)
        return self._client.start_instances(
            InstanceIds=[instance_id]
        )

    def terminate_instance(self, instance_id):
        print('Terminating EC2 Instance ' + instance_id)
        return self._client.terminate_instances(
            InstanceIds=[instance_id]
        )