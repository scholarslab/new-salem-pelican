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
corpus = []
see_also = {}
see_also_case = {}
wrong_dates = {}
no_dates = []
count_dates = 0

docs_json = json.load(open("docs.json"))

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

                if doc.lstrip().split("\n")[0].startswith("(See also:"):
                    links = getlinks(doc.lstrip().split("\n")[0])
                    for link in links:
                        if link[1].split("#")[-1] in docs_json:
                            # link is okay, so let's move on
                            continue
                        if link[1] in see_also and normalize_string(link[0]) != normalize_string(see_also[link[1]]):
                            see_also_case[link[1]].append((metadata["slug"],link[0]))
                            print("URL mismatch:")
                            for case in see_also_case[link[1]]:
                                print("   ",case[0],"lists",link[1],"as",case[1])
                        else:
                            see_also_case[link[1]] = [(metadata["slug"],link[0])]
                        see_also[link[1]] = link[0]
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
                    corpus.append(
                        {"id": doc_id, "case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text, "date": datestr, "year": year, "month": month, "day": day})
                elif month_match:
                    date = re.search(
                        r'[a-zA-Z0-9 ,]{9,}', month_match.group()).group().strip()
                    datestr = parse(date, default=datetime.datetime(
                        1691, 1, 1)).strftime("%Y-%m")
                    year = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%Y")
                    month = parse(date, default=datetime.datetime(1691, 1, 1)).strftime("%m")
                    corpus.append(
                        {"id": doc_id, "case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text, "date": datestr, "year": year, "month": month})
                else:
                    corpus.append(
                        {"id": doc_id, "case_id": metadata["slug"], "case_title": metadata["title"], "slug": metadata["slug"], "title": doc_title, "content": doc_text})
                    wrong_date = re.search(r'\n\[[A-Za-z?+ .,0-9\'\(\)]*\]\n', doc)
                    if wrong_date:
                        wrong_dates[doc_id] = wrong_date.group().strip()
                    else:
                        no_dates.append(doc_id)

see_also_map = {}
see_also_not_found = []

for link in see_also:
    case = see_also[link].split(" -- ")[0]
    type = see_also[link].split(" -- ")[1]
    found = False

    for doc in corpus:
        if normalize_string(case) in normalize_string(doc["case_title"]):
            if doc["id"] == link[-len(doc["id"]):]:
                #Case number is real, don't need to remap
                found = True
                break
            elif normalize_string(type) in normalize_string(doc["title"]):
                # Case number isn't real, but found matching case and doc title.
                # Add to remap table
                if not found:
                    see_also_map[link+" / "+see_also[link]] = [doc]
                    found = True
                    continue
                if found:
                    # Already found - case contains multiple matching documents
                    see_also_map[link+" / "+see_also[link]].append(doc)
                    
    if not found:
        print("not found:",link, case, type)
        see_also_map[link+" / "+see_also[link]] = []

with open("seealso.json","w") as outfile:
    outfile.write(json.dumps(see_also_map,indent=4))

for link in see_also_map:
    if len(see_also_map[link])>1:
        print()