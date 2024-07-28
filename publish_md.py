import os
import markdown
from zwebpage import ZWebPage
import re

EXPORT_PATH = '_build'
DOCS_PATH = "docs"

def md2html(source, target):
    f = open(source,  "r", encoding="utf-8")
    md=f.read()
    html = markdown.markdown(md)
    html=re.sub(r'.md',r'.html',html)
    html=html.replace('<blockquote>', '<span class="content__command" @click="saveText">')
    html=html.replace('</blockquote>','</span>')
    html=html.replace('<ul>','<ul class="list-style-sword">')
    
    page_title =  md.split('\n',2)[0].replace('#',''). strip()

    page1 = ZWebPage(EXPORT_PATH+ '/' + target, page_title )
    page1.print(html)
    page1.write()


files = os.listdir(DOCS_PATH)
for file in files:
    filename, file_extension = os.path.splitext(file)
    
    if file_extension == ".md":
        md2html("docs/"+filename+".md",filename + '.html')



