import markdown
from zwebpage import ZWebPage
import re
EXPORT_PATH = '_build/'

def md2html(source, target):
    f = open(source,  "r", encoding="utf-8")
    md=f.read()
    html = markdown.markdown(md)
    html=re.sub(r'.md',r'.html',html)
    html=html.replace('<blockquote>', '<span class="content__command" @click="saveText">')
    html=html.replace('</blockquote>','</span>')
    html=html.replace('<ul>','<ul class="list-style-sword">')
    
    page_title =  md.split('\n',2)[0].replace('#',''). strip()

    page1 = ZWebPage(EXPORT_PATH+target, page_title )
    page1.print(html)
    page1.write()


md2html("docs/rules.md",'rules.html')
md2html("docs/moderation.md",'moderation.html')
md2html("docs/Moderation_guide.md",'Moderation_guide.html')
md2html("docs/link_ds.md",'link_ds.html')


