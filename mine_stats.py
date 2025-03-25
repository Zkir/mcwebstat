import yaml
import json
import os
from nbt import nbt
from datetime import datetime
from datetime import UTC
from os import listdir
from pathlib import Path
import glob
import sqlite3
from zwebpage import ZWebPage


MINECRAFT_DIR = "d:/.Minecraft.1.20-paper_world_n2"
#MINECRAFT_DIR = "d:/.minecraft_server"

WEB_DIR = "d:/_minecraft_site"

STATS_DIR = MINECRAFT_DIR + "/world/stats"
PLAYER_DATA_DIR = MINECRAFT_DIR +"/world/playerdata"
ADVANCEMENTS_DIR = MINECRAFT_DIR +"/world/advancements"

WHITELIST_FILE = MINECRAFT_DIR +"/whitelist.json"
BANNEDLIST_FILE = MINECRAFT_DIR +"/banned-players.json"
PERMISSIONS_FILE = MINECRAFT_DIR + "/plugins/PermissionsEx/permissions.yml" 
DS_LINKS_FILE = MINECRAFT_DIR + "/plugins/DiscordSRV/accounts.aof" 
NLOGIN_DB_FILE = MINECRAFT_DIR+ '/plugins/nLogin/nlogin.db'

ranks={'admins4':6, 'admins3a':5, 'admins3':4,'admins2':3,'admins':2,'police':1, 'default':0}

def sort_users_by_rank(user):
    if user['whitelisted']:
        wl='1'
    else: 
        wl='0'    
    return str(ranks[user['group']]) + '_' + str(wl) +'_' + str(format_time(user['play_time']))

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
    
def remove_color_tags(s):
    
    s = s.replace('&4','')
    s = s.replace('&6','')
    s = s.replace('&9','')
    s = s.replace('&c','')
    s = s.replace('&e','')
    s = s.replace('&r','') 

    s = s.replace('§4','')
    s = s.replace('§5','')
    s = s.replace('§6','')
    s = s.replace('§9','')
    s = s.replace('§c','')
    s = s.replace('§e','')
    s = s.replace('§r','')
    s = s.replace('§f','')    
    
    return s
    
def remove_medals_and_stars(s):
    s = s.replace('[***]','')    
    s = s.replace('[**]','')    
    s = s.replace('[*]','')    
    s = s.replace('[||]','')    
    s = s.replace('[|]','')    
    
    s = s.replace('✔','')    
    s = s.replace('✻','')    
    s = s.replace('Ⓑ','')    
    s = s.replace('Ⓜ','')    
    s = s.replace('Ⓥ','')    
    
    s = s.replace('ⓑ','')    
    s = s.replace('❖','')    
    
    return s

#just a list of user files
playerdata_file_list=glob.glob(PLAYER_DATA_DIR+"/*.dat")

#per permissions file 
with open(PERMISSIONS_FILE, "r",encoding='utf-8') as stream:
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
        
# DS links 
# it seems that now it's just a text file lines separated by space
with open(DS_LINKS_FILE,encoding='utf-8') as f:
        ds_links_data = f.readlines()
ds_links ={}
for line in ds_links_data:
    key = line.strip().split(' ')[0]
    value = line.strip().split(' ')[1]
    ds_links[value]=key # for some reason it is "ds_id minecraft_uuid"
    

#we need just UUIDs of whitelisted players.
whitelist_uuids=[] 
for record in whitelist :
    whitelist_uuids.append(record['uuid'])  
    
#Obtain the list of registred users from nlogin db    
connection = sqlite3.connect(NLOGIN_DB_FILE)  
cursor = connection.cursor()
cursor.execute('SELECT last_name, last_ip FROM nlogin where password is not NULL')  
registered_users1 = cursor.fetchall()
connection.close()

registered_users = {}
for ruser in registered_users1:
    registered_users[ruser[0]]=ruser[1]

# let's obtain the list of materials, counted as blocks.
# we need them for builder statistics
block_materials = []
with open("blocks.txt", "r") as f:
    mat_lines = f.readlines()

for mat_line in mat_lines:
    block_materials.append("minecraft:"+mat_line.lower().strip())
    

#also obtain named achivements, because in world files named and unnamed achivements are mixed

named_advancements = []
with open("advancements.txt", "r") as f:
    advancements_lines = f.readlines()

for advancements_line in advancements_lines:
    named_advancements.append("minecraft:"+advancements_line.lower().strip())
    

#read data from user files
admins= []
for playerdata_filename in playerdata_file_list:
    admin = {} 
        
    key=Path(playerdata_filename).stem
    admin['uuid'] = key    
    
    try:       
        nbtfile = nbt.NBTFile(playerdata_filename)  
        admin['last_played']  = int(str(nbtfile['bukkit']['lastPlayed']))//1000
        admin['first_played'] = int(str(nbtfile['bukkit']['firstPlayed']))//1000
        admin['name'] = str(nbtfile['bukkit']['lastKnownName'])
    except:
        admin['last_played']  = 0
        admin['first_played'] = 0
        admin['name'] = "nbt_unreadable"
        print("ERROR: unable to parse nbt player data for player " + playerdata_filename)
    
    admin['group'] = 'default'
    admin['prefix'] =''
    
    try: 
        admin['suffix'] = pex_users[key]['options']['suffix'];
    except KeyError:
        admin['suffix'] = ''
    
    if key in pex_users: 
        
    
        #there can be several groups, we need to find one relevant to administrative ladder 
        #TODO: one may say that we need to find single primary group, but collect  prefixes  and suffixes from ALL groups. 
        if 'group' in pex_users[key]:
            for group in pex_users[key]['group']:         
                if group in ranks: 
                    admin['group'] = group
                    break
        
        options = pex_users[key].get('options')
        if options is not None:
            #admin['name'] = options['name']
            admin['prefix'] = pex_groups[admin['group']]['options'].get('prefix','')
        else:
            admin['prefix'] =''
        

        
    admin['prefix'] = remove_color_tags (admin['prefix'])
    admin['suffix'] = remove_color_tags (admin['suffix'])

    with open(STATS_DIR +'/' + admin['uuid'] +'.json') as f:
        stats = json.load(f)
        admin['play_time'] = stats["stats"]["minecraft:custom"]["minecraft:total_world_time"] #play_time
        
        if "minecraft:mined" in stats["stats"] :
            admin['mined'] = sum(stats["stats"]["minecraft:mined"].values())
        else:
            admin['mined'] = 0   
        if "minecraft:used" in stats["stats"]:
            admin['used'] = 0
            for mat in stats["stats"]["minecraft:used"]:
                if mat in block_materials:
                    admin['used'] += stats["stats"]["minecraft:used"][mat]
                else:
                    #print(mat)
                    pass
        else:
            admin['used'] = 0
            
    admin['whitelisted'] = (admin["uuid"] in whitelist_uuids)         
    
    if admin["uuid"] in ds_links:
        admin['discord'] =  ds_links[admin["uuid"]]
    else:
        admin['discord'] = ''


    if True: #admin['group'] != 'default': 
        admins.append(admin)
        
       
     
    #advancements  
    with open(ADVANCEMENTS_DIR +'/' + admin['uuid'] +'.json') as f:
        advancements = json.load(f)
    
    n_advancements = 0
    for advancement_name, advancement in advancements.items():
        
        #if isinstance(advancement,dict):
        if advancement_name in named_advancements: 
            if (advancement['done']==True):
                n_advancements += 1
    admin["advancements"]=n_advancements        

admins.sort(key=sort_users_by_rank,  reverse = True)


page2 = ZWebPage("_build/adminlist.html", "Игроки")

admin_list_html=''

admin_list_html += '<h1>Игроки сервера "Добрый король и веселые сыроежки"</h1> \n'

admin_list_html += '<table class="sortable">'
admin_list_html += '<tr><th>Имя</th><th>Первое появление</th><th>Префикс</td><th>Медали</th><th>Наигранное время</th><th>Добыто</th><th>Использовано</th><th>Последнее появление</th><th>Статус</th><th>Дискорд</th></tr> \n'
i=0
players_json = []
for user in admins:
    status=''
    i=i+1
    if not user['whitelisted']:
        status +='<s>W</s>'
        
        
    #if user['name'] in registered_users:
    #    status +='R'
        
    #if user['name'] not in registered_users and user['whitelisted']:    
    #    print(user['name'])
    
    last_ip=""
    if user['name'] in registered_users:
        last_ip=registered_users[user['name']]
    
    
    medals = str(user['suffix'])
    
    discord = '&#10004' if user['discord'] !='' else ''
    discord1 = '✔' if user['discord'] !='' else ''

    if True: #user['whitelisted']:    
        admin_list_html +=  '<tr>'  
        #admin_list_html += '<td>'+str(user['uuid'])+'</td>'
        admin_list_html += '<td>'+str(user['name'])+'</td><td style="text-align:center">'+format_unix_time(user['first_played'])+'</td>'\
                           +'<td>'+str(user['prefix'])+'</td><td>'+medals+'</td><td>'+str(format_time(user['play_time']))+'</td>'\
                           +'<td style="text-align: right;">'+str(user['mined'])+'</td><td style="text-align: right;">'+str(user['used'])+'</td>'\
                           +' <td style="text-align:center">'+format_unix_time(user['last_played'])+'</td><td>'+status+'</td>'\
                           + '<td style="text-align:center">'+discord+'</td>'
        admin_list_html += '</tr> \n'

        player_json = {}
        player_json["id"] = i
        player_json["uuid"] = str(user['uuid'])
        player_json["name"] = str(user['name'])
        if not user['whitelisted']:
            player_json["name"] ='<s>'+player_json["name"]+'</s>'

            
        player_json["prefix"] = str(user['prefix'])
        player_json["medals"] = medals

        player_json["date_last_usage"] = format_unix_time(user['last_played'])
        
        face_path = "/tiles/faces/32x32/"+str(user['name']) + ".png"
        if os.path.exists(WEB_DIR+face_path):
            player_json["face"] = '<img src="'+face_path+'"><src>'
        else:
            #face may not be yet generated by dynmap
            player_json["face"] =''
            
        
        player_json["time_gameplay"] = str(format_time(user['play_time']))
            
        player_json_more = {} 

        player_json_more["date_register"] = format_unix_time(user['first_played'])
        
        
        player_json_more["status"] = status 
        player_json_more["discord"] = discord1
        player_json_more["last_ip"] = last_ip
        activity_path = "/activity/"+str(user['uuid']) + ".png"
        player_json_more["activity"] = '<img src="'+activity_path+'"><src>'  
        
        player_json_more["mined"] = int(user['mined'])
        player_json_more["used"] = int(user['used'])
        player_json_more["advancements"] = int(user['advancements'])    

        player_json["more"] =[]
        player_json["more"].append(player_json_more)
        players_json.append(player_json)

admin_list_html += '</table>'

with open('_build/players.json', 'w', encoding='utf-8') as f:
    json.dump(players_json, f, ensure_ascii=False, indent=4)


page2.print(admin_list_html)
#page2.write()
 

page1 = ZWebPage("_build/banlist.html", "Активные баны")
banlist_html =''
banlist_html += '<h1>Активные баны</h1> \n'
banlist_html += '<table class="sortable">\n'

banlist_html +='<tr><th>Игрок</th><th>Cуффикс</th><th>Наигранное время</th><th>Когда забанен</th><th>Кем</th><th>Причина бана</th><th>Срок</th></tr>\n' #<th>В белом списке</th>

banlist.sort(key=lambda ban: ban["created"],  reverse = True)
i=0
bans_json = []
for ban in banlist:
    i=i+1
    whitelisted = (ban["uuid"] in whitelist_uuids) 
    ban_end = ban["expires"]
    if ban_end == "forever":
        ban_end = 'Навсегда'
     
    #Наигранное время 
    suffix = ""
    for user in admins: 
        
        if str(user['uuid']) ==  str(ban['uuid']):
            suffix = str(user['suffix'])
            played_time = str(format_time(user['play_time']))
            break
        
    if whitelisted:
        banlist_html +='<tr><td>'+ban["name"]+'</td><td>'+suffix+ '</td><td>'+played_time+'</td><td>'+ban["created"]+'</td><td>'+remove_color_tags(ban["source"].replace('§','&'))+'</td><td>'+ban["reason"]+'</td>'\
                      +'<td>'+ban_end+'</td></tr> \n' #<td>'+str(whitelisted)+'</td>

        ban_json = {}
        ban_json["id"] = i

        ban_json["name"] = ban["name"]

        ban_json["who"]  = remove_medals_and_stars (remove_color_tags(ban["source"].replace('&','§')))
        print("debug",ban_json["who"], ban["source"])
        ban_json["reason"] = ban["reason"]
        ban_json["time"] = ban_end 
        face_path = "/tiles/faces/32x32/"+str(ban['name']) + ".png"
        if os.path.exists(WEB_DIR+face_path):
            ban_json["face"] = '<img src="'+face_path+'"><src>'
        else:
            #face may not be yet generated by dynmap
            ban_json["face"] =''        
        ban_json_more = {} 

        ban_json_more["time_gameplay"] = played_time
        ban_json_more["date_ban"] = ban["created"]
        ban_json_more["suffix"] =  suffix

        ban_json["more"] = []
        ban_json["more"].append(ban_json_more)
        bans_json.append(ban_json)
         

banlist_html += '</table>\n'

page1.print(banlist_html)
#page1.write()

with open('_build/bans.json', 'w', encoding='utf-8') as f:
    json.dump(bans_json, f, ensure_ascii=False, indent=4)

