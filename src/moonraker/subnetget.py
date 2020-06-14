import boto3
import collections
from pkg_resources import resource_filename

# Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
# subnet_dict['Mappings'] = collections.defaultdict(dict)
# subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)

# NU LOOP
def get_subnets(main_file, profile_nm, region_nm, network_type="Private"):

    # Initial setup
    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
    main_source_file = resource_filename('moonraker', 'ec2.tf')
    # main_source_file = "main.tf"
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

        with open(var_file, 'r+') as f:
            f.read()
            f.write('\nvariable "subnets_public" {\n')
            f.write("\ttype    = map(string)\n")
            f.write("\n}\n")
            
        with open(main_source_file, 'r') as f:
            build = f.read()
            build = build.replace("subnets_private", "subnets_public")
        
        with open(main_file, 'w') as f:
            f.write(build)
            f.write('\nresource "aws_eip" "public_ip" {')
            f.write("\n\tvpc\t= true")
            f.write("\n\tinstance\t= aws_instance.moon_node.id")
            f.write("\n}")

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

        with open(var_file, 'r+') as f:
            f.read()
            f.write('\nvariable "subnets_private" {\n')
            f.write("\ttype    = map(string)\n")
            f.write("}\n")
   
    return subnet_dict
