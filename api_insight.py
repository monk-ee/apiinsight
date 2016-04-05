import os
import requests
import time
from datetime import datetime
from requests_oauthlib import OAuth1
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


client_key = ''
client_secret = ''
resource_owner_key = ''
resource_owner_secret = ''
elasticsearch_url = 'search-apiinsight-kb6v2fx4mflhwi3bruxy5fihfq.us-east-1.es.amazonaws.com'

url = {}
url['site'] = 'http://api.softwareproduct.com/'
url['site_defaults'] = 'http://api.softwareproduct.com/defaults'
url['site_configuration'] = 'http://api.softwareproduct.com/configuration'
url['site_service_categories'] = 'http://api.softwareproduct.com/service_categories'
url['site_services'] = 'http://papi.softwareproduct.com/services'
url['site_employees'] = 'http://api.softwareproduct.com/employees'

awsauth = AWS4Auth(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], 'us-east-1', 'es', 
                   session_token=os.environ['AWS_SESSION_TOKEN'])
es = Elasticsearch([{'host': elasticsearch_url, 'port': 443}], use_ssl=True, verify_certs=True, http_auth=awsauth, 
                   connection_class=RequestsHttpConnection, ca_certs='root-ca.pem')

def testEndpoint(url):
    for name, endpoint in url.items():
        start = time.time()
        headeroauth = OAuth1(client_key, client_secret,
                             resource_owner_key, resource_owner_secret,
                             signature_type='auth_header')
        r = requests.get(endpoint, auth=headeroauth)
        roundtrip = time.time() - start
        payload = {}
        payload['timestamp'] = datetime.now()
        payload['roundtrip'] = float(roundtrip)
        payload['status'] = int(r.status_code)
        payload['headers'] = str(r.headers)
        payload['elapsed'] = float(r.elapsed.total_seconds())
        payload['url'] = str(endpoint)
        print(payload)
        try:
            es.index(index='apiinsight', doc_type='apiinsight', body=payload)
        except ConnectionError as ce:
            print(ce)
        except Exception as e:
            print(e)

testEndpoint(url)