block_device_pool = ['/dev/xvdb', '/dev/xvdc', '/dev/xvdd', '/dev/xvde' ]

def add_block_device():
    counter = 0
    while input("Standard root volume is 64 GB. Add block davice [y/N]? ") == 'y':
        size = input("Please specify size of volume: ")
        with open('moon-lander-main.tf', 'r+') as file:
            file.read()
            print("#   27 - Optional - EBS Block Device", file=file)
            print("\tebs_block_device {", file=file)
            print(f'\t\tdevice_name = "{block_device_pool[counter]}"', file=file)
            counter += 1
            print("\t\tencrypted   = true", file=file)
            print(f"\t\tvolume_size = {size}", file=file)
            print("\t}", file=file)
            print("}", file=file)

