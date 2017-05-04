from functools import partial
import json , urllib2, time, warnings
#import urllib.request
#python3
import requests, re
import threading
from collections import Counter
# Vyatta Configuration
vyatta_ip = 'localhost'
auth=('vyatta', 'vyatta')
headers = {'Accept': 'application/json' , 'Vyatta-Specification-Version': '0.1' }
spam_drop = "https://www.spamhaus.org/drop/drop.txt"
delimiter = "##############################"
def start():
	print (delimiter)
	print ("Connecting to Vyatta")
	conf_url = 'https://%s/rest/conf' %vyatta_ip
	warnings.filterwarnings("ignore")
	r = requests.post(conf_url, auth=auth, headers=headers, verify=False)
	id = r.headers['location'].split('/')[2]
	conf_url = 'https://%s/rest/conf' %vyatta_ip
	requests.get(conf_url, auth=auth, headers=headers, verify=False)
	print ("Connection is established")
	print (delimiter)
	return id

id = start()


def get_ip_file(file_path):
	list_ip = []
	count = 0
	with open(file_path) as f:
		mylist = f.read().splitlines()
		for line in mylist:
			if line.startswith(";") or line.startswith("#") or not line.strip():
				continue
			regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})(?:\/[\d]{1,2})?',line)
			if regex != []:
				list_ip.append(regex[0])
				count = count + 1
	print ("Path of file: %s\nTotal IP: %s"  %(file_path,count))
	return list_ip

def get_ip_url(url):
	start_time = time.time()
	print (delimiter)
	print ("Adding IP List from URL %s is processing.\nPlease wait!" %(url))
	list_ip = []
	count = 0
	for line in urllib2.urlopen(url):
	#for line in urllib.request.urlopen(url):
		line = line.rstrip().decode("utf-8")
		if line.startswith(";") or line.startswith("#") or not line.strip():
			continue
		regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})(?:\/[\d]{1,2})?',line)
		if regex != []:
			count = count + 1
			list_ip.append(regex[0])
	elapsed_time = time.time() - start_time
	print ("Total IP: %s"  %(count))
	print ("Elapsed Time:%s seconds." %(elapsed_time))
	print (delimiter)
	return list_ip


def add_ip(list_ip,group_ip):
	start_time = time.time()
	print ("Adding IP List to Vyatta address-group %s is processing.\nPlease wait!" %(group_ip))
	for ip in list_ip:
		ip = ip.replace('/', '%2F')
		url = 'https://%s/rest/conf/%s/set/resources/group/address-group/%s/address/%s' %(vyatta_ip,id,group_ip,ip)
		requests.put(url, auth=auth, headers=headers, verify=False)        
	elapsed_time = time.time() - start_time
	print ("Elapsed Time:%s seconds." %(elapsed_time))

def commit():
	commit_url = 'https://%s/rest/conf/%s/commit' %(vyatta_ip,id)
	requests.post(commit_url, auth=auth, headers=headers, verify=False)
	return

def save():
	save_url = 'https://%s/rest/conf/%s/save' %(vyatta_ip,id)
	requests.post(save_url, auth=auth, headers=headers, verify=False)
	return

def exit():
	exit_url = 'https://%s/rest/conf/%s' %(vyatta_ip,id)
	requests.delete(exit_url, auth=auth, headers=headers, verify=False)
	return
# End Vyatta Configuration

##########################
# Connection Tracking
proc = "/proc/net/tcp"
ports = []
conn_limit = 0
ct_interval = 10
def conf(proc_file):
	with open(proc_file) as f:
		f.readline()
		mylist = f.read().splitlines()
		li = []
		for line in mylist:
			line = line.strip().split(' ')
			src_ip, src_p = get_ip_port(line[1])
			des_ip, des_p = get_ip_port(line[2])
			if src_ip == "0.0.0.0" or src_ip == "127.0.0.1":
				continue
			if ports == []:
				li.append(des_ip)
			elif src_p not in set(ports):
				continue
			else:
				li.append(des_ip)
	return (Counter(li))

def hex2dec(num):
	num = str(int(num,16))
	return	num 	
def get_ip_port(li):
	host,port = li.split(':')
	return ip(host),hex2dec(port)
def ip(s):
    ip = [(hex2dec(s[6:8])),(hex2dec(s[4:6])),(hex2dec(s[2:4])),(hex2dec(s[0:2]))]
    return '.'.join(ip)
	
def conn_track(conn_limit):
	#threading.Timer(ct_interval, conn_track, args = (ct_interval,conn_limit)).start()
	ips = conf(proc)
	list_ip = []
	for ip, num in ips.items():
	# python 2.x
	#for ip, num in ips.iteritems():
		if num >= conn_limit:
			list_ip.append(ip)

if conn_limit != 0:
	cronjob(conn_track,ct_interval,conn_limit)


# End connnection tracking.	
##########################
def cronjob(func,interval,*args):
    # call the provided func
    func(*args)
    threading.Timer(interval, partial(repeat, func, interval), args=args).start()

##########################
dshi = "http://feeds.dshield.org/top10-2.txt"
block = "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist"
blocklist = "https://lists.blocklist.de/lists/all.txt"
#add_ip(get_ip_url(blocklist),"blocklist")
#add_ip(get_ip_url(block),"block")
add_ip(get_ip_url(dshi),"dshi")
#add_ip(get_ip_url(spam_drop),"spam")
add_ip(get_ip_file("all.txt"), "blocklist")
commit()
save()
exit()
