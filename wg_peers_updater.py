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



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    zone = myTimeZone()
    print("TimeZone:",zone)





dbconfig = {
  "host":"47.0.0.0",
  "user":"root",
  "password":"******",
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


#UPDATE wg_peers SET latest_handshakes = 1  WHERE server_host = '61.160.213.135' and  allowed_ips = '10.10.10.2/32'


data = [

]



for index in range(1,255):
    cmd = 'cat /etc/wireguard/client_cfg/client_private_' + str(index) + '.key'
    out = subprocess.Popen(cmd,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,shell=True)
    cmdout, stderr = out.communicate()
    allowip = '10.10.%.'+ str(index + 1)  + '/32'
    data.append((cmdout.strip(),allowip))


print(data)




cmdStr = "UPDATE wg_peers SET private_key = %s WHERE allowed_ips like %s"
mycursor.executemany(cmdStr,data)


cnx1.commit()
print(mycursor.rowcount, "record updated.")

cnx1.close()


