import csv
from girder_client import GirderClient
import requests
import json
import os
import re
import sys


def lookup_envo_number(envo):
    with open('envo_lookup.json', 'r') as f:
        lookup_table = json.load(f)

    if envo in lookup_table:
        return lookup_table[envo]
    response = requests.get('https://www.ebi.ac.uk/ols/api/select',
                            params={'q': envo})
    json_response = response.json()
    try:
        label = json_response['response']['docs'][0]['label']
        lookup_table[envo] = label
        return label
    except IndexError:
        return None


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
    with open(os.path.join(directory, filename), 'r') as myfile:
        return thatFormatReader(taxon_oid, myfile.read())


def get_table_list_for_oid(oid):
    tables = []
    with open("File_Name-SP_ID_Mapping.txt") as search:
        for line in search:
            if oid in line.strip():
                tables.append(line.split()[0])

    return tables


def create_item_from_row(row, directory, gc):
    if not row[7]:
        return
    print("Ingesting {}".format(row[0]))
    parent = gc.resourceLookup('collection/ResonantEco/datasets/JGI')
    item = gc.createItem(parent['_id'], row[0], reuseExisting=True)
    latitude = None
    longitude = None
    try:
        latitude = float(row[60])
        longitude = float(row[59])
    except:
        pass
    metadata = {
        'latitude': latitude,
        'longitude': longitude,
        'source': 'JGI'
    }
    metadata['timestamp'] = row[48]
    metadata['name'] = row[1]
    metadata['biome'] = lookup_envo_number(row[5])
    metadata['feature'] = lookup_envo_number(row[6])
    metadata['material'] = lookup_envo_number(row[7])
    metadata['omics'] = row[20].lower()
    table7 = {}
    table8 = {}
    table9 = {}
    for filename in get_table_list_for_oid(row[8]):
        if 'Table_7' in filename:
            table7 = parseTable(directory, filename)
        elif 'Table_8' in filename:
            table8 = parseTable(directory, filename)
        elif 'Table_9' in filename:
            table9 = parseTable(directory, filename)

    gc.addMetadataToItem(
        item['_id'],
        {
            'meta': metadata,
            'table7': table7,
            'table8': table8,
            'table9': table9
        }
    )


def create_items_from_csv(path, data_dir, gc):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            create_item_from_row(row, data_dir, gc)


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
    create_items_from_csv('./jgi_data/NMDC_metadata_datasets - NMDC_datasets_metadata.csv', data_dir, gc)
    # with open("envo_lookup.json", "w") as f:
    #     f.write(json.dumps(lookup_table))
