#!/bin/bash

 
yum install net-tools psmisc  wget  python-pip -y 

firewall-cmd --state
systemctl stop firewalld.service
systemctl disable firewalld.service


echo "net.ipv4.ip_forward=1" > /etc/sysctl.conf
sysctl -p /etc/sysctl.conf 


pip install mysql-connector-python


yum install epel-release elrepo-release -y
yum install yum-plugin-elrepo -y
yum install kmod-wireguard wireguard-tools -y
