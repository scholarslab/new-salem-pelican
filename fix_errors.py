# Fixes common markdown errors in SWP docs


from pathlib import Path
import re
import datetime
import os
import string
import fileinput

COMMIT = True


# Interpreting number at start of lines as numbered lists is a problem.
# Sometimes dates will have period delimiters
# In any case, we don't ever want markdown replacing numbers in lists.
def unnumber_lists(doc,pathstr):
    pattern = re.compile("\n([0-9]+)\..{0,15}")
    for match in re.finditer(pattern, doc):
        print(pathstr, match.group())
    (doc,found) = re.subn("\n([0-9]+)\.",r"\n\1\\.",doc)
    if found:
        return doc


# Avoid code blocks
def no_code_blocks(doc,pathstr):
    pattern = re.compile(".{0,15}[ ]{4,}.{0,15}")
    for match in re.finditer(pattern, doc):
        print("\n",pathstr,"\n", match.group())
    
    (doc,found) = re.subn("\n[ ]{4,}",r"\n   ",doc)

    if found:
        return doc



# Interpreting number at start of lines as numbered lists is a problem.
# Sometimes dates will have period delimiters
# In any case, we don't ever want markdown replacing numbers in lists.
def single_newlines(doc,pathstr):
    ## Handle case with single space before newline
    pattern = re.compile(".{0,15}[^ ] \n([^\n]).{0,15}")
    for match in re.finditer(pattern, doc):
        print("\n",pathstr,"\n", match.group())
    
    (doc,found1) = re.subn("[^ ] \n([^\n])",r"  \n\1.",doc)

    ## Now handle case with no space before newline
    pattern = re.compile(".{0,15}([^\n])\n([^\n]).{0,15}")
    for match in re.finditer(pattern, doc):
        print("\n",pathstr,"\n", match.group())
    
    (doc,found2) = re.subn("([^ ][^\n ])\n([^\n])",r"\1  \n\2.",doc)
    
    if found1 or found2:
        return doc


pathlist = Path("content/swp").glob('*.md')
tags = {}
for path in pathlist:
    # because path is object not string
    pathstr = str(path)[7:]
    if "tag/" in pathstr or "SalVRec" in pathstr:
        continue
    with open("content"+pathstr, 'r') as page:
        doc = page.read()
        doc = unnumber_lists(doc, pathstr)
        doc = single_newlines(doc, pathstr)
        doc = no_code_blocks(doc,pathstr)
    if doc and COMMIT:
        with open("content"+pathstr, 'w') as page:
            page.write(doc)
