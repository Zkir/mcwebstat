import re
import sys
import gzip
from os import listdir
from os.path import isfile, join


MINECRAFT_DIR = "d:/.Minecraft.1.20-paper_world_n2"
LOGS_DIR="d:/_temp/logs"

#obtain the list of log files in the directory
logfiles = [f for f in listdir(LOGS_DIR) if isfile(join(LOGS_DIR, f))]

print(str(len(logfiles))+' log files found')

#search_term = "([.]?[A-Za-z0-9_]+) issued server command: ([/][a-z:]+)" 
#search_term = "[.]?([A-Za-z0-9_]+) issued server command: ([/][a-z:]+)" 
search_term = "[.]?([A-Za-z0-9_]+) issued server command: ([/]lb) rollback" 

X ={}

#f = LOGS_DIR + "/" + "latest.log"
#for line in open(f, 'r',encoding='utf-8'):
#    r=re.search(search_term, line)
#    if r:
#        user_name=r.groups()[0]
#        command=r.groups()[1]
# 
#        if user_name not in X:
#            X[user_name]={}
#
#        if command not in X[user_name]:
#            X[user_name][command] = 0
#    
#        X[user_name][command] += 1
#
#
#print(X)

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

    with gzip.open(join(LOGS_DIR, gzfile)) as f:
      for line in f:
        line = line.decode('utf-8') # for compatible with python3
        r=re.search(search_term, line)
        if r:
            user_name=r.groups()[0]
            command=r.groups()[1]
            
            if command  in admin_commands_1:
                print(gzfile, line)
                if user_name not in X:
                    X[user_name]={}
        
                if command not in X[user_name]:
                    X[user_name][command] = 0
            
                X[user_name][command] += 1

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
