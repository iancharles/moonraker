import boto3
import collections
# from datetime import datetime
import datetime
from dateutil import parser

def get_amis(region_nm, profile_nm, file_name):





    # Initial setup
    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

    # Initiate the session
    ec2 = session.client('ec2')

    with open(file_name, 'r+') as file:
        file.read()

        # Initial structure and defaults
        subnet_dict = collections.defaultdict(dict)
        subnet_dict['Mappings'] = collections.defaultdict(dict)
        subnet_dict['Mappings']['AMIMap'] = collections.defaultdict(dict)

        # Get all AMIs
        all_amis = ec2.describe_images(
            Owners=[
                'self',
            ]
        )

        # Format dates and order main dict by date
        for image in all_amis['Images']:
            image['CreationDate'] = image['CreationDate'][:19]
            # image['CreationDate'] = datetime.datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S")

        all_amis['Images'].sort(key= lambda image: datetime.datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S"))

        count = 0

        # Create empty OS dicts
        ubuntu16_amis = [""]
        ubuntu18_amis = [""]
        suse_amis = [""]

        # Sort images into dicts by OS
        for image in all_amis['Images']:
            if 'ubuntu' in image['Name'].lower() and '16' in image['Name'].lower():
                ubuntu16_amis.append(image)
            elif 'ubuntu' in image['Name'].lower() and '18' in image['Name'].lower():
                ubuntu18_amis.append(image)
            elif 'suse' in image['Name'].lower():
                suse_amis.append(image)    

        ubuntu16 = ubuntu16_amis[-1]
        ubuntu18 = ubuntu18_amis[-1]
        suse = suse_amis[-1]


        try:
            # print(f"{ubuntu16['Name']} - {ubuntu16['ImageId']} - {ubuntu16['CreationDate']}")
            subnet_dict['Mappings']['AMIMap'][region_nm]['ubuntu16'] = ubuntu16['ImageId']
        except:
            pass

        try:
            # print(f"{ubuntu18['Name']} - {ubuntu18['ImageId']} - {ubuntu18['CreationDate']}")
            subnet_dict['Mappings']['AMIMap'][region_nm]['ubuntu18'] = ubuntu18['ImageId']
        except:
            pass
        try:
            # print(f"{suse['Name']} - {suse['ImageId']} - {suse['CreationDate']}")
            subnet_dict['Mappings']['AMIMap'][region_nm]['suse'] = suse['ImageId']
        except:
            pass

        print("ami = {", file=file)
        # The final printer
        for key in subnet_dict:
            for key_two in subnet_dict[key]:
                for key_three in subnet_dict[key][key_two]:
                    for key_four in subnet_dict[key][key_two][key_three]:
                        print(f'\t"{key_four}"\t=  "{subnet_dict[key][key_two][key_three][key_four]}"', file=file)
        print("}", file=file)