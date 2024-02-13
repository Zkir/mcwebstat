import yaml
import json
from nbt import nbt
from datetime import datetime
from datetime import UTC
from os import listdir
from pathlib import Path
import glob
from zwebpage import ZWebPage


MINECRAFT_DIR = "d:/.Minecraft.1.20-paper_world_n2"
#MINECRAFT_DIR = ".Minecraft.1.20-paper_world_n2"

PERMISSIONS_FILE = MINECRAFT_DIR + "/plugins/PermissionsEx/permissions.yml" 
STATS_DIR = MINECRAFT_DIR + "/world/stats"
PLAYER_DATA_DIR = MINECRAFT_DIR +"/world/playerdata"

WHITELIST_FILE = MINECRAFT_DIR +"/whitelist.json"
BANNEDLIST_FILE = MINECRAFT_DIR +"/banned-players.json"


ranks={'admins3':4,'admins2':3,'admins':2,'police':1, 'default':0}

def sort_users_by_rank(user):
    return str(ranks[user['group']]) +'_' + str(format_time(user['play_time']))

def  format_time(t): 
    t=t//20
    d=t // (60*60*24)
    h=t % (60*60*24) // (60*60)
    m=t % (60*60) // 60
    s=0
    #return str(d) + ' д. ' + str(h) +' ч. ' + str(m) + ' мин.'
    return  f"{d:02d}" + ' д. ' + f"{h:02d}" +' ч. ' + f"{m:02d}" + ' мин.'


def format_unix_time(ts):
    return datetime.fromtimestamp(ts, UTC).strftime('%Y-%m-%d') #%H:%M:%S
 
#just a list of user files
playerdata_file_list=glob.glob(PLAYER_DATA_DIR+"/*.dat")

#per permissions file 
with open(PERMISSIONS_FILE, "r") as stream:
    try:
        pex_permissions = yaml.safe_load(stream)
        #print(dict)
    except yaml.YAMLError as exc:
        print(exc)

pex_groups=pex_permissions['groups']
pex_users=pex_permissions['users']


# white list and banned list


 
with open(WHITELIST_FILE,encoding='utf-8') as f:
        whitelist = json.load(f)

with open(BANNEDLIST_FILE,encoding='utf-8') as f:
        banlist = json.load(f)

#we need just UUIDs of whitelisted players.

whitelist_uuids=[] 
for record in whitelist :
    whitelist_uuids.append(record['uuid'])  

#read data from user files
admins= []
for playerdata_filename in playerdata_file_list:
    admin = {} 
    nbtfile = nbt.NBTFile(playerdata_filename)
    key=Path(playerdata_filename).stem
        
    #print('\n')
    #for k in nbtfile :
    #    print(k, nbtfile[k])
    #exit(1)    
      
    admin['uuid'] = key
    admin['last_played']  = int(str(nbtfile['bukkit']['lastPlayed']))//1000
    admin['first_played'] = int(str(nbtfile['bukkit']['firstPlayed']))//1000
    admin['name'] = str(nbtfile['bukkit']['lastKnownName'])
    
    if key in pex_users: 
        admin['group'] = pex_users[key]['group'][0]
        options = pex_users[key].get('options')
        if options is not None:
            #admin['name'] = options['name']
            admin['prefix'] = pex_groups[admin['group']]['options'].get('prefix','')
        else:
            admin['prefix'] =''
        

    else:
        admin['group'] = 'default'
        admin['prefix'] =''

    admin['prefix'] = admin['prefix'].replace('&r','') 
    admin['prefix'] = admin['prefix'].replace('&9','')
    admin['prefix'] = admin['prefix'].replace('&c','')

    with open(STATS_DIR +'/' + admin['uuid'] +'.json') as f:
        stats = json.load(f)
        admin['play_time'] = stats["stats"]["minecraft:custom"]["minecraft:total_world_time"] #play_time
        
        if "minecraft:mined" in stats["stats"] :
            admin['mined'] = sum(stats["stats"]["minecraft:mined"].values())
        else:
            admin['mined'] = 0   
        if "minecraft:used" in stats["stats"]:
            admin['used'] = sum(stats["stats"]["minecraft:used"].values())
        else:
            admin['used'] = 0
            
    admin['whitelisted'] = (admin["uuid"] in whitelist_uuids)         


    if True: #admin['group'] != 'default': 
        admins.append(admin)

       

admins.sort(key=sort_users_by_rank,  reverse = True)


page2 = ZWebPage("adminlist.html", "Игроки")

admin_list_html=''

admin_list_html += '<h1>Игроки сервера "Добрый король и веселые сыроежки"</h1> \n'

admin_list_html += '<table class="sortable">'
admin_list_html += '<tr><th>Имя</th><th>Первое появление</th><th>Группа</th><th>Префикс</td><th>Наигранное время</th><th>Добыто</th><th>Использовано</th><th>Последнее появление</th><th>Статус</th></tr> \n'
for user in admins:
    status=''
    if not user['whitelisted']:
        status +='<s>W</s>'
    #<td>'+str(user['uuid'])+'</td>
    admin_list_html += '<tr><td>'+str(user['name'])+'</td><td style="text-align:center">'+format_unix_time(user['first_played'])+'</td><td>'+str(user['group'])+'</td><td>'+str(user['prefix'])+'</td><td>'+str(format_time(user['play_time']))+'</td><td style="text-align: right;">'+str(user['mined'])+'</td><td style="text-align: right;">'+str(user['used'])+'</td> <td style="text-align:center">'+format_unix_time(user['last_played'])+'</td><td>'+status+'</td> </tr> \n'

admin_list_html += '</table>'


page2.print(admin_list_html)
page2.write()
 

page1 = ZWebPage("banlist.html", "Активные баны")
banlist_html =''
banlist_html += '<h1>Активные баны</h1> \n'
banlist_html += '<table class="sortable">'

banlist_html +='<tr><th>Игрок</th><th>Когда забанен</th><th>Кем</th><th>Причина бана</th><th>В белом списке</th></tr>'
for ban in banlist:
    whitelisted = (ban["uuid"] in whitelist_uuids) 
    if whitelisted:
        banlist_html +='<tr><td>'+ban["name"]+'</td><td>'+ban["created"]+'</td><td>'+ban["source"]+'</td><td>'+ban["reason"]+'</td><td>'+str(whitelisted)+'</td></tr>'

banlist_html += '</table>'

page1.print(banlist_html)
page1.write()


    