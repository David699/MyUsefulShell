#!/bin/bash  
SERVER_TOTAL=1  
CLIENT_TOTAL=100

SERVER_START_PORT=58800

CFG_FILE="/etc/wireguard/wg1.conf"

NET_DEVICE="eth0"
  
function genServerKey(){
    for((i=1;i<=$SERVER_TOTAL;i++));  
	do  
	echo "wg genkey | tee /etc/wireguard/server_cfg/server_private_$i.key | wg pubkey | sudo tee /etc/wireguard/server_cfg/server_public_$i.key "
	wg genkey | tee /etc/wireguard/server_cfg/server_private_$i.key | wg pubkey | sudo tee /etc/wireguard/server_cfg/server_public_$i.key 
	done 
}

function delServerKey(){
    rm -f  /etc/wireguard/server_cfg/server_private_*.key
	rm -f  /etc/wireguard/server_cfg/server_public_*.key
}

function genClientKey(){
    for((i=1;i<=$CLIENT_TOTAL;i++));  
	do  
	echo "wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key "
	wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key 
	done 
}

function delClientKey(){
    rm -f  /etc/wireguard/client_cfg/client_private_*.key
	rm -f  /etc/wireguard/client_cfg/client_public_*.key
}



function genClientKey(){
    for((i=1;i<=$CLIENT_TOTAL;i++));  
	do  
	echo "wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key "
	wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key 
	done 
}

function genServerCfg(){
serverPrivateKey=`cat /etc/wireguard/server_cfg/server_private_1.key`
cat > $CFG_FILE<<-EOF
[Interface]
Address = 10.10.10.1/24
ListenPort = $SERVER_START_PORT
PrivateKey = $serverPrivateKey
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o $NET_DEVICE -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o $NET_DEVICE -j MASQUERADE

#[Peer]
#PublicKey = AYQJf6HbkQ0X0Xyt+cTMTuJe3RFwbuCMF46LKgTwzz4=
#AllowedIPs = 10.10.10.2/32

EOF

for((i=1;i<=$CLIENT_TOTAL;i++));  
do
count=$(($i+1))
echo "#=============================Peer$count =========================" >> $CFG_FILE 
echo "[Peer]" >> $CFG_FILE
PublicKey=`cat /etc/wireguard/client_cfg/client_public_$i.key`
echo "PublicKey = $PublicKey"  >> $CFG_FILE
echo "AllowedIPs = 10.10.10.$count/32"  >> $CFG_FILE
done 
   
}


 
#genServerKey
#genClientKey
genServerCfg
