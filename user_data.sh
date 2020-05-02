
#! /bin/bash
sudo hostnamectl set-hostname moon-node-5
echo America/Chicago > /home/ubuntu/timezone.txt
sudo apt-get update
sudo apt-get install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
echo "Started" > /home/ubuntu/3.txt
echo "<h1>Deployed via Terraform</h1>" | sudo tee /var/www/html/index.html
sudo echo nv-admin > /home/ubuntu/user.txt
sudo reboot
