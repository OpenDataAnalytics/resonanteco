import csv
from os.path import isfile, join
from os import listdir
import re
import sys
from girder_client import GirderClient


def ingest(directory, gc):
    table7Dict = {}
    table8Dict = {}
    table9Dict = {}
    for filename in [f for f in listdir(directory) if isfile(join(directory, f))]:
        if 'meta.txt' in filename:
            metaDict = parseCSV(directory, filename)
        if 'summary.txt' in filename:
            summaryDict = parseCSV(directory, filename)
        elif 'Table_7' in filename:
            table7 = parseTable(directory, filename)
            table7Dict[table7['taxon_oid']] = table7
        elif 'Table_8' in filename:
            table8 = parseTable(directory, filename)
            table8Dict[table8['taxon_oid']] = table8
        elif 'Table_9' in filename:
            table9 = parseTable(directory, filename)
            table9Dict[table9['taxon_oid']] = table9

    datasetsFolder = findDatasetFolder()
    for taxon_oid in metaDict:
        data = {"meta_": metaDict[taxon_oid], "summary": summaryDict[taxon_oid],
                "table7": table7Dict[taxon_oid], "table8": table8Dict[taxon_oid], "table9": table9Dict[taxon_oid]}
        data['meta'] = extractMeta(data)
        gc.loadOrCreateItem(taxon_oid, datasetsFolder['_id'], metadata=data)


def parseCSV(directory, filename):
    with open(join(directory, filename), 'r') as myfile:
        reader = csv.DictReader(myfile, delimiter='\t')
        return {value['taxon_oid']: value for value in list(reader)}


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


def parseTable(directory, filename):
    taxon_oid = re.search('([0-9]{2,})', filename).groups()[0]
    with open(join(directory, filename), 'r') as myfile:
        return thatFormatReader(taxon_oid, myfile.read())


def extractMeta(data):
    def getMaterial(name):
        if re.search('soil', name, re.IGNORECASE):
            return 'soil'
        elif re.search('water', name, re.IGNORECASE):
            return "water"
        elif re.search('vegetation', name, re.IGNORECASE):
            return 'vegetation'

    def getEcosystem(name):
        if re.search('arctic', name, re.IGNORECASE):
            return 'arctic'
    name = data['meta_']['Genome Name / Sample Name'].split(' - ')[1]
    latitude = data['meta_']['Lat']
    longitude = data['meta_']['Long']
    omics = data['meta_']['Transect']
    material = getMaterial(data['meta_']['Genome Name / Sample Name'])
    ecosystem = getEcosystem(data['meta_']['Genome Name / Sample Name'])
    return {
        'name': name,
        'latitude': float(latitude),
        'longitude': float(longitude),
        'timestemp': None,
        'material': material,
        'feature': None,
        'biome': ecosystem,
        'omics': omics,
        'source': 'LLNL'
    }


def findDatasetFolder():
    collection = gc.resourceLookup('/collection/ResonantEco')
    datasets = gc.resourceLookup('/collection/ResonantEco/datasets')
    return gc.resourceLookup('/collection/ResonantEco/datasets/LLNL')


if __name__ == '__main__':
    if len(sys.argv) < 5:
        sys.exit('Sample call: python ingest.py ./data localhost 8080 admin letmein')
    data_dir = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]
    gc = GirderClient(apiUrl='http://{}:{}/api/v1'.format(host, port))
    gc.authenticate(user, password)
    ingest(data_dir, gc)
