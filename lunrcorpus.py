from pathlib import Path
from bs4 import BeautifulSoup
import json
import markdown
import re

pathlist = Path("content/").glob('**/*.md')
corpus = []
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr:
        continue
    with open("content"+pathstr, 'r') as page:
        print("Parsing: "+pathstr)
        metadata = {}
        while 1:
            line = page.readline()
            if line=="\n" or line=="":
                break
            if ":" in line:
                metadata[line.split(":",1)[0].lower()] = line.split(":",1)[1].strip()
        md = page.read()
        if len(md.split("\n\n# Document: "))>1:
            for doc in md.split("\n\n# Document: "):
                doc_id = doc[:doc.find("\n\n")]
                doc_html = markdown.markdown(doc[doc.find("\n\n")+2:])
                doc_text = ''.join(BeautifulSoup(doc_html).findAll(text=True))
                corpus.append({"id": doc_id,"slug": metadata["slug"],"title":metadata["title"],"content":doc_text})
        else:
            html = markdown.markdown(md)
            text = ''.join(BeautifulSoup(html).findAll(text=True))
            corpus.append({"id": metadata["slug"],"slug": metadata["slug"],"title":metadata["title"],"content":text})

print("Writing to corpus")
with open("corpus.json", 'w') as cout:
    cout.write(json.dumps(corpus))
