#!/usr/bin/env python3

hostname    = "moon-node-5"
timezone    = "America/Chicago"
user        = "nv-admin"


userdata_raw = """
#! /bin/bash
sudo hostnamectl set-hostname VAR_HOSTNAME
echo VAR_TIMEZONE > /home/ubuntu/timezone.txt
sudo apt-get update
sudo apt-get install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
echo "Started" > /home/ubuntu/3.txt
echo "<h1>Deployed via Terraform</h1>" | sudo tee /var/www/html/index.html
sudo echo VAR_USER > /home/ubuntu/user.txt
sudo reboot
"""

print("RAW:\n")
print(userdata_raw)

userdata_host = userdata_raw.replace("VAR_HOSTNAME", hostname)
userdata_tz = userdata_host.replace("VAR_TIMEZONE", timezone)
userdata_final = userdata_tz.replace("VAR_USER", user)


print(userdata_host)
with open("user_data.sh", "w") as file:
    file.write(userdata_final)



