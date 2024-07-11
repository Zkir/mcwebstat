#=============================================================
# This a very simple web-site engine
#
#=============================================================
EXPORT_PATH = './'

from datetime import datetime

class ZWebPage:
    def __init__(self, name, title):
        self.page_name=name
        self.content = '' 
        self.title = title

        with open('zwebpage_template/page_template.html', 'r', encoding="utf-8") as f:
            self.page_html =  f.read()
        #print(self.page_html)

    def print(self, text):
        self.content += text

    def write(self):
        s = self.page_html
        s = s.replace("<%title% />", self.title)
        s = s.replace("<%content% />", self.content)
        s = s.replace("<%content_updated% />", 'Страница создана '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        with open(EXPORT_PATH+self.page_name, 'w', encoding="utf-8") as f1:
            f1.write(s)
