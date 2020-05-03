import boto3
import argparse
from subnetget import get_subnets
from amiget import get_amis
from sg_get import get_sgs
from add_block_device import add_block_device
from userdata_get import get_userdata


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', help="region of VPC")
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-o','--os', help="operating system")
parser.add_argument('-t','--type', help="instance type (size)")
parser.add_argument('-z','--zone', help="availability zone")
parser.add_argument('--hostname', help='name of instance')
parser.add_argument('--keyname', help='name of keypair')
parser.add_argument('--role', help='instance iam role')
parser.add_argument('--profile', help="AWS CLI Profile")
parser.add_argument('--network', help="Public or Private subnet")
args = parser.parse_args()

profile_nm = args.profile
region_nm = args.region
vpc = args.vpc
os = args.os
#temp
moon_node_nos = [1, 2, 3, 4, 5]

if args.network == 'public':
    public = True
else:
    public = False
hostname = args.hostname or "moon-server-default"
timezone = "America/Chicago"
user = "nv-admin"
file_tfvars = 'moon-lander-vars.tfvars'
file_main   = 'moon-lander-main.tf'

intro_file = open(file_tfvars, 'w')
print("#Build Notes:", file=intro_file)
print("#------------", file=intro_file)
print(f"# for VPC: '{vpc}'\n", file=intro_file)
print(f"# vpc specific", file=intro_file)
print(f'region\t= "{region_nm}"', file=intro_file)
intro_file.close()


get_amis(region_nm, profile_nm, file_tfvars)
get_subnets(vpc, region_nm, profile_nm, file_tfvars, public)
get_userdata(hostname, timezone, user)

az = args.zone or "a"

# populate vpc-specific values in tfvars
intro_file = open(file_tfvars, 'r+')
intro_file.read()
print(f"# instance specific", file=intro_file)
if args.hostname:
    print(f'hostname\t= "{args.hostname}"', file=intro_file)
if args.keyname:
    print(f'key_name\t= "{args.keyname}"', file=intro_file)
if args.role:
    print(f'iam_instance_profile\t= "{args.role}"', file=intro_file)
if args.type:
    print(f'instance_type\t= "{args.type}"', file=intro_file)
print(f'availability_zone\t= "{region_nm}{az}"', file=intro_file)
print(f'os\t\t= "{os}"', file=intro_file)
intro_file.close()

get_sgs(vpc, region_nm, profile_nm, file_tfvars)
add_block_device()

with open(file_main, 'r+') as file:
    file.read()
    print("}", file=file)
    if public:
        print('resource "aws_eip" "public_ip" {', file=file)
        print('\tvpc\t= true', file=file)
        print('\tinstance\t= aws_instance.moon_node.id', file=file)
        print("}", file=file)