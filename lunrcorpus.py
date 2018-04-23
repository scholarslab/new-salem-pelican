from pathlib import Path
from bs4 import BeautifulSoup
import json
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
        text = " ".join(page.read().split())
        corpus.append({"id": metadata["slug"],"slug": metadata["slug"],"title":metadata["title"],"content":text})
        #soup = BeautifulSoup(page, 'html.parser')

print("Writing to corpus")
with open("corpus.json", 'w') as cout:
    cout.write(json.dumps(corpus))
