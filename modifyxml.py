from lxml import etree
import os
import re
# from xml.etree import ElementTree

filename = "test.pzfx"
full_file = os.path.abspath(os.path.join(".", filename))

tree = etree.parse(full_file)
root = tree.getroot()
# ns = re.match(r'{.*}', root.tag).group(0)
# table = root.find(f"{ns}Table")
# title = table.find(f"{ns}Title")
ns = {"": "http://graphpad.com/prism/Prism.htm"}
table = root.find("Table", namespaces=ns)
title = table.find("Title", namespaces=ns)
compd_titles = table.findall("YColumn/Title", namespaces=ns)

for t in compd_titles:
    print(t.text)

data = table.findall("YColumn/Subcolumn/d", namespaces=ns)
i = 18
for d in data:
    d.text = str(i)
    i += 1
    print(d.text)

new_file_name = f"{title.text}.pzfx"
with open(new_file_name, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
tree.write(open(new_file_name, "ab"), encoding="UTF-8")
