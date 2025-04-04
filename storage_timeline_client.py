import ssl
import json
import urllib.parse
import urllib.request


# Represents a time-line instance reference
class TimeLine:

    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

    def all_numbers(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        uri_string = f"{self.schema.storage.uri}/timeline/all/numbers?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
        request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def all_strings(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        uri_string = f"{self.schema.storage.uri}/timeline/all/strings?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
        request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def all_documents(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        uri_string = f"{self.schema.storage.uri}/timeline/all/strings?schema={self.schema.name}&timeLine={self.name}"

        request = urllib.request.Request(uri_string)
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
        request.add_header('Content-Type', 'application/storage-timeline')

        response = urllib.request.urlopen(request, context=ssl_context)
        return response.read()

    def add_string(self, value, time=None):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

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
        request.add_header('Content-Type', 'application/storage-timeline')

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

        uri_string = f"{self.storage.uri}/schema/list?schema={self.name}"

        request = urllib.request.Request(uri_string)
        request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def time_line(self, name):
        return TimeLine(self, name)


# Represents a storage instance reference
class Storage:

    def __init__(self, uri):
        # Remove trailing slash if present
        self.uri = uri.rstrip('/')

    def schema(self, name):
        return Schema(self, name)

    def list(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        uri_string = f"{self.uri}/storage/list"

        request = urllib.request.Request(uri_string)
        request.add_header('Content-Type', 'application/storage-timeline')

        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data
