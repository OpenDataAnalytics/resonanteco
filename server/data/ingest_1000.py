import csv
import girder_client

gc = girder_client.GirderClient(apiUrl='http://localhost:8080/api/v1')
gc.authenticate('admin', 'letmein')
parent = gc.resourceLookup('collection/ResonantEco/datasets/LLNL')

def create_item_from_row(row):
    print("Ingesting {}".format(row[0]))
    item = gc.createItem(parent['_id'], row[0], reuseExisting=True)
    metadata = {}
    metadata['timestamp'] = row[48]
    metadata['name'] = row[1]
    gc.addMetadataToItem(item['_id'], {'meta': metadata})

def create_items_from_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            create_item_from_row(row)

if __name__ == '__main__':
    create_items_from_csv('metadata_1K_datasets_curated_JGI.csv')
