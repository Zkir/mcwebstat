import yaml
from zwebpage import ZWebPage
import sqlite3

def get_minecraft_dir():
    with open('mcwebstat_config.yml', 'r') as f:
        config = yaml.safe_load(f)
    return config['MINECRAFT_DIR']

MINECRAFT_DIR = get_minecraft_dir()
MEDAL_CONFIG_FILE = MINECRAFT_DIR + "/plugins/BlindSniperMC/medals.yml" 
MEDAL_DB_FILE = MINECRAFT_DIR + "/plugins/BlindSniperMC/medals.db" 

def remove_color_tags(s):
    
    s = s.replace('&4','')
    s = s.replace('&6','')
    s = s.replace('&9','')
    s = s.replace('&c','')
    s = s.replace('&e','')
    s = s.replace('&r','') 
    
    s = s.replace('§4','')
    s = s.replace('§6','')
    s = s.replace('§9','')
    s = s.replace('§c','')
    s = s.replace('§e','')
    s = s.replace('§r','')
    
    return s

def obtain_medal_stats():
    x = {} 
    connection = sqlite3.connect(MEDAL_DB_FILE)  
    cursor = connection.cursor()
    cursor.execute('select medal_type, sum (1) from player_medals GROUP BY medal_type')  
    recs = cursor.fetchall()
    connection.close()
    
    for rec in recs:
        x[rec[0]]=rec[1]
    return x


def main():

    with open(MEDAL_CONFIG_FILE, "r",encoding='utf-8') as stream:
        medals = yaml.safe_load(stream)
        
    medal_stats=obtain_medal_stats()        
        
    page1 = ZWebPage("_build/medals.html", "Награды Сервера")

    medals_html="<h1> Награды сервера </h1>\n"
    medals_html += '<div id="bka_scroll" class="a123" style="overflow:auto;">\n'
    medals_html += '<table class="sortable" style="width: 100%;">\n'
    medals_html += '<th>Название награды</th><th>Вид награды</th><th>Правила награждения</th><th>Символ</th><th>Призы</th><th>Количество награжденных</th> \n'

    for medal in medals['Medals']:
     
        medals_html += '<tr>\n    '
        medals_html += '<td column-name="Название награды">' + medal['Medal']['name'] +  '</td>' 
        medals_html += '<td column-name="Вид награды">' + medal['Medal']['medal_item']['title'] + '</td>' 
        medals_html += '<td column-name="Правила награждения">' +'Выдается '+ medal['Medal']['medal_item']['description'] + '</td>'\
                     + '<td column-name="Символ">' + remove_color_tags(medal['Medal']['symbol'])+ '</td>' \
                     + '<td column-name="Призы">'

        medals_html += medal['Medal']['medal_item']['material'] + ' 1' + '<br />'                 
        if 'prizes' in medal['Medal']:
            for prize in medal['Medal']['prizes']:
                medals_html += prize['prize']['material'] + ' ' + str(prize['prize']['amount']) + '<br />'
        medals_html += '</td>'
        
        n = medal_stats.get(medal['Medal']['id'],0)

        medals_html += '<td column-name="Количество награжденных">'+str(n)+'</td>' \
                     + '</tr>\n'
        

    medals_html += '</table>\n'
    medals_html += '</div>\n'
    medals_html += "<h3> Примечания</h3>\n"
    medals_html += '<p>Отличие ("звёздочка") выдается за побитие текущего рекорда, так что порог на награды с отличием со временем увеличивается.</p>'


    page1.print(medals_html)
    page1.write()    
    
    
main()    