import csv
import girder_client
import requests
import json


gc = girder_client.GirderClient(apiUrl='http://localhost:8080/api/v1')
gc.authenticate('admin', 'letmein')
parent = gc.resourceLookup('collection/ResonantEco/datasets/LLNL')

lookup_table = {}

def lookup_envo_number(envo):
    response = requests.get('https://www.ebi.ac.uk/ols/api/select',
                     params={'q': envo})
    json_response = response.json()
    try:
        label = json_response['response']['docs'][0]['label']
        lookup_table[envo] = label
        return label
    except IndexError:
        return None

def get_envo_number(envo):
    with open('envo_lookup.json', 'r') as f:
        lookup = json.load(f)
        try:
            return lookup[envo]
        except KeyError:
            return None

def create_item_from_row(row):
    if not row[7]:
        return
    print("Ingesting {}".format(row[0]))
    item = gc.createItem(parent['_id'], row[0], reuseExisting=True)
    metadata = {
        'latitude': None,
        'longitude': None,
        'source': 'JGI'
    }
    metadata['timestamp'] = row[48]
    metadata['name'] = row[1]
    metadata['biome'] = get_envo_number(row[5])
    metadata['feature'] = get_envo_number(row[6])
    metadata['material'] = get_envo_number(row[7])
    gc.addMetadataToItem(item['_id'], {'meta': metadata})

def create_items_from_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            create_item_from_row(row)

if __name__ == '__main__':
    create_items_from_csv('metadata_1K_datasets_curated_JGI.csv')
    # with open("envo_lookup.json", "w") as f:
    #     f.write(json.dumps(lookup_table))
