#=============================================================
# This a very simple web-site engine
#
#=============================================================
EXPORT_PATH = './'

from datetime import datetime

class ZWebPage:
    def __init__(self, name, title):
        self.page_name=name
        self.page_html = '' 
        self.content = '' 
        self.title = title

    def print(self, text):
        self.content += text

    def write(self):
        self.page_html = '<html>' \
                                  + '<head>' \
                                  + '<meta charset="UTF-8">' \
                                  + '<title>' + self.title + '</title>' \
                                  +'<script src="/js/sorttable.js" type="Text/javascript"></script>' \
                                  + '<style>' \
                                  + 'table {border: 1px solid grey;} ' \
                                  + 'th {border: 1px solid grey; }' \
                                  + 'td {border: 1px solid grey; padding:5px}' \
                                  + '</style>' \
                                  + '</head>' \
                                  + '<body> \n'

        self.page_html += """<div id="menu">
                  <b><a href="/">Карта Сервера</a> </b> 
                  -- <a href="adminlist.html">Игроки</a> 
                  -- <a href="banlist.html">Баны</a> 
                  -- <a href="https://discord.gg/wjSQsGW8rD">Дискорд</a>
               </div>"""

        self.page_html += self.content

        self.page_html += '<hr />' \
                                   + '<small><center> страница создана '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'</center></small> \n' \
                                   + '</body></html>'

        with open(EXPORT_PATH+self.page_name, 'w', encoding="utf-8") as f1:
            f1.write(self.page_html)
