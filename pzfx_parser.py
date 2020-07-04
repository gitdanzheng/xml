"""Package to load and parse tables in a Prism pzfx file."""

import lxml.etree as ET
import pandas as pd
from itertools import count, chain, cycle
import numpy as np
import os

__version__ = '0.3'


class PrismFileLoadError(Exception):
    pass


def _get_all_text(element):
    s = ''
    for c in element.iter():
        if c.text is not None:
            s += c.text
    return s


def _subcolumn_to_numpy(subcolumn):
    # data = [float(_get_all_text(d)) if not (('Excluded' in d.attrib) and (d.attrib['Excluded'] == '1')) else np.nan
    #         for d in subcolumn.findall('d')]
    #
    # return np.array(data)
    data = []
    for d in subcolumn.findall('d'):
        if not (('Excluded' in d.attrib) and (d.attrib['Excluded'] == '1')):
            data.append(float(_get_all_text(d)))
        else:
            data.append(np.nan)
    return np.array(data)


def _parse_xy_table(table):
    xformat = table.attrib['XFormat']
    try:
        yformat = table.attrib['YFormat']
    except KeyError:
        yformat = None
    evformat = table.attrib['EVFormat']

    xscounter = count()
    def xsubcolumn_names(): return str(next(xscounter))
    if yformat == 'SEN':
        yslist = cycle(['Mean', 'SEM', 'N'])
        def ysubcolumn_names(): return next(yslist)
    elif yformat == 'upper-lower-limits':
        yslist = cycle(['Mean', 'Lower', 'Upper'])
        def ysubcolumn_names(): return next(yslist)
    else:
        yscounter = count()
        def ysubcolumn_names(): return str(next(yscounter))

    columns = {}
    for xcolumn in chain(table.findall('XColumn'), table.findall('XAdvancedColumn')):
        xcolumn_name = _get_all_text(xcolumn.find('Title'))
        for subcolumn in xcolumn.findall('Subcolumn'):
            subcolumn_name = xcolumn_name + '_' + xsubcolumn_names()
            columns[subcolumn_name] = _subcolumn_to_numpy(subcolumn)
    for ycolumn in chain(table.findall('YColumn'), table.findall('YAdvancedColumn')):
        ycolumn_name = _get_all_text(ycolumn.find('Title'))
        for subcolumn in ycolumn.findall('Subcolumn'):
            subcolumn_name = ycolumn_name + '_' + ysubcolumn_names()
            columns[subcolumn_name] = _subcolumn_to_numpy(subcolumn)

    maxlength = max([v.shape[0] for v in columns.values()])
    for k, v in columns.items():
        if v.shape[0] < maxlength:
            columns[k] = np.pad(v, ((0, maxlength-v.shape[0])),
                                mode='constant', constant_values=np.nan)
    return pd.DataFrame(columns)


def _parse_table_to_dataframe(table):
    table_id = table.attrib['ID']

    tabletype = table.attrib['TableType']

    if tabletype == 'XY' or tabletype == 'TwoWay' or tabletype == 'OneWay':
        df = _parse_xy_table(table)
    else:
        raise PrismFileLoadError('Cannot parse %s tables for now!' % tabletype)

    return df


def read_pzfx(filename):
    """Open and parse the Prism pzfx file given in `filename`.
    Returns a dictionary containing table names as keys and pandas DataFrames as values."""

    tree = ET.parse(filename)
    root = tree.getroot()
    ns = {"": "http://graphpad.com/prism/Prism.htm"}
    tables = {_get_all_text(table.find('Title', ns)): _parse_table_to_dataframe(table)
              for table in root.findall('Table', ns)}

    return tables


file = r"C:\Users\danz\github\xml\IBR-FSI5-C12b_bMe-TG_plasma.pzfx"
tables = read_pzfx(file)
print(tables)
