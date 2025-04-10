import ssl
import json
import urllib.parse
import urllib.request


def is_v2_api(value):
    return "cloudfunctions.net" in value


# Represents a time-line instance reference
class TimeLine:

    def __init__(self, schema, name, binary=False):
        self.schema = schema
        self.name = name
        self.binary = binary

    def all_numbers(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=number&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = f"{self.schema.storage.uri}/timeline/all/numbers?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def all_strings(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=string&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = f"{self.schema.storage.uri}/timeline/all/strings?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def all_documents(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}?format=string&schema={self.schema.name}&timeLine={self.name}"
        else:
            uri_string = f"{self.schema.storage.uri}/timeline/all/strings?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())

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

        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}"
            data = {
                "format": "number",
                "schema": self.schema.name,
                "timeLine": self.name,
                "value": value
            }
        else:
            uri_string = f"{self.schema.storage.uri}/timeline/add/number"
            data = {
                "schema": self.schema.name,
                "timeLine": self.name,
                "value": value
            }

        if time is not None:
            data["time"] = time

        encoded_data = urllib.parse.urlencode(data).encode()

        request = urllib.request.Request(uri_string, data=encoded_data)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()

    def add_string(self, value, time=None):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.schema.storage.uri):
            uri_string = f"{self.schema.storage.uri}"
            data = {
                "format": "string",
                "schema": self.schema.name,
                "timeLine": self.name,
                "value": value
            }
        else:
            uri_string = f"{self.schema.storage.uri}/timeline/add/string"
            data = {
                "schema": self.schema.name,
                "timeLine": self.name,
                "value": value
            }

        if time is not None:
            data["time"] = time

        encoded_data = urllib.parse.urlencode(data).encode()

        request = urllib.request.Request(uri_string, data=encoded_data)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()


# Represents a schema instance reference
class Schema:

    def __init__(self, storage, name, binary=False):
        self.storage = storage
        self.name = name
        self.binary = binary

    def list(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.storage.uri):
            uri_string = f"{self.storage.uri}?action=schema-list&schema={self.name}"
        else:
            uri_string = f"{self.storage.uri}/schema/list?schema={self.name}"

        request = urllib.request.Request(uri_string)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def time_line(self, name):
        # Use the binary attribute from the Schema instance
        return TimeLine(self, name, self.binary)


# Represents a storage instance reference
class Storage:

    def __init__(self, uri, binary=False):
        # Remove trailing slash if present
        self.uri = uri
        self.binary = binary

    def schema(self, name):
        # Use the binary attribute from the Storage instance
        return Schema(self, name, self.binary)

    def list(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.uri):
            uri_string = f"{self.uri}?action=storage-list"
        else:
            uri_string = f"{self.uri}/storage/list"

        request = urllib.request.Request(uri_string)
        if self.binary:
            request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data
