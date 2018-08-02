# storage-timeline-client.py
import json
import urllib.request

# Represents a time-line instance reference
class TimeLine:
    
    def __init__(self, schema, name):
        self.schema = schema
        self.name = name
        
    def allStrings(self):
        uriString = self.schema.storage.uri + 'timeline/all/strings?schema=' + self.schema.name + '&timeLine=' + self.name
        with urllib.request.urlopen(uriString, context = sslContext) as url:
            data = json.loads(url.read().decode())
            return data

# Represents a schema instance reference
class Schema:
    
    def __init__(self, storage, name):
        self.storage = storage
        self.name = name
        
    def timeLine(self, name):
        return TimeLine(self, name);
    
# Represents a storage instance reference
class Storage:
    
    def __init__(self, uri):
        self.uri = uri
    
    def schema(self, name):
        return Schema(self, name)
