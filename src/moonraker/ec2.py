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
    from json import dumps
    from pathlib import Path

    # from moonraker.amiget import get_amimap
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

    # if args.populate:
    #     pop_dict = populate(args.populate)
    # else:
    pop_dict = {}

    vars_list = ""

    # add generator later
    # instance_count = 1


    #Note: if updating allowed_os, also update linux_os (below) and user_dict in userdata.py
    allowed_os = [
        'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7', 'windows2016'
        ]
    linux_os = [
        'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7'
        ]
    allowed_regions = ['us-east-1', 'us-east-2', 'us-west-2', 'eu-central-1']
    
    # Generate filename values
    build_no = '{:%H%M%S}'.format(datetime.datetime.now())
    # Create tfvars file
    tfvars_file = Path("variables.tfvars")
    if not tfvars_file.is_file():
        Path(tfvars_file).touch()
    provider_file = Path("main.tf")
    if not provider_file.is_file():
        with open(resource_filename('moonraker', 'main.tf')) as f:
            filedata = f.read()
        with open(provider_file, 'w') as file:
            file.write(filedata)    
    # Create Main File
    main_file = f"ec2-{build_no}.tf"
    main_source_file = resource_filename('moonraker', 'ec2.tf')
    with open(main_source_file, 'r') as file :
        filedata = file.read()
    with open(main_file, 'w') as file:
        file.write(filedata)

    # Create generic variables file
    var_file = Path("variables.tf")
    if not var_file.is_file():
        with open(var_file, 'w') as file:
            file.write('\nvariable "profile" {}')
            file.write('\nvariable "region" {}')

    # Create EC2 variables file
    ec2_var_file = Path("ec2_variables.tf")
    if not ec2_var_file.is_file():
        var_source_file = resource_filename('moonraker', 'ec2_variables.tf')
        with open(var_source_file, 'r') as file :
            filedata = file.read()
        with open(ec2_var_file, 'w') as file:
            file.write(filedata)

    # Create data file
    data_file = Path("data.tf")
    if not data_file.is_file():
        data_source_file = resource_filename('moonraker', 'data.tf')
        with open(data_source_file, 'r') as file :
            filedata = file.read()
        with open(data_file, 'w') as file:
            file.write(filedata)

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
        selection = input("\nEnter instance type (size): ")
        value_dict["instance_type"] = selection

    # key pair
    if args.key:
        value_dict[f"key_name_{build_no}"] = args.key
    else:
        key = get_key_pairs(profile, region)
        if key:
            value_dict[f"key_name_{build_no}"] = key
        # else:
        #     print("Keypair is required")
        #     print("Exiting...")
        #     sys.exit(1)
    vars_list += (f'\nvariable "key_name_{build_no}"')
    vars_list += " {}\n"

    # GET AUTOMATIC VALUES

    # value_dict["ami"] = get_amimap(profile, region)


    # USER GEN OR PROMPTED
    if args.sgs:
        sgs_fmt = []
        for group in args.sgs:
            sgs_fmt.append(group)
        value_dict["security_groups"] = dumps(sgs_fmt)
    else:
        value_dict["security_groups"] = dumps(get_sgs(vpc, region, profile))

    # If OS is entered, use it. Else, create as parameter
    if args.os in allowed_os:
        os = args.os
        value_dict["os"] = os
    else:
        os = get_os(allowed_os)
        if os:
            value_dict["os"] = os
    
        # else:
        #     print("\nProceeding without OS")
        #     os_params = "OS:"
        #     os_params += "\n    Type: String"
        #     os_params += "\n    AllowedValues:"
        #     for os in allowed_os:
        #         if os not in linux_os:
        #             os_params += "\n      - " + os

        #     value_dict["# VAR_PARAM_OS"] = os_params
        #     value_dict["os"] = "!Ref OS"
        #     skipped_opts["os"] = "Enter as PARAMETER in CloudFormation (Windows Only)"


    # USER GEN - REQUIRED

    # Hostname (Required)
    if args.hostname:
        hn = args.hostname
    else:
        print("\nHOSTNAME")
        print("========")
        hn = input("Please enter hostname: ")

    vars_list += (f'\nvariable "hostname_{build_no}"')
    vars_list += " {}\n"
    value_dict[f"hostname_{build_no}"] = hn

    # USER GEN - OPTIONAL

    # Availability Zone
    if args.zone:
        az = args.zone
    else:
        az = "a"
    vars_list += (f'variable "availability_zone_{build_no}"')
    vars_list += " {}\n"
    value_dict[f"availability_zone_{build_no}"] = region + az



    # If network type is entered, use it. Else, create as parameter
    if args.network and args.network.lower() == 'public':
        # value_dict["network"] = "Public"
        value_dict["subnets_public"] = get_subnets(main_file, profile, region, "Public")
    else:
        # value_dict["network"] = "Private"
        value_dict["subnets_private"] = get_subnets(main_file, profile, region, "Private")

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
        # Get values to populate user_data file
        if args.timezone:
            # value_dict["# timedatectl"] = "timedatectl"
            tz = args.timezone
        elif pop_dict and pop_dict["timezone"]:
            tz = pop_dict["timezone"]
        else:
            tz = "UTC"
            skipped_opts["timezone"] = tz

        # Default system user - maybe only necessary for linux
        if args.user:
            user = args.user
        elif pop_dict and pop_dict['user']:
            user = pop_dict['user']
        else:
            print("\nUSERNAME")
            print("========")
            print("Default username is required for Linux instances:")
            user = input("Please enter user: ")

        add_user_data(os, hn, tz, user, build_no)

    # Format root EBS vol properly
    # if os in ['amazonlinux2']:
    #     value_dict["VAR_ROOT_VOL_NAME"] = "/dev/xvda"
    # else:
    #     value_dict["VAR_ROOT_VOL_NAME"] = "/dev/sda1"

    # Override root volume size if necessary
    if args.root:
        # root_vol_size = str(args.root)
        value_dict["root_vol_size"] = str(args.root)

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
            disk_params += "\tebs_block_device {\n"
            disk_params += f'\t\tdevice_name = "{block_device_pool[counter]}"\n'
            disk_params += "\t\tencrypted = true\n"
            disk_params += f"\t\tvolume_size = {disk}\n"
            disk_params += "\t}\n"
            
            counter += 1
                
        # value_dict["# VAR_PARAM_DISKS"] = disk_params
        # Read in the file
        with open(main_file, 'r') as file :
            filedata = file.read()
        # Replace the target string    
            filedata = filedata.replace('#VAR_EBS', disk_params)
        # Write the file out again
        with open(main_file, 'w') as file:
            file.write(filedata)
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

## FINALIZE
    # Finalize instance main file
    with open(main_file, 'r') as file :
        filedata = file.read()
    # Replace the target string    
        filedata = filedata.replace('BUILD_NO', build_no)
        filedata = filedata.replace("VAR_OS", os)
    # Write the file out again
    with open(main_file, 'w') as file:
        file.write(filedata)  

    # Finalize variables file
    with open(ec2_var_file, 'r') as file :
        filedata = file.read()
        # filedata = filedata.replace("BUILD_NO", build_no)
        filedata += vars_list
    with open(ec2_var_file, 'w') as file:
        file.write(filedata)

    # Finalize TFVARS file
    with open(tfvars_file, 'r+') as f:
        existing = f.read()
        for key, value in value_dict.items():
            if key not in existing:
                if key == "security_groups":
                    f.write(f"{key} = {value}")
                    f.write("\n")
                elif isinstance(value,dict):
                    f.write(f"{key}")
                    f.write(" = {\n")
                    for k, v in value.items():
                        f.write(f'\t{k} = "{v}"\n')
                    f.write("}\n")
                else:
                    f.write(f'{key} = "{value}"\n')

    # print(value_dict)

    # Print final output
    print(f"\nYou created this template with the profile {profile}")
    print("Please make sure this is for the correct profile\n")
    print(f"Your moonraker TF File is now available at {main_file}\n")
    print(f"Your moonraker variables now available at {tfvars_file}\n")
