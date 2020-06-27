def add_s3_logs(main_file):

    logs = input("Please enter a name for a new logs bucket: ")

    with open(main_file, 'r+') as f:
        f.read()
        f.write('\nresource "aws_s3_bucket" "log_bucket" {')
        f.write(f'\n\tbucket = "{logs}"')
        f.write(f'\n\tacl = "log-delivery-write"')
        f.write("\n}\n")

    return logs