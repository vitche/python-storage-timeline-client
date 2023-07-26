import ssl
import json
import urllib.parse
import urllib.request


def is_v2_api(value):
    return "cloudfunctions.net" in value


# Represents a time-line instance reference
class TimeLine:

    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

    def all_numbers(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=number&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = self.schema.storage.uri + 'timeline/all/numbers?schema=' + self.schema.name + '&timeLine='
            uri_string += self.name
        with urllib.request.urlopen(uri_string, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def all_strings(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=string&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = self.schema.storage.uri + 'timeline/all/strings?schema=' + self.schema.name + '&timeLine='
            uri_string += self.name
        with urllib.request.urlopen(uri_string, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def add_number(self, value):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.schema.storage.uri + 'timeline/add/number'
        data = urllib.parse.urlencode({
            "schema": self.schema.name,
            "timeLine": self.name,
            "value": value
        }).encode()
        request = urllib.request.Request(uri_string, data=data)
        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()

    def add_string(self, value):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.schema.storage.uri + 'timeline/add/string'
        data = urllib.parse.urlencode({
            "schema": self.schema.name,
            "timeLine": self.name,
            "value": value
        }).encode()
        request = urllib.request.Request(uri_string, data=data)
        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()

    # Represents a schema instance reference


class Schema:

    def __init__(self, storage, name):
        self.storage = storage
        self.name = name

    def list(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.storage.uri + 'schema/list?schema=' + self.name
        with urllib.request.urlopen(uri_string, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def time_line(self, name):
        return TimeLine(self, name)


# Represents a storage instance reference
class Storage:

    def __init__(self, uri):
        self.uri = uri

    def schema(self, name):
        return Schema(self, name)
