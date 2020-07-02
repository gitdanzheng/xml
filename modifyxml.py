from lxml import etree as ElementTree
import os
import re
# from xml.etree import ElementTree

filename = "test.pzfx"
full_file = os.path.abspath(os.path.join(".", filename))

tree = ElementTree.parse(full_file)
root = tree.getroot()
ns = re.match(r'{.*}', root.tag).group(0)
table = root.find(f"{ns}Table")
title = table.find(f"{ns}Title")

compd_titles = table.findall(f"{ns}YColumn/{ns}Title")
for t in compd_titles:
    print(t.text)

data = table.findall(f"{ns}YColumn/{ns}Subcolumn/{ns}d")
i = 20
for d in data:
    d.text = str(i)
    i += 1
    print(d.text)

with open("new.pzfx", "w") as new_file:
    new_file.write(r'<?xml version="1.0" encoding="UTF-8"?>')

tree.write(open("new.pzfx", "ab"), encoding="UTF-8")


# xml_string = r'<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(root).decode()
#
