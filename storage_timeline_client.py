# storage_timeline_client.py
import ssl
import json
import urllib.request

# Represents a time-line instance reference
class TimeLine:
    
    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

    def allNumbers(self):
        sslContext = ssl.create_default_context();
        sslContext.check_hostname = False
        sslContext.verify_mode = ssl.CERT_NONE
        uriString = self.schema.storage.uri + 'timeline/all/numbers?schema=' + self.schema.name + '&timeLine=' + self.name
        with urllib.request.urlopen(uriString, context = sslContext) as url:
            data = json.loads(url.read().decode())
            return data

    def allStrings(self):
        sslContext = ssl.create_default_context();
        sslContext.check_hostname = False
        sslContext.verify_mode = ssl.CERT_NONE
        uriString = self.schema.storage.uri + 'timeline/all/strings?schema=' + self.schema.name + '&timeLine=' + self.name
        with urllib.request.urlopen(uriString, context = sslContext) as url:
            data = json.loads(url.read().decode())
            return data

# Represents a schema instance reference
class Schema:
    
    def __init__(self, storage, name):
        self.storage = storage
        self.name = name
        
    def list(self):
        sslContext = ssl.create_default_context();
        sslContext.check_hostname = False
        sslContext.verify_mode = ssl.CERT_NONE
        uriString = self.storage.uri + 'schema/list?schema=' + self.name
        with urllib.request.urlopen(uriString, context = sslContext) as url:
            data = json.loads(url.read().decode())
            return data
        
    def timeLine(self, name):
        return TimeLine(self, name);
    
# Represents a storage instance reference
class Storage:
    
    def __init__(self, uri):
        self.uri = uri
    
    def schema(self, name):
        return Schema(self, name)
