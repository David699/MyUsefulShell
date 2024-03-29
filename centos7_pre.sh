#!/bin/bash

 
yum install net-tools psmisc  wget  python-pip -y 

firewall-cmd --state
systemctl stop firewalld.service
systemctl disable firewalld.service


sed -i 's@net.ipv4.ip_forward.*@net.ipv4.ip_forward = 1@g' /etc/sysctl.conf

echo "net.ipv4.ip_forward = 1" >>  /etc/sysctl.conf

sysctl -p /etc/sysctl.conf 


pip install mysql-connector-python
pip install requests


yum install epel-release elrepo-release -y
yum install yum-plugin-elrepo -y
yum install kmod-wireguard wireguard-tools -y
