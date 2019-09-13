import csv
import girder_client
import requests
import json


gc = girder_client.GirderClient(apiUrl='http://localhost:8080/api/v1')
gc.authenticate('girder', 'girder')
parent = gc.resourceLookup('collection/ResonantEco/datasets/JGI')

lookup_table = {}
with open('envo_lookup.json', 'r') as f:
    lookup_table = json.load(f)
print(lookup_table)


def lookup_envo_number(envo):
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


def create_item_from_row(row):
    if not row[7]:
        return
    print("Ingesting {}".format(row[0]))
    item = gc.createItem(parent['_id'], row[0], reuseExisting=True)
    metadata = {
        'latitude': row[60],
        'longitude': row[59],
        'source': 'JGI'
    }
    metadata['timestamp'] = row[48]
    metadata['name'] = row[1]
    metadata['biome'] = lookup_envo_number(row[5])
    metadata['feature'] = lookup_envo_number(row[6])
    metadata['material'] = lookup_envo_number(row[7])
    metadata['omics'] = row[20].lower()
    gc.addMetadataToItem(item['_id'], {'meta': metadata})


def create_items_from_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            create_item_from_row(row)


if __name__ == '__main__':
    create_items_from_csv('./jgi_data/NMDC_metadata_datasets - NMDC_datasets_metadata.csv')
    # with open("envo_lookup.json", "w") as f:
    #     f.write(json.dumps(lookup_table))
