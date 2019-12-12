from pathlib import Path
from bs4 import BeautifulSoup
import json
import markdown
import re
from dateutil.parser import parse
import datetime
import os
import string

def getlinks(text):
    return(re.findall(
                    r'\[([^\]]*)\]\(([^\)]*)\)', text))

def normalize_string(s):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    return " ".join(s.translate(translator).split()).upper()

def get_url_from_doc(doc):
    return doc["case_id"]+".html#"+doc["id"]

pathlist = Path("content/swp").glob('*.md')
corpus = {}

wrong_dates = {}
no_dates = []
count_dates = 0
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr or "SalVRec" in pathstr:
        continue
    with open("content"+pathstr, 'r') as page:
        metadata = {}
        while 1:
            line = page.readline()
            if line=="\n" or line=="":
                break
            if ":" in line:
                metadata[line.split(":",1)[0].lower()] = line.split(":",1)[1].strip()
        md = page.read()
        if len(md.split('\n<div markdown class="doc" id="')) > 1:
            for doc in md.split('\n<div markdown class="doc" id="'):
                if len(doc.strip().split("\n"))<=1:
                    #Ignore single lines (incl. the first split single div line)
                    continue
                doc_id = doc[:doc.find('">\n')].strip()

                try:
                    doc_title = metadata["title"]
                    doc_title = re.search(r'\n# (.*)', doc).group(1)
                    # strip out links
                    doc_title = re.sub(
                        r'\]\([^)]*\)', '', doc_title).replace('[', '').split(": ")[-1]                    
                except:
                    doc_title = doc_id

                doc = doc.replace("](/tag/", "] _").replace(".html)", " ")
                doc_html = markdown.markdown(doc[doc.find("\n\n")+2:])
                doc_text = ''.join(BeautifulSoup(doc_html, "lxml").findAll(
                    text=True)).replace("\n", "").replace("\t", "")
                
                # regex full date match
                date_match = re.search(
                    r'\n\n\[[\+\? ]*\=*\s*\b(January|Jan|February|Feb|March|Mar|April|Apr|May|June|July|August|Aug|September|Sept|Sep|October|Oct|November|Nov|December|Dec)\b\s*[\d]{1,2}\s*[\,\.]?\s*\d{4}\.?\s*\]\n\n', doc)
                #regex month only match
                month_match = re.search(
                    r'\n\n\[[\+\? ]*\=*\s*\b(January|Jan|February|Feb|March|Mar|April|Apr|May|June|July|August|Aug|September|Sept|Sep|October|Oct|November|Nov|December|Dec)\b\s*[\,\.]?\s*\d{4}\.?\s*\]\n\n', doc)
                if date_match:
                    count_dates +=1
                    date = re.search(r'[a-zA-Z0-9 ,.]{9,}', date_match.group()).group().strip()
                    datestr = parse(date, default=datetime.datetime(
                        1691, 1, 1)).strftime("%Y-%m-%d")
                    year = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%Y")
                    month = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%m")
                    day = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%d")
                    corpus[doc_id] = {"case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text, "date": datestr, "year": year, "month": month, "day": day}
                elif month_match:
                    date = re.search(
                        r'[a-zA-Z0-9 ,]{9,}', month_match.group()).group().strip()
                    datestr = parse(date, default=datetime.datetime(
                        1691, 1, 1)).strftime("%Y-%m")
                    year = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%Y")
                    month = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%m")
                    corpus[doc_id] = {"case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text, "date": datestr, "year": year, "month": month}
                else:
                    corpus[doc_id] = {"case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text}
                    wrong_date = re.search(r'\n\[[A-Za-z?+ .,0-9\'\(\)]*\]\n', doc)
                    if wrong_date:
                        wrong_dates[doc_id] = wrong_date.group().strip()
                    else:
                        no_dates.append(doc_id)

with open("docs.json","w") as outfile:
    outfile.write(json.dumps(corpus,indent=4))