# python-storage-timeline-client

# Represents a time-line instance reference
class TimeLine:
    
    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

# Represents a schema instance reference
class Schema:
    
    def __init__(self, storage, name):
        self.storage = storage
        self.name = name
        
    def timeLine(self, name):
        return TimeLine(self, );
    
class Storage:
    
    def __init__(self, uri):
        self.uri = uri
    
    def schema(self, name):
        return Schema(self, name)
