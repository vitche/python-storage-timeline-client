import ssl
import json
import urllib.parse
import urllib.request
from wasm_runner import WASMRunnerFactory


def is_v2_api(value):
    return "cloudfunctions.net" in value


# Class for working with time series with WASM support
class TimeLine:
    def __init__(self, schema, name, binary=False):
        self.schema = schema
        self.name = name
        self.binary = binary

    def _process_response(self, response):
        """Process server response, checking for binary format"""
        data = response.read()
        content_type = response.headers.get('Content-Type', '')

        if self.binary and 'application/storage-timeline' in content_type:
            # Use WASM to analyze binary data
            return self.schema.storage.wasm_runner.parse_timeline(data)
        else:
            # Regular JSON response
            return json.loads(data.decode('utf-8'))

    def all_numbers(self):
        """Get all numeric values from the timeline"""
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

        with urllib.request.urlopen(request, context=ssl_context) as response:
            return self._process_response(response)

    def all_strings(self):
        """Get all string values from the timeline"""
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

        with urllib.request.urlopen(request, context=ssl_context) as response:
            return self._process_response(response)

    def all_documents(self):
        """Get all documents from the timeline"""
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

        with urllib.request.urlopen(request, context=ssl_context) as response:
            data = self._process_response(response)

            # Parse JSON documents in response
            for item in data:
                try:
                    item["value"] = json.loads(item["value"])
                except:
                    item["value"] = None

            return data

    def add_number(self, value, time=None):
        """Add numeric value to timeline"""
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
        response = urllib.request.urlopen(request, context=ssl_context)
        return self._process_response(response)

    def add_string(self, value, time=None):
        """Add string value to timeline"""
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
        response = urllib.request.urlopen(request, context=ssl_context)
        return self._process_response(response)


# Class for working with data schemas
class Schema:
    def __init__(self, storage, name, binary=False):
        self.storage = storage
        self.name = name
        self.binary = binary

    def list(self):
        """Get list of timelines in the schema"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.storage.uri):
            uri_string = f"{self.storage.uri}?action=schema-list&schema={self.name}"
        else:
            uri_string = f"{self.storage.uri}/schema/list?schema={self.name}"

        request = urllib.request.Request(uri_string)
        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data

    def time_line(self, name):
        """Get timeline object"""
        return TimeLine(self, name, self.binary)


# Main class for working with data storage
class Storage:
    def __init__(self, uri, binary=False):
        """
        Initialize data storage

        Args:
            uri: Storage server URI
            binary: Whether to use binary format (uses WASM for processing)
        """
        self.uri = uri.rstrip('/')
        self.binary = binary
        # Use factory to obtain singleton WASM runner
        self.wasm_runner = WASMRunnerFactory.instance() if binary else None

    def schema(self, name):
        """Get data schema object"""
        return Schema(self, name, self.binary)

    def list(self):
        """Get list of data schemas in storage"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if is_v2_api(self.uri):
            uri_string = f"{self.uri}?action=storage-list"
        else:
            uri_string = f"{self.uri}/storage/list"

        request = urllib.request.Request(uri_string)
        with urllib.request.urlopen(request, context=ssl_context) as url:
            data = json.loads(url.read().decode())
            return data
