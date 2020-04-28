import boto3
import argparse
from subnetget import get_subnets
from amiget import get_amis
from sg_get import get_sgs
from add_block_device import add_block_device

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', help="region of VPC")
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-o','--os', help="operating system")
parser.add_argument('--hostname', help='name of instance')
parser.add_argument('--profile', help="AWS CLI Profile")
parser.add_argument('--network', help="Public or Private subnet")
args = parser.parse_args()

profile_nm = args.profile
region_nm = args.region
vpc = args.vpc
os = args.os

if args.network == 'public':
    public = True
else:
    public = False
file_tfvars = 'moon-lander-vars.tfvars'
file_main   = 'moon-lander-main.tfvars'

intro_file = open(file_tfvars, 'w')
print("#Build Notes:", file=intro_file)
print("#------------", file=intro_file)
print(f"# for VPC: '{vpc}'\n", file=intro_file)
print(f"# vpc specific", file=intro_file)
print(f'region\t= "{region_nm}"', file=intro_file)
intro_file.close()


get_amis(region_nm, profile_nm, file_tfvars)
get_subnets(vpc, region_nm, profile_nm, file_tfvars, public)

az_raw = input("Specify availability zone (Optional) ") or "a"

# populate vpc-specific values in tfvars
intro_file = open(file_tfvars, 'r+')
intro_file.read()
print(f"# instance specific", file=intro_file)
if args.hostname:
    print(f'hostname\t= "{args.hostname}"', file=intro_file)
print(f'availability_zone\t= "{region_nm}{az_raw}"', file=intro_file)
print(f'os\t\t= "{os}"', file=intro_file)
intro_file.close()

get_sgs(vpc, region_nm, profile_nm, file_tfvars)
add_block_device()