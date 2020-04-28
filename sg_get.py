import boto3
import collections
from json import dumps

def get_sgs(vpc, region_nm, profile_nm, file_name):

    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
    ec2 = session.client('ec2')


    with open(file_name, 'r+') as file:
        file.read()

        available_sgs = ec2.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc
                    ]
                }
            ]
        )

        # print(available_sgs)


        # # Initial structure and defaults
        subnet_dict = collections.defaultdict(dict)
        subnet_dict['SecurityGroups'] = collections.defaultdict(dict)
      
        selected_security_groups = []
        counter = 0
        display = input("Would you like to see the available security groups first? [y/N] ").lower()
        if display == 'y':
            print(f"\nAvailable Security Groups for {vpc}:\n")
            for item in available_sgs['SecurityGroups']:
                print(f"{item['GroupName']} - {item['Description']}")
            print("\n#------------------#\n")
        print("Choose from Available Security Groups:\n")
        for item in available_sgs['SecurityGroups']:
            if input(f"{item['GroupName']} - {item['Description']} [y/N]: ").lower() == 'y':
                selected_security_groups.append(item["GroupId"])
        
        security_groups = dumps(selected_security_groups)

        print("")
        print(f'security_groups\t= {security_groups}', file=file)