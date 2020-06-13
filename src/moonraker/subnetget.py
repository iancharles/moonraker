import boto3
import collections


# Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
# subnet_dict['Mappings'] = collections.defaultdict(dict)
# subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)

# regions = ['us-east-1', 'us-east-2', 'us-west-2']

# NU LOOP
def get_subnets(profile_nm, region_nm, network_type="Private"):

    # Initial setup
    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
    var_file = "variables.tf"

    # Initiate the session
    ec2 = session.client('ec2')

    if network_type == 'Public':

        # Get public subnets
        public_subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*ublic*'
                    ]
                }
            ]
        )

        # print("Public Subnets")
        for subnet in public_subnets['Subnets']:
            subnet_dict[subnet['AvailabilityZone']] = subnet['SubnetId']

        output = "subnets_public = {"
        with open(var_file, 'r+') as f:
            f.read()
            f.write('\nvariable "subnets_public" {\n')
            f.write("\ttype    = map(string)\n")
            f.write("}\n")

    else:
        # Get private subnets
        private_subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*rivate*'
                    ]
                }
            ]
        )

        # print("Private Subnets")
        for subnet in private_subnets['Subnets']:
            subnet_dict[subnet['AvailabilityZone']] = subnet['SubnetId']

        output = "subnets_private = {"
        with open(var_file, 'r+') as f:
            f.read()
            f.write('\nvariable "subnets_private" {\n')
            f.write("\ttype    = map(string)\n")
            f.write("}\n")
   
    return subnet_dict
