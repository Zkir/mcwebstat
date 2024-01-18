import yaml
import json
from nbt import nbt
from datetime import datetime
from datetime import UTC

MINECRAFT_DIR = "d:/.Minecraft.1.20-paper_world_n2"
#MINECRAFT_DIR = "d:/.Minecraft.1.19-paper_world_n1"

PERMISSIONS_FILE = MINECRAFT_DIR + "/plugins/PermissionsEx/permissions.yml" 
STATS_DIR = MINECRAFT_DIR + "/world/stats"
PLAYER_DATA_DIR = MINECRAFT_DIR +"/world/playerdata"

ranks={'admins3':0,'admins2':1,'admins':2,'police':3, 'default':1000}

def sort_users_by_rank(users):
    return ranks[users['group']]

def  format_time(t): 
    t=t//20
    d=t // (60*60*24)
    h=t % (60*60*24) // (60*60)
    m=t % (60*60) // 60
    s=0
    return str(d) + ' д. ' + str(h) +' ч. ' + str(m) + ' мин.'

def format_unix_time(ts):
    return datetime.fromtimestamp(ts, UTC).strftime('%Y-%m-%d') #%H:%M:%S
 

with open(PERMISSIONS_FILE, "r") as stream:
    try:
        dict = yaml.safe_load(stream)
        #print(dict)
    except yaml.YAMLError as exc:
        print(exc)

groups=dict['groups']

dict=dict['users']

admins= []
for key in dict:
    admin ={} 
    admin['uuid'] = key
    options = dict[key].get('options')
    if options is not None:
        admin['name'] = options['name']
        admin['group'] = dict[key]['group'][0]
        admin['prefix'] = groups[admin['group']]['options'].get('prefix','')
        admin['prefix'] = admin['prefix'].replace('&r','') 
        admin['prefix'] = admin['prefix'].replace('&9','')
        admin['prefix'] = admin['prefix'].replace('&c','')
        with open(STATS_DIR +'/' + admin['uuid'] +'.json') as f:
            stats = json.load(f)
            admin['play_time'] = stats["stats"]["minecraft:custom"]["minecraft:total_world_time"] #play_time
           
            admin['mined'] =sum(stats["stats"]["minecraft:mined"].values())
            admin['used'] =sum(stats["stats"]["minecraft:used"].values())
        
        playerdata_filename= PLAYER_DATA_DIR +'/' + admin['uuid'] +'.dat' 
         
        nbtfile = nbt.NBTFile(playerdata_filename)
        
        #print('\n')
        #for k in nbtfile :
        #    print(k, nbtfile[k])
          
        admin['last_played']  = int(str(nbtfile['bukkit']['lastPlayed']))//1000
        admin['first_played'] = int(str(nbtfile['bukkit']['firstPlayed']))//1000
        admin['name'] = str(nbtfile['bukkit']['lastKnownName']) # should be the same as name from permissions.
        if True: #admin['group'] != 'default': 
            admins.append(admin)

admins.sort(key=sort_users_by_rank)


admin_list_html='<html><head>' \
                +'<title>Список администраторов</title>' \
                +'</head><body>'

admin_list_html += '<h1>Список Администраторов Сервера "Добрый король и веселые сыроежки"</h1> \n'

admin_list_html += '<table>'
admin_list_html += '<tr><th>Имя</th><th>Первое появление</th><th>Группа</th><th>Префикс</td><th>Наигранное время</th><th>Добыто</th><th>Использовано</th><th>Последнее появление</th></tr> \n'
for user in admins:
    #<td>'+str(user['uuid'])+'</td>
    admin_list_html += '<tr><td>'+str(user['name'])+'</td><td style="text-align:center">'+format_unix_time(user['first_played'])+'</td><td>'+str(user['group'])+'</td><td>'+str(user['prefix'])+'</td><td>'+str(format_time(user['play_time']))+'</td><td style="text-align: right;">'+str(user['mined'])+'</td><td style="text-align: right;">'+str(user['used'])+'</td> <td style="text-align:center">'+format_unix_time(user['last_played'])+'</td> </tr> \n'

admin_list_html += '</table></body></html>'

with open('adminlist.html', 'w') as f1:
    f1.write(admin_list_html)


