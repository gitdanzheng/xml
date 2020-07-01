import os
from xml.etree import ElementTree

filename = "test.pzfx"
full_file = os.path.abspath(os.path.join(".", filename))

tree = ElementTree.parse(full_file)

root = tree.getroot()


table = root.find("Table")
title = table.find("Title")
print(title.text)

compd_titles = table.findall("YColumn/Title")
for t in compd_titles:
    print(t.text)

data = table.findall("YColumn/Subcolumn/d")
i = 100
for d in data:
    d.text = str(i)
    i += 1
    print(d.text)

xml_string = r'<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(root).decode()

with open("new.pzfx", "w") as new_file:
    new_file.write(xml_string)
