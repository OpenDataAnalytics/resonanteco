import csv
from os.path import isfile, join
from os import listdir
import re
import sys

from resonanteco_server.model.meta import Meta
from resonanteco_server.model.summary import Summary
from resonanteco_server.model.table7 import Table7
from resonanteco_server.model.table8 import Table8
from resonanteco_server.model.table9 import Table9


def ingest(directory):
    Meta().collection.drop()
    Summary().collection.drop()
    Table7().collection.drop()
    Table8().collection.drop()
    Table9().collection.drop()
    for filename in [f for f in listdir(directory) if isfile(join(directory, f))]:
        if 'meta.txt' in filename:
            parseMeta(directory, filename)
        if 'summary.txt' in filename:
            parseSummary(directory, filename)
        elif 'Table_7' in filename:
            parseTable7(directory, filename)
        elif 'Table_8' in filename:
            parseTable8(directory, filename)
        elif 'Table_9' in filename:
            parseTable9(directory, filename)


def parseMeta(directory, filename):
    with open(join(directory, filename), 'r') as myfile:
        reader = csv.DictReader(myfile, delimiter='\t')
        for obj in reader:
            Meta().save(obj)

def parseSummary(directory, filename):
    with open(join(directory, filename), 'r') as myfile:
        reader = csv.DictReader(myfile, delimiter='\t')
        for obj in reader:
            Summary().save(obj)


def thatFormatReader(taxon_oid, text):
    dic = {'taxon_oid': taxon_oid}
    for line in text.splitlines()[3:]:
        splits = line.split('  ')
        key = splits[0]
        if key:
            valueStr = splits[-1].strip()
            try:
                value = float(valueStr)
            except ValueError:
                value = valueStr
            dic[key] = value
    return dic


def parseTable7(directory, filename):
    taxon_oid = re.search('([0-9]{2,})', filename).groups()[0]
    with open(join(directory, filename), 'r') as myfile:
        dic = thatFormatReader(taxon_oid, myfile.read())
        Table7().save(dic)


def parseTable8(directory, filename):
    taxon_oid = re.search('([0-9]{2,})', filename).groups()[0]
    with open(join(directory, filename), 'r') as myfile:
        dic = thatFormatReader(taxon_oid, myfile.read())
        Table8().save(dic)


def parseTable9(directory, filename):
    taxon_oid = re.search('([0-9]{2,})', filename).groups()[0]
    with open(join(directory, filename), 'r') as myfile:
        dic = thatFormatReader(taxon_oid, myfile.read())
        Table9().save(dic)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Missing argument')
    ingest(sys.argv[1])
