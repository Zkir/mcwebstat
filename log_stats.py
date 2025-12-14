import re
import sys
import gzip
from os import listdir
from os.path import isfile, join
import json

import yaml

def get_minecraft_dir():
    with open('mcwebstat_config.yml', 'r') as f:
        config = yaml.safe_load(f)
    return config['MINECRAFT_DIR']

MINECRAFT_DIR = get_minecraft_dir()
LOGS_DIR=MINECRAFT_DIR + "/logs"
BANNEDLIST_FILE = MINECRAFT_DIR + "/banned-ips.json"

with open(BANNEDLIST_FILE,encoding='utf-8') as f:
        banlist = json.load(f)
        
banned_ips = []
for rec in banlist:
    banned_ips.append(rec["ip"])


#obtain the list of log files in the directory
logfiles = [f for f in listdir(LOGS_DIR) if isfile(join(LOGS_DIR, f))]

print(str(len(logfiles))+' log files found')

#search_term = "([.]?[A-Za-z0-9_]+) issued server command: ([/][a-z:]+)" 
#search_term = "[.]?([A-Za-z0-9_]+) issued server command: ([/][a-z:]+)" 
search_term = "[.]?([A-Za-z0-9_]+) issued server command: ([/]lb) rollback" 

#[00:21:08] [Server thread/INFO]: .JiveDuck4348614[/185.8.202.242:0] logged in with entity id 3403969 at ([world]-733.4234, 69.9375, 263.56415)
#[08:09:50] [Server thread/INFO]: falyfay[/176.212.168.5:25860] logged in with entity id 3404528 at ([world]-1066.3217613394072, 67.0, 168.62756862394158)

#login line
login_line = r'\[Server thread\/INFO\]: ([.]?[A-Za-z0-9_]+)\[\/([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):[0-9]*\] logged in with entity id'

X ={}

ip_addresses = {}

non_admin_commands=('/whisper', '/tell', '/minecraft:msg', '/lay', '/sit','/spin', '/discord','/rules','/help')

#those are rather adminitstrator priviliges, not duties. 
admin_commands_0 = ('/tp', '/kill','/invsee')

#real admin commands
#admin_commands_1 = ('/tps', '/kick', '/lb','/logblock','/banlist', '/tempban', '/ban', '/banip', '/unban', '/pardon'  )
#admin_commands_1 = ('/kick', '/tempban', '/ban', '/banip', '/unban', '/pardon'  )
admin_commands_1 = ('/lb','/logblock')

#operator_commands
admin_commands_2 = ('/gamemode', '/pex','/promote', '/demote', '/summon', '/give', '/nick')

# '/dmarker', '/dynmap', '/dmap', '/stat', '/undo', '/redo', 


X = {}
for gzfile in logfiles:

    if gzfile[-6:] != "log.gz":
        continue	
	
    with gzip.open(join(LOGS_DIR, gzfile)) as f:
      for line in f:
        line = line.decode('utf-8') # for compatible with python3
        r=re.search(search_term, line)
        if r:
            user_name=r.groups()[0]
            command=r.groups()[1]
            
            if command  in admin_commands_1:
                #print(gzfile, line)
                if user_name not in X:
                    X[user_name]={}
        
                if command not in X[user_name]:
                    X[user_name][command] = 0
            
                X[user_name][command] += 1

        #analyze logins  
        r=re.search(login_line, line)
        if r:

            user_name=r.groups()[0]
            ip =r.groups()[1]

            if ip not in ip_addresses:  
                ip_addresses[ip] = []

            if user_name not in ip_addresses[ip]:
                ip_addresses[ip].append(user_name)

          
Y=[]
for user_name in X:
    command_stats = X[user_name]
    n=0
    for c in command_stats:
        n+=command_stats[c] 
    Y.append((user_name,n))


Y.sort(key=lambda element: element[1], reverse=True)

for user in Y:
    print(user[0],user[1])
    command_stats = X[user[0]]
    #print('   ', command_stats)
    #print ('')

print()

with open('_build/ips.json', 'w', encoding='utf-8') as f:
    json.dump(ip_addresses, f, ensure_ascii=False, indent=4)

#get just ips

ips = sorted(ip_addresses)

ips.sort(key=lambda ip: len(ip_addresses[ip]), reverse=True )


for ip in ips:
    if len(ip_addresses[ip])>1:
        print()
        if ip in banned_ips:
            print(ip, " -- BANNED")
        else:    
            print(ip )
        print("",ip_addresses[ip])

