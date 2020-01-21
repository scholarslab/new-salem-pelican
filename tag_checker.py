from pathlib import Path
import json
import markdown
import re
import datetime
import os
import string
import fileinput

pathlist = Path("content/swp").glob('*.md')

tags = {}
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr or "SalVRec" in pathstr:
        continue
    with open("content"+pathstr, 'r') as page:
        tags[pathstr] = []
        line = page.readline()
        while line:
            if len(tags[pathstr]) == 0 and line[:5] == "tags:":
                tags[pathstr] = [t.strip() for t in line[5:].split(",")]
                continue
            pattern = re.compile("\(\/tag\/[a-z_.]*\)")
            for match in re.finditer(pattern, line):
                person = match.group()[6:-6]
                if person not in tags[pathstr]:
                    print("Person not in tags for ", pathstr, ": ", person)
                    tags[pathstr].append(append(person))
            line = page.readline()

for path in tags.keys():
    lines = open('content'+path).read().splitlines()
    if lines[4][:5] != "tags:":
        print("Tags not on line 5!", path)
        exit()
    if lines[4] != "tags: " + ", ".join(sorted(tags[path])):    
        print(path)
        print("   "+", ".join(tags[path]))
        lines[4] = "tags: " + ", ".join(sorted(tags[path]))
        open('content'+path, 'w').write('\n'.join(lines))
