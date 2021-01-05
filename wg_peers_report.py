# coding=utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#pip install mysql-connector-python

import mysql.connector
from mysql.connector import pooling

import subprocess
import datetime
import types
import sys
import requests
import os

'''
CREATE TABLE wg_peers (
	id INT ( 8 ) UNSIGNED NOT NULL AUTO_INCREMENT,
	private_key VARCHAR ( 64 ) NOT NULL,
	allowed_ips VARCHAR ( 32 ) NOT NULL,
	latest_handshakes INT ( 12 ) UNSIGNED,
	update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	server_host VARCHAR ( 32 ),
	server_port INT ( 8 ) UNSIGNED,
PRIMARY KEY ( id ) 
)
'''

class WgPeer:
    def __init__(self, privateKey, allowIp,lastHandsShake):
        self.privateKey = privateKey
        self.allowIp = allowIp
        self.lastHandsShake = int(lastHandsShake)


    def printWgPeer(self):
        print ("privateKey : ", self.privateKey, ", allowIp: ", self.allowIp,", lastHandsShake: ", self.lastHandsShake," date:", datetime.datetime.fromtimestamp(self.lastHandsShake).isoformat())


if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    # python version < 3.3
    import time
    def timestamp(date):
        #Convert a time tuple in local time to seconds since the Epoch.
        return time.mktime(date.timetuple())
else:
    def timestamp(date):
        return date.timestamp()



def  myTimeZone():
    ts = time.time()
    seconds_offset = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)).total_seconds()
    return _format_offset(seconds_offset)


def _format_offset(seconds_offset):
    """
    将偏移秒数转换为UTC±X
    注意：这里没有考虑时区偏移非整小时的，使用请修改处理方式
    :param seconds_offset 偏移秒数
    :return: 格式化后的时区偏移
    """
    hours_offset = int(seconds_offset/60/60)
    if hours_offset >= 0:
        return "UTC+" + str(hours_offset)
    else:
        return "UTC" + str(hours_offset)

#2 hours in seconds
IDLE_TIME_OUT = int(2*60*60)
SEP_CHAR = ','
print ("get IP from https://checkip.amazonaws.com,this may take some time")
HOST_IP = requests.get('https://checkip.amazonaws.com').text.strip()
print("my pub IP:",HOST_IP)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    zone = myTimeZone()
    print("TimeZone:",zone)
    if zone != 'UTC+0':
        print("Please set time zone to UTC+0 first")
    else:
        print("TimeZone UTC+0 ok")


now = datetime.datetime.now()
print("now",now.isoformat())


nowTimeStamp = int(timestamp(now))
print("timestamp",  nowTimeStamp)

date = datetime.datetime.fromtimestamp(nowTimeStamp)
print("date",  date.isoformat())



#wg show all dump | grep "10.10."| cut -f2,5,6
out = subprocess.Popen("wg show all dump | grep '10.10.' | cut -f2,5,6 --output-delimiter=','",
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,shell=True)


cmdout,stderr = out.communicate()


#print(cmdout)
sArray = cmdout.splitlines()

if len(sArray) <= 2:
    'may be run on windows,get error code'
    cmdout='''RnENCJeppInySU07Iaw8OiC3bk257gbRtX5A15UAfCc=    10.10.10.2/32   0
60ZqmGjIFzy8xeYsUMnoF8JhXBUdKCl3AtVHG9wyMlE=    10.10.10.3/32   0
FrVsp0q/Ud9gR2LLBEbFwEuHqOY3pdAyPm/qzMYoZU8=    10.10.10.4/32   0
NLJUsDEuBNxOExPzqZ/P2A/QyBheDuPClQ7mCszMYTg=    10.10.10.30/32  0
OjjsN+Ahw4zjc4D8bpr/MwMu7yFo2gqflOxg0lvZYjs=    10.10.10.31/32  0
KSnzdolYlapid5h7ba4i36vXN3fuHZRLlnYK6L39amM=    10.10.10.32/32  0
QXpLWrHol82y4yHcYqcuKOV3Sd+ApHDyIUNIWKTailM=    10.10.10.33/32  1607433986
TGd7GxWRhRrbrA/L+ARxD+wj3vxxXqKRxcjzhtoMxQg=    10.10.10.34/32  0
KSnzdolYlapid5h7ba4i36vXN3fuHZRLlnYK6L39amM=    10.10.11.32/32  0
QXpLWrHol82y4yHcYqcuKOV3Sd+ApHDyIUNIWKTailM=    10.10.11.33/32  1607434257
TGd7GxWRhRrbrA/L+ARxD+wj3vxxXqKRxcjzhtoMxQg=    10.10.11.34/32  0
'''
    #set to a debug string
    sArray = cmdout.splitlines()


#print(stderr)

#print (cmdout)


wgPeerList = []


for line in sArray:
    #print(line)
    ret = line.split(SEP_CHAR)
    while '' in ret:
        ret.remove('')

    if len(ret) < 3:
        print("invalid peer:",ret)
        continue

    wgPeer = WgPeer(ret[0],ret[1],ret[2])
    if nowTimeStamp - wgPeer.lastHandsShake >= IDLE_TIME_OUT and wgPeer.lastHandsShake != 0:
        wgPeerList.append(wgPeer)

'''
#test only
del wgPeerList [:]
wgPeerList.append(WgPeer("RnENCJeppInySU07Iaw8OiC3bk257gbRtX5A15UAfCc=","10.10.10.2/32",0))
wgPeerList.append(WgPeer("60ZqmGjIFzy8xeYsUMnoF8JhXBUdKCl3AtVHG9wyMlE=","10.10.10.3/32",0))
wgPeerList.append(WgPeer("FrVsp0q/Ud9gR2LLBEbFwEuHqOY3pdAyPm/qzMYoZU8=","10.10.10.4/32",0))
'''


data = [

]


for peer in wgPeerList:
    peer.printWgPeer()
    data.append((peer.lastHandsShake,peer.allowIp,HOST_IP))


dbconfig = {
  "host":"47.0.0.0",
  "user":"root",
  "password":"000000",
  "database":"databasename",
  "connection_timeout":5
  #TypeError: argument 4 must be int, not float(5  not 5.0)

}


'''
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",pool_size=3,**dbconfig)
cnx1 = cnxpool.get_connection()
'''

cnx1 = mysql.connector.connect(**dbconfig)


mycursor = cnx1.cursor(buffered=True)


#UPDATE wg_peers SET latest_handshakes = 1  WHERE server_host = '61.61.61.61' and  allowed_ips = '10.10.10.2/32'

cmdStr = "UPDATE wg_peers SET latest_handshakes = %s WHERE allowed_ips = %s and server_host = %s"
mycursor.executemany(cmdStr,data)


cnx1.commit()
print(mycursor.rowcount, "record updated.")

cnx1.close()


