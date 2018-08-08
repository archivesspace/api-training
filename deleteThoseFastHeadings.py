import json, sys, requests, authenticate, runtime, logging

# to do:  logging and other things should be handled differently, but this is just a proof of concept.
# for a more robust approach, see: https://github.com/hudmol/yale_as_post_mig_acc_fix/blob/master/delete_unlinked_subjects.rb
# that script deletes unlinked subjects, but the same basic approach could be used.

def search_and_destroy(baseURL, headers, query):
    search_results = requests.get(baseURL + query, headers=headers).json()
    result_count = len(search_results['results'])
    print('Found ' + str(result_count) + ' records.')
    if result_count > 0:
        print("Are you ready to delete those records?")
        if not input("Are you sure? (y/n): ").lower().strip()[:1] == "y":
            print("Those FAST records will live to see another day. Perhaps...")
            logging.info('Script aborted. No deletes today. Perhaps...\n')
            sys.exit(1)
        for result in search_results['results']:
            record_uri = result['id']
            json = result['json']
            #uh oh.  requests.delete not working on the LYRASIS installs (a 400 status is returned). is something else needed in the headers?
            #the next line works fine when running a local instal of 2.4.1
            delete_response = requests.delete(baseURL + record_uri, headers=headers).json()
            print(delete_response)
            logging.info('%s successfully deleted', record_uri)
            logging.info(record_uri + ' Deleted JSON: ' + json)
            logging.info('\n')
        print("Now we'll check to see if there are any more headings to delete.")
        search_and_destroy(baseURL, headers, query)
    else:
        print('Nothing to delete today.')

def main():
    logging.info('Started updates in %s', baseURL)
    search_and_destroy(baseURL, headers, query)
    logging.info('Finished updates in %s', baseURL)
    input("Press enter to exit... ")

if __name__ == '__main__':
    logging.basicConfig(filename='delete.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    # This is where we connect to ArchivesSpace.  See authenticate.py
    baseURL, headers = authenticate.login()
    # search records with source equal to "fast"
    query = '/search?page=1&filter={"query":{"jsonmodel_type":"field_query","field":"source","value":"fast","literal":true}}'
    main()
