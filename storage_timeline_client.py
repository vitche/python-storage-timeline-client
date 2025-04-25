import ssl
import json
import urllib.parse
import urllib.request
from wasm_execute import WASMExecutorFactory


def is_v2_api(value):
    return "cloudfunctions.net" in value


# Represents a time-line instance reference
def process_storage_timeline_data(response, binary=False):

    data = response.read()
    content_type = response.headers.get('Content-Type', '')

    if binary and 'application/storage-timeline' in content_type:
        # Use WASM to parse binary data
        wasm_runner = WASMExecutorFactory.instance()
        return wasm_runner.parse_timeline(data)
    else:
        # Regular JSON response
        return json.loads(data.decode('utf-8'))


class TimeLine:

    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

    def all_numbers(self, binary=False):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=number&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = self.schema.storage.uri + 'timeline/all/numbers?schema=' + self.schema.name + '&timeLine='
            uri_string += self.name

        request = urllib.request.Request(uri_string)
        if binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as response:
            return process_storage_timeline_data(response, binary)

    def all_strings(self, binary=False):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=string&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = self.schema.storage.uri + 'timeline/all/strings?schema=' + self.schema.name + '&timeLine='
            uri_string += self.name

        request = urllib.request.Request(uri_string)
        if binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as response:
            return process_storage_timeline_data(response, binary)

    def all_documents(self, binary=False):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=string&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = self.schema.storage.uri + 'timeline/all/strings?schema=' + self.schema.name + '&timeLine='
            uri_string += self.name

        request = urllib.request.Request(uri_string)
        if binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as response:
            data = process_storage_timeline_data(response, binary)

            # Parse JSON documents
            for item in data:
                try:
                    item["value"] = json.loads(item["value"])
                except:
                    item["value"] = None

            return data

    def add_number(self, value, time=None):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.schema.storage.uri + 'timeline/add/number'
        data = {
            "schema": self.schema.name,
            "timeLine": self.name,
            "value": value
        }
        if time is not None:
            data["time"] = time
        encoded_data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(uri_string, data=encoded_data)
        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()

    def add_string(self, value, time=None):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.schema.storage.uri + 'timeline/add/string'
        data = {
            "schema": self.schema.name,
            "timeLine": self.name,
            "value": value
        }
        if time is not None:
            data["time"] = time
        encoded_data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(uri_string, data=encoded_data)
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

    def list(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri_string = self.uri + 'storage/list'
        with urllib.request.urlopen(uri_string, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data
