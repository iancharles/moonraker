import boto3
import collections
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-r', '--region', help="region of VPC")
args = parser.parse_args()

# Temp variables, replace with logic
profile_nm = "default"


# temp variable, replace with argarse later
vpc = args.vpc

# region has to come after vpc defined
region_nm = args.region

session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
ec2 = session.client('ec2')

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


print("subnets_public = {")



# # Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
subnet_dict['Mappings'] = collections.defaultdict(dict)
subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)




for subnet in public_subnets['Subnets']:
    subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Public"] = subnet['SubnetId']

# # The final printer
for key in subnet_dict:
    # print(f"{key}:")
    for key_two in subnet_dict[key]:
        # print(f"  {key_two}:")
        for key_three in subnet_dict[key][key_two]:
            # print(f"    {key_three}:")
            for key_four in subnet_dict[key][key_two][key_three]:
                print(f"\t'{key_three}'\t= '{subnet_dict[key][key_two][key_three][key_four]}'")
print("}")

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


print("subnets_private = {")



# # Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
subnet_dict['Mappings'] = collections.defaultdict(dict)
subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)




for subnet in private_subnets['Subnets']:
    subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Private"] = subnet['SubnetId']

# # The final printer
for key in subnet_dict:
    # print(f"{key}:")
    for key_two in subnet_dict[key]:
        # print(f"  {key_two}:")
        for key_three in subnet_dict[key][key_two]:
            # print(f"    {key_three}:")
            for key_four in subnet_dict[key][key_two][key_three]:
                print(f"\t'{key_three}'\t= '{subnet_dict[key][key_two][key_three][key_four]}'")
print("}")