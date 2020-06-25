import boto3

def add_key_pair(profile_nm, region_nm, keypair_name):

    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

    ec2 = session.client('ec2')
    outfile = f"{keypair_name}.pem"

    keypair = ec2.create_key_pair(KeyName=keypair_name)


    with open(outfile, 'w') as f:
        f.write(keypair['KeyMaterial'])

# add_key_pair("default", "us-west-2", "moon-gen-3")

    