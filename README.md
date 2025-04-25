# Python `Storage.Timeline` Client

A Python client library for Vitche's [Storage.Timeline](https://github.com/vitche/wasm_storage_timeline) server.  
This library provides a simple interface to interact with schemas and timelines, supporting addition and retrieval of both string and numeric data entries.

## Table of Contents
1. Introduction
2. Requirements
3. Installation
4. Environment Variables
5. Usage
6. Example
7. Development
8. License

---

## 1. Introduction

The Storage.Timeline client allows you to:
• Connect to a Storage.Timeline server.  
• Manage schemas (list them, reference them).  
• Work with timelines (get all entries, add new entries).  

It includes native handling for JSON-based data as well as a WASM-based parser for binary data, if needed.

---

## 2. Requirements

Refer to the [requirements.txt](./requirements.txt) file for the Python library dependencies:
• python-dotenv  
• setuptools  
• wasm_storage_timeline (installed via Git)  

Ensure you have a recent version of Python 3.

---

## 3. Installation

You can install this package locally using the provided setup script:

1. Clone (or download) this repository.  
2. Navigate into the project directory.  
3. Run the following command to install the package:

   pip install .

Or you can install via the setup.py script:

   python setup.py install

---

## 4. Environment Variables

The client uses an environment variable for the Storage.Timeline server URI:

• STORAGE_TIMELINE_URI – The base URL/URI of the Storage.Timeline server.  

You can store this variable in a .env file at the root of the project, which will be automatically loaded by python-dotenv.  
For example:

STORAGE_TIMELINE_URI=https://some.storage.timeline.server/

---

## 5. Usage

Below are the primary classes you will interact with:

• Storage(uri) – Represents the entire Storage service running at the given URI.  
  - schema(name): Returns a Schema object representing a particular schema.  
  - list(): Lists available schemas (if the server supports it).  

• Schema(storage, name) – Represents a named schema.  
  - time_line(name): Returns a TimeLine object.  
  - list(): Returns information about the schema (if supported by the server).  

• TimeLine(schema, name) – Represents a timeline within the referenced schema.  
  - all_numbers(), all_strings(), all_documents(): Get entries from the timeline.  
  - add_number(value, time=None), add_string(value, time=None): Add entries to the timeline.  

---

## 6. Example

There is a simple [test.py](./test.py) file in the repository demonstrating how to use this client in your own code:

```python
import os
from dotenv import load_dotenv
from storage_timeline_client import Storage

load_dotenv()  # loads .env file if present

uri = os.getenv("STORAGE_TIMELINE_URI")  # environment variable
storage = Storage(uri)

# Access a schema
schema = storage.schema("bsc.light-node.pancake.1000-pair")

# Access a timeline
time_line = schema.time_line("0x0018f45E3f088F5b088E020160Fd8d2bc91B4A8d")

# Get all documents
all_documents = time_line.all_documents()
print(all_documents)
```

Feel free to replace the schema and timeline parameters with those relevant to your server.

