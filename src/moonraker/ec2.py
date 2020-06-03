###############
# moonraker #
###############

def main():
    import boto3
    import argparse
    import sys
    import datetime
    from os import environ
    from pkg_resources import resource_filename


    from moonraker.amiget import get_amimap
    from moonraker.iam_role_get import get_iam_role
    from moonraker.keypairget import get_key_pairs
    from moonraker.os_get import get_os
    # from moonraker.populate import populate
    from moonraker.profileget import get_profile
    from moonraker.regionget import get_region
    # from size_get import get_sizes
    from moonraker.subnetget import get_subnets
    from moonraker.sg_get import get_sgs
    from moonraker.userdata import add_user_data
    from moonraker.vpcget import get_vpc
    from moonraker.vpc_sanitize import sanitize_vpc


    # ADD ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc', help="VPC (VPC-id or friendly name)")
    parser.add_argument('-o','--os', help="operating system")
    parser.add_argument('-t','--type', help="instance type (size)")
    parser.add_argument('-z','--zone', help="availability zone")
    parser.add_argument('--hostname', help='name of instance')
    parser.add_argument('-k', '--key', help='name of keypair')
    parser.add_argument('--role', help='instance iam role')
    parser.add_argument('--region', help='region of build')
    parser.add_argument('--profile', help="AWS CLI Profile")
    parser.add_argument('--network', help="Public or Private subnet")
    parser.add_argument('--timezone', help='Timezone of instance')
    parser.add_argument('--user', help='default user on instance')
    parser.add_argument('--populate', help='enter location of file')
    parser.add_argument('--root', help='Use to override default root volume size of 64 GB')
    parser.add_argument('-d', '--disks', nargs='+', help='add data volumes', default=None)
    parser.add_argument('--sgs', nargs='+', help='add security groups', default=None)
    args = parser.parse_args()

    value_dict = {}
    skipped_opts = {}

    if args.populate:
        pop_dict = populate(args.populate)
    else:
        pop_dict = {}


    #Note: if updating allowed_os, also update linux_os (below) and user_dict in userdata.py
    allowed_os = [
        'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7', 'windows2016'
        ]
    linux_os = [
        'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7'
        ]
    allowed_regions = ['us-east-1', 'us-east-2', 'us-west-2', 'eu-central-1']

    source_file = resource_filename('moonraker', 'ec2.yml')
    # source_file = "ec2.yml"
    build_file = '{:%Y%m%d-%H%M}'.format(datetime.datetime.now()) + ".tf"

    if args.profile:
        profile = args.profile
    elif 'AWS_PROFILE' in environ:
        profile = environ['AWS_PROFILE']
    else:
        profile = get_profile()
        print("\n")
    value_dict["profile"] = profile

    # GET VPC and REGION - REQUIRED!
    if args.region:
        region = args.region
        if args.vpc:
            vpc = sanitize_vpc(profile, args.vpc, [region])
        else:
            vpc = get_vpc(profile, region)
    else:
        if args.vpc:
            vpc = sanitize_vpc(profile, args.vpc, allowed_regions)
            region = get_region(profile, args.vpc, allowed_regions)
        else:
            print("VPC or Region is required for all builds.")
            print("Specify a region with the '--region' flag, or VPC with '--vpc'")
            print("Exiting...")
            sys.exit(1)

    value_dict["region"] = region


    # USER GEN - REQUIRED

    # Instance type
    if args.type:
        value_dict["instance_type"] = args.type
    else:
        print("\nTYPE")
        print("====")
        print("Instance type is required.")
        # TO DO: Add instance type generator
        # print("You can choose to see a list of types before entering a value.")
        # size_choices = get_sizes(profile, region)
        # if input("See available types first? [y/N] ").lower() == "y":
            # print(size_choices)
        selection = input("\nEnter instance type (size): ")
        value_dict["instance_type"] = selection
        # if selection in size_choices:
        #     value_dict["VAR_INSTANCE_TYPE"] = selection
        # else:
        #     print("That was not a valid choice. Exiting...")
        #     sys.exit(1)

    # key pair
    if args.key:
        value_dict["key_name"] = args.key
    else:
        key = get_key_pairs(profile, region)
        if key:
            value_dict["key_name"] = key
        else:
            print("Keypair is required")
            print("Exiting...")
            sys.exit(1)


    # GET AUTOMATIC VALUES

    value_dict["ami"] = get_amimap(profile, region)

    value_dict["# VAR_SUBNET_MAP"] = get_subnets(profile, allowed_regions)



    # USER GEN OR PROMPTED
    if args.sgs:
        sgs_fmt = ""
        for group in args.sgs:
            sgs_fmt += "\n        - " + group
        value_dict["security_groups"] = sgs_fmt
    else:
        value_dict["security_groups"] = get_sgs(vpc, region, profile)

    # If OS is entered, use it. Else, create as parameter
    if args.os in allowed_os:
        os = args.os
        value_dict["os"] = os
    else:
        os = get_os(allowed_os)
        if os:
            value_dict["os"] = os
        else:
            print("\nProceeding without OS")
            os_params = "OS:"
            os_params += "\n    Type: String"
            os_params += "\n    AllowedValues:"
            for os in allowed_os:
                if os not in linux_os:
                    os_params += "\n      - " + os

            value_dict["# VAR_PARAM_OS"] = os_params
            value_dict["os"] = "!Ref OS"
            skipped_opts["os"] = "Enter as PARAMETER in CloudFormation (Windows Only)"



    # USER GEN - OPTIONAL

    # Hostname (maybe this should be required)
    if args.hostname:
        hn = args.hostname
    else:
        print("\nHOSTNAME")
        print("========")
        hn = input("Please enter hostname: ")

    value_dict["hostname"] = hn

    # Availability Zone
    if args.zone:
        az = args.zone
    else:
        az = "a"

    value_dict["availability_zone"] = region + az



    # If network type is entered, use it. Else, create as parameter
    if args.network and args.network.lower() == 'public':
        value_dict["VAR_NETWORK"] = "Public"
    else:
        value_dict["VAR_NETWORK"] = "Private"

    # If role is entered, use it. Else, create as parameter
    if args.role:
        value_dict["iam_instance_profile"] = args.role
    else:
        value_dict["iam_instance_profile"] = get_iam_role(profile, region)
    if not value_dict["iam_instance_profile"]:
        role_params = "IamInstanceProfile:"
        role_params += "\n    Type: String"
        role_params += "\n    Default: EC2-S3-Access"

        value_dict["# VAR_PARAM_ROLE"] = role_params
        value_dict["iam_instance_profile"] = "!Ref IamInstanceProfile"
        skipped_opts["role"] = "Enter as PARAMETER in CloudFormation"



    # Write user_data
    if os in linux_os:

        if args.timezone:
            # value_dict["# timedatectl"] = "timedatectl"
            tz = args.timezone
        elif pop_dict and pop_dict["timezone"]:
            tz = pop_dict["timezone"]
        else:
            tz = "UTC"
            skipped_opts["timezone"] = tz

        value_dict["VAR_TIMEZONE"] = tz

        # Default system user - maybe only necessary for linux
        if args.user:
            user = args.user
            value_dict["VAR_USER"] = user
        elif pop_dict and pop_dict['user']:
            user = pop_dict['user']
        else:
            print("\nUSERNAME")
            print("========")
            print("Default username is required for Linux instances:")
            user = input("Please enter user: ")

        value_dict["# VAR_UD"] = add_user_data(
            os, hn, tz, user)

    # Format root EBS vol properly
    if os in ['amazonlinux2']:
        value_dict["VAR_ROOT_VOL_NAME"] = "/dev/xvda"
    else:
        value_dict["VAR_ROOT_VOL_NAME"] = "/dev/sda1"

    # Override root volume size if necessary
    if args.root:
        root_vol_size = str(args.root)
    else:
        root_vol_size = str(64)

    value_dict["VAR_ROOT_VOL_SIZE"] = root_vol_size

    # If disks are entered, add them. Else, ignore
    if args.disks:
        disks = args.disks
        block_device_pool = [
            '/dev/xvdb', '/dev/xvdc', '/dev/xvdd', \
            '/dev/xvde', '/dev/xvdf', '/dev/xvdg', '/dev/xvdh' \
            '/dev/xvdi', '/dev/xvdj', '/dev/xvdk', '/dev/xvdl'
            ]
        counter = 0
        disk_params = ""

        for disk in disks:
            disk_params += "        - DeviceName: " + block_device_pool[counter] + "\n"
            disk_params += "          Ebs:" + "\n"
            disk_params += "            VolumeSize: " + disk + "\n"
            disk_params += "            Encrypted: true"
            counter += 1
            if counter < len(disks):
                disk_params += "\n"
                
        value_dict["# VAR_PARAM_DISKS"] = disk_params
    else:
        skipped_opts["Addt'l EBS Volumes"] = "None"




    ## CHECK VALUES


    if skipped_opts:
        print("\n#-------------#\n")
        print("You skipped the following optional parameters.")
        print("They are not required, but please confirm you did not omit them by accident")
        print("Default values shown when available\n")
        for key, value in skipped_opts.items():
            print(f"{key}: {value}")
        print("\n#-------------#\n")




    # with open(source_file, 'r') as f:
    #     build = f.read()
    #     for key, value in value_dict.items():
    #         build = build.replace(key, value)
        
    with open(build_file, 'w') as f:
        # f.write(build)
        for key, value in value_dict.items():
            f.write(f"{key}: {value}\n")

    # print(value_dict)

    print(f"\nYou created this template with the profile {profile}")
    print("Please make sure this is for the correct profile\n")
    print(f"Your moonraker TF File is now available at {build_file}\n")
