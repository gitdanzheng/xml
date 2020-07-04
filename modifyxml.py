from lxml import etree
import pandas as pd
import os
# from xml.etree import ElementTree


def plasma_pzfx_to_df(pzfx=r"C:\Users\danz\github\xml\plasma_template.pzfx"):
    # """
    # define a function to parse pzfx file (plasma result) into a pd dataframe
    #
    # """

    tree = etree.parse(pzfx)
    root = tree.getroot()
    ns = {"": "http://graphpad.com/prism/Prism.htm"}
    table = root.find("Table", namespaces=ns)
    title = table.find("Title", namespaces=ns)
    prodrug = title.text

    compd_titles = table.findall("YColumn/Title", namespaces=ns)
    compd_title_list = [t.text for t in compd_titles]
    columns = []
    for compd_title in compd_title_list:
        for repeat in range(1, 4):
            columns.append(compd_title + str(repeat))

    x_data = table.findall("XColumn/Subcolumn/d", namespaces=ns)
    x_data_list = [d.text for d in x_data]

    y_data = table.findall("YColumn/Subcolumn/d", namespaces=ns)
    y_data_list = [d.text for d in y_data]

    length = len(x_data_list)
    # split y_data_list into 9 small lists
    y_lists = [y_data_list[i: i + length] for i in range(0, len(y_data_list), length)]

    df = pd.DataFrame(y_lists, columns=x_data_list)
    df = df.T
    df.columns = columns
    return title, df


def df_to_pzfx(prodrug, df):
    templete_pzfx = r"C:\Users\danz\github\xml\plasma_template.pzfx"
    tree = etree.parse(templete_pzfx)
    root = tree.getroot()
    ns = {"": "http://graphpad.com/prism/Prism.htm"}
    table = root.find("Table", namespaces=ns)
    title = table.find("Title", namespaces=ns)
    title.text = prodrug
    info_title = table.find("Info/Title", namespaces=ns)
    info_title.text = prodrug

    data_list = []
    for column in df.items():
        for i in column[1]:
            data_list.append(i)

    subcolumns = table.findall("YColumn/Subcolumn", namespaces=ns)
    j = 0
    for subcolumn in subcolumns:
        data = subcolumn.findall("d", namespaces=ns)
        for number in data:
            number.text = data_list[j]
            j += 1

    new_file_name = f"{prodrug}.pzfx"
    # with open(new_file_name, "w") as f:
    #     f.write(r'<?xml version="1.0" encoding="UTF-8"?>')
    tree.write(new_file_name)


def main():
    prodrug, df = plasma_pzfx_to_df()

    df2 = df+"aaa2"

    df_to_pzfx("test_prodrug", df2)


if __name__ == "__main__":
    main()
