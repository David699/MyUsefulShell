#!/bin/bash
SERVER_TOTAL=1
CLIENT_TOTAL=254

SERVER_START_PORT=58800
SERVER_IP="8.8.8.8"

CFG_FILE="/etc/wireguard/wg1.conf"

NET_DEVICE="eth0"

function genServerKey() {
	for ((i = 1; i <= $SERVER_TOTAL; i++)); do
		echo "wg genkey | tee /etc/wireguard/server_cfg/server_private_$i.key | wg pubkey | sudo tee /etc/wireguard/server_cfg/server_public_$i.key "
		if [ ! -f "/etc/wireguard/server_cfg/server_private_$i.key" ]; then
			wg genkey | tee /etc/wireguard/server_cfg/server_private_$i.key | wg pubkey | sudo tee /etc/wireguard/server_cfg/server_public_$i.key
		else
			echo "skip /etc/wireguard/server_cfg/server_private_$i.key"
		fi
	done
}

function delServerKey() {
	rm -f /etc/wireguard/server_cfg/server_private_*.key
	rm -f /etc/wireguard/server_cfg/server_public_*.key
}

function genClientKey() {
	for ((i = 1; i <= $CLIENT_TOTAL; i++)); do
		echo "wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key "
		if [ ! -f "/etc/wireguard/client_cfg/client_private_$i.key" ]; then
			wg genkey | tee /etc/wireguard/client_cfg/client_private_$i.key | wg pubkey | sudo tee /etc/wireguard/client_cfg/client_public_$i.key
		else
			echo "skip /etc/wireguard/client_cfg/client_private_$i.key"
		fi
	done
}

function delClientKey() {
	rm -f /etc/wireguard/client_cfg/client_private_*.key
	rm -f /etc/wireguard/client_cfg/client_public_*.key
}

function genServerCfg() {
	serverPrivateKey=$(cat /etc/wireguard/server_cfg/server_private_1.key)
	cat >$CFG_FILE <<-EOF
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

	for ((i = 1; i <= $CLIENT_TOTAL; i++)); do
		count=$(($i + 1))
		echo "#=============================Peer$count =========================" >>$CFG_FILE
		echo "[Peer]" >>$CFG_FILE
		PublicKey=$(cat /etc/wireguard/client_cfg/client_public_$i.key)
		echo "PublicKey = $PublicKey" >>$CFG_FILE
		echo "AllowedIPs = 10.10.10.$count/32" >>$CFG_FILE
	done

}

function printClientKey() {
	for ((i = 1; i <= $CLIENT_TOTAL; i++)); do
		count=$(($i + 1))
		privateKey=$(cat /etc/wireguard/client_cfg/client_private_$i.key)
		ip="10.10.10.$count"
		echo "$ip,$privateKey"
	done

}


#pass a index for generate config for one client_cfg
# eg:55  PrivateKey = OEXPw7KJDdr2WFQSv8JBIdZH6aoCQqOp9gm+uR3ZCFo=
# Address = 10.10.10.55/32

function genOneClientConfig() {
    index=$1
	cfgFileIndex=$((index - 1))
	if [ $# -lt 1 ];then
		echo "pass a argument"
	else
		echo "gen $(whoami)/conf_client_$index.conf"
		privKey=$(cat /etc/wireguard/client_cfg/client_private_$cfgFileIndex.key)
		pubKey=$(cat /etc/wireguard/server_cfg/server_public_1.key)
		cat > /$(whoami)/conf_client_$index.conf <<-EOF
		[Interface]
			PrivateKey = $privKey
			Address = 10.10.10.$index/32
			DNS = 114.114.114.114

	    [Peer]
		PublicKey = $pubKey
		AllowedIPs = 0.0.0.0/0
		Endpoint = $SERVER_IP:$SERVER_START_PORT
		PersistentKeepalive = 25
		EOF
		
	fi
		 

}

#genServerKey
#genClientKey
#genServerCfg
#printClientKey
genOneClientConfig 55
