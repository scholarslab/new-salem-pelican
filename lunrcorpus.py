from pathlib import Path
from bs4 import BeautifulSoup
import json
import markdown
import re
from dateutil.parser import parse
import datetime
import os

pathlist = Path("content/").glob('**/*.md')
corpus = []
wrong_dates = []
no_dates = []
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr or "SalVRec" in pathstr:
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
        md = re.sub(
            r'\<div\ markdown\ class=\"doc\"\ id=\"n[0-9]{1,3}\.[0-9]{1,3}\"\>', '', md)
        if len(md.split("\n# Document: "))>1:
            for doc in md.split("\n# Document: "):
                if len(doc.strip().split("\n"))<=1:
                    #Ignore single lines (incl. the first split single div line)
                    continue
                doc_id = doc[:doc.find("\n")].strip()
                # regex full date match
                date_match = re.search(
                    r'\[\+*\?*\=*\s*\b(January|Jan|February|Feb|March|Mar|April|Apr|May|June|July|August|Aug|September|Sept|Sep|October|Oct|November|Nov|December|Dec)\b\s*[\d]{1,2}\s*[\,\.]?\s*\d{4}\s*', doc)
                if date_match:
                    date = re.search(r'[a-zA-Z0-9 ,.]{9,}', date_match.group()).group().strip()
                    datestr = parse(
                        date, default=datetime.datetime(1691, 1, 1)).strftime("%Y-%m-%d")
                else:
                    #regex month only match
                    month_match = re.search(
                        r'\[\+*\?*\=*\s*\b(January|Jan|February|Feb|March|Mar|April|Apr|May|June|July|August|Aug|September|Sept|Sep|October|Oct|November|Nov|December|Dec)\b\s*[\,\.]?\s*\d{4}\s*', doc)
                    if month_match:
                        date = re.search(
                            r'[a-zA-Z0-9 ,]{9,}', month_match.group()).group().strip()
                        datestr = parse(
                            date, default=datetime.datetime(1691, 1, 1)).strftime("%Y-%m")
                    else:
                        if re.search(r'\]\n', doc):
                            wrong_dates.append(doc_id)
                        else:
                            no_dates.append(doc_id)
                doc_html = markdown.markdown(doc[doc.find("\n\n")+2:])
                doc_text = ''.join(BeautifulSoup(doc_html,"lxml").findAll(text=True)).replace("\n","").replace("\t","")
                corpus.append(
                    {"id": doc_id, "slug": metadata["slug"], "title": metadata["title"], "content": doc_text, "date": datestr})
        else:
            html = markdown.markdown(md)
            text = ''.join(BeautifulSoup(html).findAll(text=True))
            corpus.append({"id": metadata["slug"], "slug": metadata["slug"], "title": metadata["title"], "date": metadata["date"], "content": text})
print("Writing to corpus")
with open("./content/search/corpus.json", 'w') as cout:
    cout.write(json.dumps(corpus))
print("Running index script")
os.system("cat content/search/corpus.json | scripts/build-index > content/search/idx.json")
print("\n\n###### SWP documents with suspected wrong formatting #######\n\n")
for doc in wrong_dates:
    print(doc)
print("\n\n###### SWP documents with no canonical date found #######\n\n")
for doc in no_dates:
    print(doc)
