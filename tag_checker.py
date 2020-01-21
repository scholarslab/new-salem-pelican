from pathlib import Path
import json
import markdown
import re
import datetime
import os
import string
import fileinput

pathlist = Path("content/swp").glob('*.md')

missing_tags = {}
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr or "SalVRec" in pathstr:
        continue
    with open("content"+pathstr, 'r') as page:
        tags = []
        unlisted_people = []
        line = page.readline()
        while line:
            if len(tags) == 0 and line[:5] == "tags:":
                tags = [t.strip() for t in line[5:].split(",")]
                continue
            pattern = re.compile("\(\/tag\/[a-z_.]*\)")
            for match in re.finditer(pattern, line):
                person = match.group()[6:-6]
                if person not in tags:
                    print("Person not in tags for ", pathstr, ": ",person)
                    if pathstr in missing_tags:
                        if person not in missing_tags[pathstr]:
                            print("   Appending to list")
                            missing_tags[pathstr].append(person)
                    else:
                        print("   Adding new entry")
                        missing_tags[pathstr] = [person]
            line = page.readline()

for path in missing_tags.keys():
    lines = open('content'+path).read().splitlines()
    if lines[4][:5] != "tags:":
        print("Tags not on line 5!",path)
        exit()
    print(path)
    print("   "+", ".join(missing_tags[path]))
    lines[4] = lines[4] + ", " + ", ".join(missing_tags[path])
    open('content'+path, 'w').write('\n'.join(lines))
