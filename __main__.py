"""An AWS Python Pulumi program"""
import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

sg = aws.ec2.SecurityGroup(
    "webSG",
    description = "Http",
    ingress = [
        {
            'protocol':'tcp',
            'from_port': 80,
            'to_port': 80,
            'cidr_blocks' : ['0.0.0.0/0']

        }
    ],
    egress = [
        {
            'protocol':'-1',
            'from_port': 0,
            'to_port': 0,
            'cidr_blocks' : ['0.0.0.0/0']

        }
    ]
)

ami = aws.ec2.get_ami(
    most_recent=True,
    owners=['amazon'],
    filters=[{"name":"name","values":["amzn2-ami-hvm-*-x86_64-ebs"]}
             ])

user_data = """#!/bin/bash
yum -y update
yum -y install httpd
yum -y install git
mkdir /home/games && sudo cd /home/games
git clone https://github.com/damatechguy27/gameapps.git
cp -rf gameapps/Glokar/* /var/www/html
chown -R apache:apache /var/www/html/*
systemctl start httpd
systemctl enable httpd
rm -rf /home/games
"""

instance = aws.ec2.Instance(
    "pulumi-server1",
    instance_type="t3.micro",
    security_groups = [sg.name],
    ami = ami.id,
    user_data = user_data

) 


pulumi.export("web-app-ip", instance.public_ip)

