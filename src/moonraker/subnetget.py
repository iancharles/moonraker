import boto3
import collections

# Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
# subnet_dict['Mappings'] = collections.defaultdict(dict)
# subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)

# NU LOOP
def get_subnets(main_file, profile_nm, region_nm, network_type="Private"):

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

        public_values = """variable "subnets_public" {
    type    = map(string)
}"""

        with open(var_file, 'r') as file :
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('#VAR_PUBLIC', public_values)
        # Write the file out again
        with open(var_file, 'w') as file:
            file.write(filedata)

        with open(main_file, 'r') as file :
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace("subnets_private", "subnets_public")
        # Write the file out again
        with open(main_file, 'w') as file:
            file.write(filedata)
            file.write('\nresource "aws_eip" "public_ip-BUILD_NO" {')
            file.write("\n\tvpc\t= true")
            file.write("\n\tinstance\t= aws_instance.ec2-BUILD_NO.id")
            file.write("\n}")

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

        private_values = """variable "subnets_private" {
    type    = map(string)
}"""

        with open(var_file, 'r') as file :
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('#VAR_PRIVATE', private_values)
        # Write the file out again
        with open(var_file, 'w') as file:
            file.write(filedata)
        
        # with open(var_file, 'r+') as f:
        #     f.read()
        #     f.write('\nvariable "subnets_private" {\n')
        #     f.write("\ttype    = map(string)\n")
        #     f.write("}\n")
   
    return subnet_dict
