import boto3
import collections

def get_subnets(vpc, region_nm, profile_nm, file_name, public):

    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
    ec2 = session.client('ec2')


    with open(file_name, 'r+') as file:
        file.read()

        # PRIVATE SUBNETS

        print("subnets_private = {", file=file)

        private_subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc
                    ]
                },
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*rivate*'
                    ]
                }
            ]
        )




        # # Initial structure and defaults
        subnet_dict = collections.defaultdict(dict)
        subnet_dict['Mappings'] = collections.defaultdict(dict)
        subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)




        for subnet in private_subnets['Subnets']:
            subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Private"] = subnet['SubnetId']

        # # The final printer
        for key in subnet_dict:
            for key_two in subnet_dict[key]:
                for key_three in subnet_dict[key][key_two]:
                    for key_four in subnet_dict[key][key_two][key_three]:
                        print(f"\t'{key_three}'\t= '{subnet_dict[key][key_two][key_three][key_four]}'", file=file)
        print("}", file=file)

        # PUBLIC SUBNETS
        if public:

            print("subnets_public = {", file=file)

            public_subnets = ec2.describe_subnets(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpc
                        ]
                    },
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            '*ublic*'
                        ]
                    }
                ]
            )


            # # Initial structure and defaults
            subnet_dict = collections.defaultdict(dict)
            subnet_dict['Mappings'] = collections.defaultdict(dict)
            subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)




            for subnet in public_subnets['Subnets']:
                subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Public"] = subnet['SubnetId']

            # # The final printer
            for key in subnet_dict:
                for key_two in subnet_dict[key]:
                    for key_three in subnet_dict[key][key_two]:
                        for key_four in subnet_dict[key][key_two][key_three]:
                            print(f"\t'{key_three}'\t= '{subnet_dict[key][key_two][key_three][key_four]}'", file=file)
            print("}", file=file)