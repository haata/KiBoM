from bomlib.csv_writer import WriteCSV
from bomlib.xml_writer import WriteXML
from bomlib.html_writer import WriteHTML
from bomlib.xlsx_writer import WriteXLSX

import bomlib.columns as columns
from bomlib.component import *
from xml.etree import ElementTree
from bomlib.preferences import BomPref

import os, shutil, copy

#make a tmp copy of a given file
def TmpFileCopy(filename, fmt):

    filename = os.path.abspath(filename)

    if os.path.exists(filename) and os.path.isfile(filename):
        shutil.copyfile(filename, fmt.replace("%O",filename))

"""
Write BoM to file
filename = output file path
groups = [list of ComponentGroup groups]
headings = [list of headings to display in the BoM file]
prefs = BomPref object
"""
def WriteBoM(filename, groups, net, headings = columns.ColumnList._COLUMNS_DEFAULT, prefs=None):

    filename = os.path.abspath(filename)

    #no preferences supplied, use defaults
    if not prefs:
        prefs = BomPref()

    #remove any headings that appear in the ignore[] list
    headings = [h for h in headings if not h.lower() in [i.lower() for i in prefs.ignore]]

    # Remove any columns that have no entries
    if prefs.removeEmptyColumns:
        entries = []
        for group in groups:
            row = group.getRow(headings)
            for heading, field in zip(headings, row):
                if len(field) > 0 and heading not in entries:
                    entries.append(heading)
    for field in copy.copy(headings):
        if field not in entries:
            headings.remove(field)

    #if no extension is given, assume .csv (and append!)
    if len(filename.split('.')) < 2:
        filename += ".csv"

    #make a temporary copy of the output file
    if prefs.backup != False:
        TmpFileCopy(filename, prefs.backup)

    ext = filename.split('.')[-1].lower()

    result = False

    #CSV file writing
    if ext in ["csv","tsv","txt"]:
        if WriteCSV(filename, groups, net, headings, prefs):
            print("CSV Output -> {fn}".format(fn=filename))
            result = True
        else:
            print("Error writing CSV output")

    elif ext in ["htm","html"]:
        if WriteHTML(filename, groups, net, headings, prefs):
            print("HTML Output -> {fn}".format(fn=filename))
            result = True
        else:
            print("Error writing HTML output")

    elif ext in ["xml"]:
        if WriteXML(filename, groups, net, headings, prefs):
            print("XML Output -> {fn}".format(fn=filename))
            result = True
        else:
            print("Error writing XML output")

    elif ext in ["xlsx"]:
        if WriteXLSX(filename, groups, net, headings, prefs):
            print("XLSX Output -> {fn}".format(fn=filename))
            result = True
        else:
            print("Error writing XLSX output")

    else:
        print("Unsupported file extension: {ext}".format(ext=ext))

    return result
