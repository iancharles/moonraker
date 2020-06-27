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

    from moonraker.profileget import get_profile
    from moonraker.s3_logs_add import add_s3_logs


    # ADD ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help="Name of bucket", required=True)
    parser.add_argument('--region', help='region of build', required=True)
    parser.add_argument('--profile', help="AWS CLI Profile")
    parser.add_argument('--logs', help="Bucket to store access logs")

    args = parser.parse_args()

    value_dict = {}

    # name
    name = args.name
    # value_dict["name"] = name

    # Create tfvars file
    tfvars_file = Path("variables.tfvars")
    if not tfvars_file.is_file():
        Path(tfvars_file).touch()

    # Create Main File
    main_file = f"s3-{name}.tf"
    main_source_file = resource_filename('moonraker', 's3.tf')
    with open(main_source_file, 'r') as file :
        filedata = file.read()
    with open(main_file, 'w') as file:
        file.write(filedata)
 
    # Create provider file
    provider_file = Path("main.tf")
    if not provider_file.is_file():
        with open(resource_filename('moonraker', 'main.tf')) as f:
            filedata = f.read()
        with open(provider_file, 'w') as file:
            file.write(filedata)   

    # Create variables file
    var_file = Path("variables.tf")
    if not var_file.is_file():
        with open(var_file, 'w') as file:
            file.write('\nvariable "profile" {}')
            file.write('\nvariable "region" {}')

    # region
    region = args.region
    value_dict["region"] = region
    # profile
    if args.profile:
        profile = args.profile
    elif 'AWS_PROFILE' in environ:
        profile = environ['AWS_PROFILE']
    else:
        profile = get_profile()
        print("\n")
    value_dict["profile"] = profile
    # logs
    if args.logs:
        logs = args.logs
    else:
        logs = add_s3_logs(main_file)


## FINALIZE
    # Finalize instance main file
    with open(main_file, 'r') as file :
        filedata = file.read()
    # Replace the target string    
        filedata = filedata.replace('VAR_NAME', name)
        filedata = filedata.replace("VAR_LOGS", logs)
    # Write the file out again
    with open(main_file, 'w') as file:
        file.write(filedata)  

    # Finalize TFVARS file
    with open(tfvars_file, 'r+') as f:
        existing = f.read()
        for key, value in value_dict.items():
            if key not in existing:
                f.write(f'\n{key} = "{value}"\n')



    # print(value_dict)

    # Print final output
    print(f"\nYou created this template with the profile {profile}")
    print("Please make sure this is for the correct profile\n")
    print(f"Your moonraker TF File is now available at {main_file}\n")


main()