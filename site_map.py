import os
import json
import re
from zwebpage import ZWebPage


def page(url, title):
    return {"type": "page", "title": title, "url": url}
    
def category(title):
    return {"type": "category", "title": title, "pages": []} 
    
def get_page_title(filename):
    with open(filename, 'r', encoding="utf-8") as f:
      html=f.read()
   
    #match = re.search(r'<title>(.*)</title>','sdfsdf<title>Вы все дураки и не лечитесь</title>sdfsdf')
    match = re.search(r'<title>(.*)</title>',html)
    
    title = match.group(1)
    return title
    
 
docs_dir = "docs"
html_dir = "_build"

site_map = []
site_map.append(page("index.html", "Карта мира"))
auto_pages = category("Данные")
docs_pages = category("Документы")

site_map.append(auto_pages)
site_map.append(docs_pages)

auto_pages["pages"].append(page("players.html", "Список игроков"))
auto_pages["pages"].append(page("bans.html", "Активные баны"))
 

files = os.listdir(html_dir)
for file in files:
    filename, file_extension = os.path.splitext(file)
    if (file_extension == '.html') and (filename!='sitemap'):
        url = filename + '.html'
        page_title = get_page_title(html_dir+'/'+ file)

        if os.path.exists(docs_dir +'/' + filename +'.md'):
            docs_pages["pages"].append(page(url, page_title))    
        else:
            auto_pages["pages"].append(page(url, page_title))
  

with open('_build/site_map.json', 'w', encoding='utf-8') as f:
    json.dump(site_map, f, ensure_ascii=False, indent=4)    
    
    
html = ''
#html += '<ul class="list-style-sword">\n'
html += '<h1>Оглавление сайта</h1>\n'
html += '<ul>\n'
for element in site_map:
    if element["type"] == "page":
        html += '<li>'+ '<a href="'+element["url"]+'">' + element["title"]+ '</a></li>\n'
    else:
        html += '<li><b>'+ element["title"]+ '</b></li>\n'
        html += '<ul>'
        for el2 in element["pages"]:
            html += '<li>'+ '<a href="'+el2["url"]+'">' + el2["title"]+ '</a></li>\n'
        html += "</ul>\n"

html += "</ul>\n"


page1 = ZWebPage('_build/sitemap.html', "Оглавление сайта")
page1.print(html)
page1.write()