import csv
import girder_client
import requests

gc = girder_client.GirderClient(apiUrl='http://localhost:8080/api/v1')
gc.authenticate('admin', 'letmein')
parent = gc.resourceLookup('collection/ResonantEco/datasets/LLNL')


def lookup_envo_number(envo):
    response = requests.get('https://www.ebi.ac.uk/ols/api/select',
                     params={'q': envo})
    json_response = response.json()
    return json_response['response']['docs'][0]['label']



def create_item_from_row(row):
    print("Ingesting {}".format(row[0]))
    item = gc.createItem(parent['_id'], row[0], reuseExisting=True)
    metadata = {
        'latitude': None,
        'longitude': None,
        'source': 'JGI'
    }
    metadata['timestamp'] = row[48]
    metadata['name'] = row[1]
    metadata['biome'] = lookup_envo_number(row[5])
    metadata['feature'] = lookup_envo_number(row[6])
    metadata['material'] = lookup_envo_number(row[7])
    gc.addMetadataToItem(item['_id'], {'meta': metadata})

def create_items_from_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            create_item_from_row(row)

if __name__ == '__main__':
    create_items_from_csv('metadata_1K_datasets_curated_JGI.csv')
