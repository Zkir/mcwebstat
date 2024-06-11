import markdown
from zwebpage import ZWebPage
import re
EXPORT_PATH = '_build/'

def md2html(source, target):
    f = open(source,  "r", encoding="utf-8")
    md=f.read()
    html = markdown.markdown(md)
    html=re.sub(r'.md',r'.html',html)

    #with open(EXPORT_PATH+target, 'w', encoding="utf-8") as f1:
    #       f1.write(html)

    page1 = ZWebPage(EXPORT_PATH+target, target)
    page1.print(html)
    page1.write()


md2html("docs/rules.md",'rules.html')
md2html("docs/moderation.md",'moderation.html')
md2html("docs/Moderation_guide.md",'Moderation_guide.html')
md2html("docs/link_ds.md",'link_ds.html')


