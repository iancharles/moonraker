import boto3
import argparse
from subnetget import get_subnets
from amiget import get_amis
from sg_get import get_sgs

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-r', '--region', help="region of VPC")
parser.add_argument('--profile', help="AWS CLI Profile")
parser.add_argument('--public', help="Public or Private Subnet (Default is Private)")
args = parser.parse_args()

profile_nm = args.profile
region_nm = args.region
vpc = args.vpc
if args.public:
    public = True
else:
    public = False
file_name = 'moon-lander-4.yml'
# region has to come after vpc defined



intro = """
# account specific
"""


intro_file = open(file_name, 'w')
print("#Build Notes:", file=intro_file)
print("#------------", file=intro_file)
print(f"# for VPC: '{vpc}'\n", file=intro_file)
print(f"# vpc specific", file=intro_file)
print(f"region\t= {region_nm}", file=intro_file)
intro_file.close()


get_amis(region_nm, profile_nm, file_name)
get_subnets(vpc, region_nm, profile_nm, file_name, public)

az_raw = input("Specify availability zone (Optional) ") or "a"

# populate vpc-specific values in tfvars
intro_file = open(file_name, 'r+')
intro_file.read()
print(f"# instance specific", file=intro_file)
print(f"availability_zone\t= '{region_nm}{az_raw}'", file=intro_file)
intro_file.close()

get_sgs(vpc, region_nm, profile_nm, file_name)